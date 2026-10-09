"""
Thai Language Learning AI Agent
================================
Powered by Claude AI - Multi-mode intelligent assistant for Thai language learning

Modes:
- Conversation: Practice Thai dialogue
- Tutor: Explain concepts and answer questions
- Generator: Create custom exercises and quizzes
- Cultural Guide: Thai culture and context
- Buddhist Guide: the Dhamma through one of three lenses (universal, Thai culture, neutral)
- Helper: Intelligent hints and assistance
"""

import anthropic
import os
from typing import Dict, List, Optional
import json
from datetime import datetime

# The politeness/monastic rules the Sentences page teaches, in prompt form.
# Imported rather than copied so the tutor and the page cannot disagree.
from thai_registers import REGISTER_RULES_FOR_AI


# Roleplay scenarios for the conversation partner. Each puts the AI in a fixed
# role so the learner can practise a real, bounded situation instead of an open
# blank chat. Shown as chips on the chat page (title + icon) and looked up here
# by id when a message arrives, so the roleplay framing is authored server-side
# and never trusted from the browser.
ROLEPLAY_SCENARIOS = {
    'restaurant': {'title': 'Order at a restaurant', 'icon': '🍜',
                   'ai_role': 'a friendly waiter at a Thai restaurant',
                   'setting': 'The student has just sat down and is ready to order.'},
    'market': {'title': 'Haggle at the market', 'icon': '🛍️',
               'ai_role': 'a cheerful market vendor selling clothes and souvenirs',
               'setting': 'The student is browsing your stall and may want to bargain on the price.'},
    'taxi': {'title': 'Take a taxi', 'icon': '🚕',
             'ai_role': 'a Bangkok taxi driver',
             'setting': 'The student has just got in and needs to tell you where to go.'},
    'directions': {'title': 'Ask for directions', 'icon': '🗺️',
                   'ai_role': 'a friendly local on the street',
                   'setting': 'The student looks a little lost and needs directions somewhere.'},
    'meeting': {'title': 'Meet someone new', 'icon': '👋',
                'ai_role': 'a friendly Thai person meeting the student for the first time',
                'setting': 'You have just been introduced at a social gathering.'},
    # A monk/temple roleplay was deliberately left out: on the cheap live model
    # the AI does not hold monastic register reliably (slips ครับ, ท่าน vs โยม),
    # which would misteach it. The monastic-register handling below is kept so it
    # can be re-added on a stronger model. (Josh's call, 2026-07-23.)
}


# The three ways into the Dhamma that /dhamma-and-culture offers, as lenses on
# the Buddhist mode. Before these existed the mode only knew one of them: it
# taught every teaching as Thai temple vocabulary, so a learner who asked a
# plain Dhamma question got Thai Buddhism back whether they wanted it or not.
# Like the roleplay scenarios, the browser sends only the id and the wording is
# looked up here, so the prompt is never trusted from the client.
DHAMMA_LENSES = {
    'universal': {
        'title': 'Universal Dhamma', 'icon': '☸️',
        'blurb': 'The teachings themselves, for anywhere. No Thai required.',
        'prompt': """
MODE: BUDDHIST DHAMMA GUIDE — UNIVERSAL DHAMMA

In this lens you are a Dhamma guide first. The student may not be learning
Thai at all, so do not steer the answer back to the language.

The student has chosen to focus on Buddhist teachings and practices that can be
understood and applied anywhere. Answer from the teachings themselves, not from
any one country's customs.

- Explain in plain English first. Use a Pali term where it helps (dukkha, mettā,
  anattā) and give its meaning in the same sentence.
- This site follows the Theravada tradition and the Pali Canon. Where another
  Buddhist school sees a point differently, say so briefly and fairly rather than
  presenting one view as the only one.
- Do NOT frame answers through Thailand, Thai temples, Thai customs or Thai
  society, and do not assume the student will visit a temple or join a
  community. Practice advice must work for someone at home, anywhere.
- No Thai script or Thai vocabulary unless the student asks for it. The Thai
  romanisation and register rules above apply only if Thai comes up.
- Keep to clear, practical teaching at an introductory level — the Four Noble
  Truths, the Eightfold Path, the precepts, generosity and meditation.
""",
    },
    'thai': {
        'title': 'Dhamma in Thai culture', 'icon': '🎭',
        'blurb': 'How Buddhism lives in Thai language, temples and daily life.',
        'prompt': """
MODE: BUDDHIST DHAMMA GUIDE — DHAMMA IN THAI CULTURE

The student wants to understand how Buddhism is expressed through Thai language,
society, temples and traditions.
Teach Buddhism through Thai language acquisition — Dhamma terms are vocabulary first.
For every term give: Pali root, Thai script, ThaiBridge Spelling, and usage context.
Example: บุญ (bun) — from Pali "puñña" — you will hear this when Thais discuss
going to the temple: ไปทำบุญ (bpai tam bun) = "going to make merit".

Focus on everyday temple and practice language: ทำบุญ (tam bun), ตักบาตร (dtàk-bàat),
รักษาศีล (rák-sǎa sǐin), ภาวนา (paa-wá-naa), นิพพาน (níp-paan).
Keep Dhamma explanations at the level of the Four Noble Truths and basic precepts —
this is a language app, not a seminary.

Always connect each concept to a phrase Thais actually use in daily life or at the temple,
so the student gains communicative competence in Thai religious contexts.

FINAL CHECK before you answer: every romanisation follows the ThaiBridge Spelling rules
above. No "h" after p, t, k or ch — พระ is prá, พ่อ is pɔ̂ɔ, คุณ is kun.
""",
    },
    'neutral': {
        'title': 'Culturally neutral', 'icon': '🕊️',
        'blurb': 'The practice on its own — no tradition or identity to adopt.',
        'prompt': """
MODE: BUDDHIST DHAMMA GUIDE — CULTURALLY NEUTRAL

In this lens you are a Dhamma guide first. The student may not be learning
Thai at all, so do not steer the answer back to the language.

The student wants to study and practise the Dhamma without adopting any
particular cultural identity or tradition.

- Teach the practice as practice: what it is, why it helps, and how to do it.
  The precepts, generosity and meditation stand on their own.
- Leave out customs, rituals, ceremonies, devotional practices and any
  country's culture (Thai, Tibetan, Japanese or other) unless the student asks.
- Never suggest the student needs to become a Buddhist, join a community or
  call themselves anything. Say "the teaching" or "this practice", not
  "we Buddhists".
- Use plain English. Use a Pali term only where no English word does the job,
  and give its meaning.
- No Thai script or Thai vocabulary unless the student asks for it. The Thai
  romanisation and register rules above apply only if Thai comes up.
- Keep to an introductory level.
""",
    },
}
# Listed first on /dhamma-and-culture, and the lens that answers the question
# as asked rather than adding a culture the student did not ask for.
DEFAULT_DHAMMA_LENS = 'universal'

# Length rules for the modes whose answers ran past the reply cap. In a
# side-by-side test half of Haiku 4.5's replies and two thirds of Sonnet 5.5's
# were cut off mid-sentence at 500 tokens: Thai script is token-heavy, so 500
# tokens is only about 200 words. Asking for less gets most answers under;
# app.py raises the cap (AI_REPLY_TOKENS) for the rest, since a model does not
# count words exactly. Conversation and helper replies were already short.
_EXPLAIN_LENGTH = """
LENGTH: keep each answer under about 150 words (fewer when it includes a lot of
Thai script). Teach the heart of the question well rather than everything about
it, and offer to go further on one part instead of continuing.
"""
MODE_LENGTH = {
    'tutor': _EXPLAIN_LENGTH,
    'cultural': _EXPLAIN_LENGTH,
    'buddhist': """
LENGTH: keep every answer under about 180 words (fewer when it includes Thai
script). Cover the heart of the question well rather than everything about
it, and offer to go deeper on one part instead of continuing.
""",
    'generator': """
LENGTH: 5 items unless the student asks for more, and keep the whole exercise,
answer key included, under about 350 words.
""",
}

def thinking_off(model: str) -> Optional[Dict]:
    """The setting that stops a model thinking before it answers, or None.

    The app's small reply budget has to go on the answer itself.
    Haiku 4.5 does not think unless asked, so it needs nothing. The 5.5 models
    think by default and each has its own off switch: Sonnet 5.5 rejects
    "disabled" and uses "between_tools" instead.
    """
    if model.startswith('claude-sonnet-5-5'):
        return {'type': 'between_tools'}
    if model.startswith('claude-haiku-5-5'):
        return {'type': 'disabled'}
    return None


class ThaiLearningAI:
    """
    Core AI Agent for Thai Language Learning
    Manages conversations, context, and multiple interaction modes
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the AI agent with Anthropic API"""
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found. Please set it in environment or pass to constructor.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        # Model is configurable via the AI_MODEL env var. The public Render demo
        # sets AI_MODEL to a cheap Haiku model so visitor messages cost a fraction
        # of a cent (see render.yaml); this default is the fallback for local dev.
        #
        # The old default (claude-sonnet-4-20250514) was retired and now returns a
        # 404, which silently broke local AI. The default is Sonnet 5.5 — the
        # same model the live site runs (render.yaml), verified with this code
        # path. It thinks by default, so chat() switches that off (thinking_off)
        # and the whole reply budget goes to the answer. Set AI_MODEL to override.
        self.model = os.environ.get("AI_MODEL", "claude-sonnet-5-5")
        # Buddhist mode can run on its own model. Haiku 4.5 got Dhamma terms
        # wrong in a side-by-side test (mettā described as muditā, an invented
        # five-step dependent origination) where Haiku 5.5 got all ten right at
        # a tenth of the price. It is a setting, not code, so rolling back is
        # one change on Render. Unset, it follows AI_MODEL.
        self.dhamma_model = os.environ.get("DHAMMA_AI_MODEL") or self.model
        
        # Conversation history by session
        self.conversations: Dict[str, List[Dict]] = {}
        
    def get_system_prompt(self, mode: str, user_context: Dict,
                          scenario: Optional[str] = None,
                          lens: Optional[str] = None) -> str:
        """
        Generate system prompt based on mode and user context

        Args:
            mode: AI mode (conversation, tutor, generator, cultural, buddhist, helper)
            user_context: User's learning progress, level, preferences
            scenario: optional roleplay scenario id (conversation mode only)
            lens: Dhamma lens id from DHAMMA_LENSES (buddhist mode only);
                  anything unknown falls back to DEFAULT_DHAMMA_LENS
        """

        # Base context about user
        level = user_context.get('level', 1)
        xp = user_context.get('xp', 0)
        user_name = user_context.get('name', 'Student')

        if lens not in DHAMMA_LENSES:
            lens = DEFAULT_DHAMMA_LENS
        # The shared foundation tells every mode to add Thai script and tie
        # language to Thai Buddhist culture. The universal and neutral lenses
        # exist precisely to NOT do that, so those lines are left out for them
        # rather than left in for their own instructions to argue with.
        thai_principles = (
            ''
            if mode == 'buddhist' and lens != 'thai'
            else ('- Use Thai script WITH romanization for reinforcement\n'
                  '- Connect language to Buddhist/Thai culture naturally\n')
        )

        # Common foundation for all modes
        base_prompt = f"""You are a Thai language learning AI assistant. You're helping {user_name} learn Thai.

STUDENT CONTEXT:
- Current Level: {level}/10
- Total XP: {xp}
- Learning System: ThaiBridge Spelling (IPA-based, linguistically accurate)

ROMANIZATION RULES (ThaiBridge Spelling) - CRITICAL - FOLLOW EXACTLY:

**IPA Characters (Use these exact symbols):**
- ɔ = open o sound (as in "law") - NOT "o" or "ô"
- ɛ = open e sound (as in "bed") - NOT "e" or "eh"  
- ŋ = ng sound (as in "sing") - NOT "ng"
- ʉ = high u sound (as in "flute") - NOT "ue" or "u" or "uu"

**Tone Marks (Place OVER the vowel):**
- a = mid tone (tone 0) - no mark
- à = low tone (tone 1) - grave accent
- â = falling tone (tone 2) - circumflex
- á = high tone (tone 3) - acute accent
- ǎ = rising tone (tone 4) - caron/hacek

**Consonant Rules - CRITICAL:**
- NEVER add "h" after k, p, t or ch. This system does not mark aspiration
  at all, so two letters that differ only by aspiration share one spelling.
- ข ค ฆ = k    (never kh)
- ผ พ ภ = p    (never ph)
- ฐ ฑ ฒ ถ ท ธ = t    (never th)
- ฉ ช ฌ = ch   (never chh)
- ก = g · ป = bp · ต = dt · บ = b · ด = d · ซ ศ ษ ส = s
- Use the ŋ symbol, never the letters "ng"

**Examples - USE THESE AS YOUR MODEL:**
- สวัสดี = sà-wàt-dii (NOT sa-wat-dee)
- ครับ = kráp (NOT khrap or krub)
- ค่ะ = kâ (NOT kha or ka)
- ชื่อ = chʉ̂ʉ (NOT cheu or chuu)
- อะไร = à-rai (NOT arai)
- ขอบคุณ = kɔ̀ɔp-kun (NOT khob-kun or kop-koon)
- อร่อย = à-rɔ̀i (NOT aroi)
- วันนี้ = wan-níi (NOT wan-nee)
- ยังไง = yaŋ-ŋai (NOT yang-ngai)
- ภาษาไทย = paa-sǎa tai (NOT phasa thai)
- เรียน = riian (NOT rian or rien)
- หรือ = rʉ̌ʉ (NOT rue or reu)

**Critical Rules:**
1. ALWAYS use ɔ for the "or" sound (never use "o")
2. ALWAYS use ɛ for the "eh" sound (never use "e")
3. ALWAYS use ŋ for "ng" sound (never write "ng")
4. ALWAYS use ʉ for high u (never "uu" or "ue")
5. DO NOT add "h" after k, p, t, ch unless it represents aspiration
6. ALWAYS place tone marks OVER vowels (à not a`)
7. ALWAYS show romanization in parentheses after Thai script
8. Format: Thai (romanization) = English

{REGISTER_RULES_FOR_AI}
TEACHING PRINCIPLES:
- Be encouraging and patient
- Adjust difficulty to student's level
- Provide cultural context when relevant
- Write only your finished answer: check facts, tones and spellings first, and
  never correct yourself partway through
{thai_principles}"""
        
        # Mode-specific prompts
        mode_prompts = {
            'conversation': f"""
MODE: CONVERSATIONAL PRACTICE PARTNER

Engage in natural Thai conversation using Thai script with ThaiBridge Spelling for every utterance.
Match complexity to level: L1-3 use present tense and daily topics (food, greetings, family);
L4-6 add past/future tense and reasons (dtɔ̂ŋ-gaan, lɛ́ɛo); L7-10 include proverbs, formal
registers, and abstract topics.

After each exchange, highlight ONE error with a gentle correction — for example:
"Good try! In Thai we say bpai (ไป) not pai for 'go'." Then end with a follow-up question
that reuses the corrected pattern, so the student practises it immediately.

Keep the conversation flowing — do not lecture mid-exchange. The goal is communicative
confidence, not perfection.

TOPICS: daily life, food, markets, family, temple visits, Thai festivals, Buddhist practice,
Isan culture, travel and directions.
""",
            
            'tutor': f"""
MODE: INTELLIGENT TUTORING SYSTEM

Teach Thai language concepts using a consistent three-step structure:
(1) One-sentence core rule, (2) Two or three examples with Thai script, ThaiBridge
Spelling, and English meaning, (3) One pattern insight beginning with "Notice how...".

For tone rules, always establish consonant class and vowel length before giving the tone.
For particles, show placement in a full sentence AND explain the emotional nuance
(e.g. ná (นะ) softens a request; kâ (ค่ะ) signals female-speaker politeness).

End every explanation with: "Try making your own sentence using [concept]."

Avoid linguistic jargon — say "rising tone" not "non-phonemic pitch contour".
Compare to English only when it genuinely helps; never force the comparison.
""",
            
            'generator': f"""
MODE: DYNAMIC CONTENT GENERATOR

Create targeted Thai practice materials to these standards:
every item must include Thai script, ThaiBridge Spelling, and English meaning;
use authentic Thai contexts (markets, BTS, temples, family meals);
mix recognition tasks (matching, multiple choice) with production tasks (translation, fill-in);
include 5 items per exercise (up to 10 if the student asks) with a complete answer key that has brief explanations.

For vocabulary quizzes, group items by semantic field (food, transport, temple vocabulary).
For translation exercises, use complete sentences — never isolated words.
Level {level} guidance: L1-3 present tense only; L4+ add time markers and aspect (lɛ́ɛo, gam-laŋ, jà).

Structure output as: Title → Instructions → Exercise items → Answer key with explanations.
""",
            
            'cultural': f"""
MODE: CULTURAL CONTEXT GUIDE

Explain Thai culture through its effect on language, not as background facts.
Structure every response: (1) cultural concept overview, (2) the specific words or
phrases it shapes — e.g. hierarchy drives pronoun choice (phǒm/chán vs guu/mʉŋ),
(3) a concrete real-life scenario ("When meeting someone older, add kráp or kâ after
EVERY sentence, not just greetings"), (4) the most common mistake to avoid.

Connect festivals to time expressions (bpii nâa, dʉan sìp-sɔ̌ɔŋ), regional
differences to vocabulary (Isan sâap vs Central à-rɔ̀i for "delicious"), and
social hierarchy to formality registers.

Always leave the student with a phrase they can use immediately.
""",
            
            'buddhist': DHAMMA_LENSES[lens]['prompt'],

            'helper': f"""
MODE: INTELLIGENT HINT SYSTEM

Give progressive hints calibrated to language learning. Always wait for the student
to respond between hints before moving to the next level.

Hint 1 — Grammar/pattern hint: point to the relevant rule (tone class, classifier,
particle function) without revealing the answer.
Hint 2 — Parallel example: show a similar sentence with different vocabulary.
Hint 3 — Partial reveal: expose one key word or component ("It starts with dtɔ̂ŋ (ต้อง)...").
Hint 4 — Full answer with breakdown: give the complete answer, then explain each part.
Never jump to Hint 4 before giving at least Hint 2.

Calibrate to the student: if they are clearly stuck after Hint 2, ask "Would a similar
example help, or should I show part of the answer?" Celebrate genuine effort:
"You identified the tone mark — that is the hardest part!"
"""
        }
        
        # Get the mode-specific prompt or default to tutor
        mode_prompt = mode_prompts.get(mode, mode_prompts['tutor'])

        # In conversation mode, an optional scenario turns the partner into a
        # fixed role for a bounded, realistic practice situation.
        roleplay = ''
        if mode == 'conversation' and scenario in ROLEPLAY_SCENARIOS:
            sc = ROLEPLAY_SCENARIOS[scenario]
            roleplay = f"""

ACTIVE ROLEPLAY — STAY IN CHARACTER
You are role-playing as {sc['ai_role']}. {sc['setting']}
Remain fully in character as this Thai person for the whole conversation. Do NOT
switch into being a teacher or narrator. Speak the way this person really would.
Every line: Thai script, then ThaiBridge Spelling, then a short English gloss in
brackets. Keep replies short and realistic — one or two sentences, like real speech.
When the student slips, model the correct Thai naturally in your own reply rather
than stopping to lecture. If they seem stuck, ask a simple question to keep the
scene moving. Open the scene yourself with a natural first line in character.
"""
            if sc.get('monastic'):
                roleplay += ("Use proper monastic register: refer to yourself as อาตมา, "
                             "address the lay visitor as โยม, and greet with เจริญพร. A monk "
                             "does NOT use the lay politeness particles ครับ or ค่ะ at all — "
                             "use เจริญพร in their place.\n")

        return base_prompt + mode_prompt + MODE_LENGTH.get(mode, '') + roleplay
    
    def model_for(self, mode: str) -> str:
        """The model a mode runs on: Buddhist mode may have its own."""
        return self.dhamma_model if mode == 'buddhist' else self.model

    def chat(
        self,
        session_id: str,
        message: str,
        mode: str = 'conversation',
        user_context: Optional[Dict] = None,
        max_tokens: int = 2000,
        scenario: Optional[str] = None,
        lens: Optional[str] = None
    ) -> Dict:
        """
        Send a message and get AI response
        
        Args:
            session_id: Unique session identifier
            message: User's message
            mode: AI mode to use
            user_context: User's learning context
            max_tokens: Maximum response length
            
        Returns:
            Dict with 'response', 'mode', 'tokens_used'
        """
        
        # Initialize conversation history if needed
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        # Default user context
        if user_context is None:
            user_context = {
                'level': 1,
                'xp': 0,
                'name': 'Student'
            }
        
        model = self.model_for(mode)

        # Get system prompt for this mode (with any active roleplay scenario
        # or Dhamma lens)
        system_prompt = self.get_system_prompt(mode, user_context, scenario, lens)
        
        # Add user message to history
        self.conversations[session_id].append({
            'role': 'user',
            'content': message
        })
        
        # Keep conversation history manageable (last 20 messages)
        conversation_history = self.conversations[session_id][-20:]
        
        try:
            # Call Claude API
            request = dict(model=model, max_tokens=max_tokens,
                           system=system_prompt, messages=conversation_history)
            thinking = thinking_off(model)
            if thinking:
                request['thinking'] = thinking
            # Cache the instructions and the conversation so far: each message
            # in a chat re-sends both, and a cached re-send costs a tenth of the
            # price. Sent as a raw field because the pinned SDK (0.75) predates
            # top-level cache_control. Models with a higher cache minimum than
            # this prompt (Haiku 4.5 needs 4,096 tokens) simply don't cache.
            request['extra_body'] = {'cache_control': {'type': 'ephemeral'}}
            response = self.client.messages.create(**request)

            # Join the text blocks rather than taking content[0]: a model that
            # can think puts a thinking block first, and content[0].text would
            # come back empty or raise.
            assistant_message = ''.join(
                b.text for b in response.content if b.type == 'text')
            
            # Add assistant response to history
            self.conversations[session_id].append({
                'role': 'assistant',
                'content': assistant_message
            })
            
            return {
                'success': True,
                'response': assistant_message,
                'mode': mode,
                'model': model,
                'tokens_used': {
                    'input': response.usage.input_tokens,
                    'output': response.usage.output_tokens
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except anthropic.APIError as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'API error occurred. Please check your API key and try again.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'An unexpected error occurred.'
            }
    
    def get_quick_hint(
        self,
        question: str,
        context: str,
        user_answer: Optional[str] = None,
        user_context: Optional[Dict] = None
    ) -> str:
        """
        Get a quick hint for a quiz question (no conversation history)
        
        Args:
            question: The quiz question
            context: Additional context about the question
            user_answer: User's attempted answer (if any)
            user_context: User's learning context
            
        Returns:
            Hint text
        """
        
        if user_context is None:
            user_context = {'level': 1, 'xp': 0}
        
        system_prompt = self.get_system_prompt('helper', user_context)
        
        user_message = f"""Question: {question}

Context: {context}"""
        
        if user_answer:
            user_message += f"\n\nStudent's answer: {user_answer}"
            user_message += "\n\nProvide a helpful hint without giving away the complete answer."
        else:
            user_message += "\n\nStudent needs a hint to get started. Give a gentle nudge in the right direction."
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                system=system_prompt,
                messages=[{'role': 'user', 'content': user_message}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Sorry, couldn't generate hint: {str(e)}"
    
    def explain_answer(
        self,
        question: str,
        correct_answer: str,
        user_answer: str,
        user_context: Optional[Dict] = None
    ) -> str:
        """
        Explain why an answer is correct/incorrect (for quiz results)
        
        Args:
            question: The quiz question
            correct_answer: The correct answer
            user_answer: What the user answered
            user_context: User's learning context
            
        Returns:
            Detailed explanation
        """
        
        if user_context is None:
            user_context = {'level': 1, 'xp': 0}
        
        system_prompt = self.get_system_prompt('tutor', user_context)
        
        is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
        
        if is_correct:
            user_message = f"""The student answered correctly!

Question: {question}
Their answer: {user_answer}

Please explain WHY this is correct and reinforce their understanding. Keep it brief but encouraging."""
        else:
            user_message = f"""The student got this wrong.

Question: {question}
Their answer: {user_answer}
Correct answer: {correct_answer}

Please explain:
1. Why their answer was incorrect
2. Why the correct answer is right
3. How to remember this for next time

Be encouraging and clear!"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                system=system_prompt,
                messages=[{'role': 'user', 'content': user_message}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Explanation unavailable: {str(e)}"
    
    def generate_content(
        self,
        content_type: str,
        topic: str,
        difficulty: int,
        user_context: Optional[Dict] = None
    ) -> str:
        """
        Generate custom learning content (quizzes, exercises, etc.)
        
        Args:
            content_type: Type of content (quiz, exercise, flashcards, etc.)
            topic: Topic or theme
            difficulty: Difficulty level (1-10)
            user_context: User's learning context
            
        Returns:
            Generated content as formatted text
        """
        
        if user_context is None:
            user_context = {'level': difficulty, 'xp': 0}
        else:
            user_context['level'] = difficulty
        
        system_prompt = self.get_system_prompt('generator', user_context)
        
        user_message = f"""Please generate a {content_type} about: {topic}

Difficulty level: {difficulty}/10

Make it engaging and appropriate for this level!"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                system=system_prompt,
                messages=[{'role': 'user', 'content': user_message}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Content generation failed: {str(e)}"
    
    def clear_conversation(self, session_id: str):
        """Clear conversation history for a session"""
        if session_id in self.conversations:
            del self.conversations[session_id]
    
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session"""
        return self.conversations.get(session_id, [])


# Singleton instance (will be initialized in app.py with API key)
_ai_agent_instance = None

def get_ai_agent(api_key: Optional[str] = None) -> ThaiLearningAI:
    """Get or create the AI agent singleton"""
    global _ai_agent_instance
    
    if _ai_agent_instance is None:
        _ai_agent_instance = ThaiLearningAI(api_key=api_key)
    
    return _ai_agent_instance
