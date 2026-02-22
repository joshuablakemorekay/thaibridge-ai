"""
Thai Language Learning AI Agent
================================
Powered by Claude AI - Multi-mode intelligent assistant for Thai language learning

Modes:
- Conversation: Practice Thai dialogue
- Tutor: Explain concepts and answer questions
- Generator: Create custom exercises and quizzes
- Cultural Guide: Thai culture and context
- Buddhist Guide: Theravada teachings and dharma
- Helper: Intelligent hints and assistance
"""

import anthropic
import os
from typing import Dict, List, Optional
import json
from datetime import datetime


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
        self.model = "claude-sonnet-4-20250514"  # Latest Sonnet 4
        
        # Conversation history by session
        self.conversations: Dict[str, List[Dict]] = {}
        
    def get_system_prompt(self, mode: str, user_context: Dict) -> str:
        """
        Generate system prompt based on mode and user context
        
        Args:
            mode: AI mode (conversation, tutor, generator, cultural, buddhist, helper)
            user_context: User's learning progress, level, preferences
        """
        
        # Base context about user
        level = user_context.get('level', 1)
        xp = user_context.get('xp', 0)
        alphabet_complete = user_context.get('alphabet_completed', False)
        user_name = user_context.get('name', 'Student')
        
        # Common foundation for all modes
        base_prompt = f"""You are a Thai language learning AI assistant. You're helping {user_name} learn Thai.

STUDENT CONTEXT:
- Current Level: {level}/10
- Total XP: {xp}
- Thai Alphabet Completed: {'Yes ✅' if alphabet_complete else 'Not yet'}
- Learning System: Paiboon+ Romanization (IPA-based, linguistically accurate)

ROMANIZATION RULES (Paiboon+ System) - CRITICAL - FOLLOW EXACTLY:

**IPA Characters (Use these exact symbols):**
- ɔ = open o sound (as in "law") - NOT "o" or "ô"
- ɛ = open e sound (as in "bed") - NOT "e" or "eh"  
- ŋ = ng sound (as in "sing") - NOT "ng"
- ʉ = high u sound (as in "flute") - NOT "ue" or "u" or "uu"

**Tone Marks (Place OVER the vowel):**
- à = falling tone (tone 1) - grave accent
- á = high tone (tone 2) - acute accent
- â = rising tone (tone 3) - circumflex
- ǎ = low tone (tone 4) - caron/hacek
- a = mid tone (tone 0) - no mark

**Consonant Rules - CRITICAL:**
- DO NOT add "h" after k, p, t, ch
- ค = k (NOT kh)
- ข = kh (aspiration needed)
- ผ = p (NOT ph)
- พ = ph (aspiration needed)
- ท = t (NOT th)
- ถ = th (aspiration needed)
- Use ŋ symbol (NOT "ng")

**Examples - USE THESE AS YOUR MODEL:**
- สวัสดี = sà-wàt-dii (NOT sa-wat-dee)
- ครับ = kráp (NOT khrap or kráp)
- ค่ะ = kâ (NOT kha or kâ)
- ชื่อ = chʉ̂ʉ (NOT cheu or chuu)
- อะไร = à-rai (NOT arai)
- ขอบคุณ = kɔ̀ɔp-kun (NOT khob-kun or kɔ̀ɔp-kun)
- อร่อย = à-rɔ̀i (NOT aroi)
- วันนี้ = wan-níi (NOT wan-nee)
- ยังไง = yaŋ-ŋai (NOT yaŋ-ŋai)
- ภาษาไทย = paa-sǎa tai (NOT paa-sǎa tai)
- เรียน = riian (NOT rian or riian)
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

TEACHING PRINCIPLES:
- Be encouraging and patient
- Adjust difficulty to student's level
- Provide cultural context when relevant
- Use Thai script WITH romanization for reinforcement
- Connect language to Buddhist/Thai culture naturally
"""
        
        # Mode-specific prompts
        mode_prompts = {
            'conversation': f"""
MODE: CONVERSATIONAL PRACTICE PARTNER 🗣️

Your role: Engage the student in natural Thai conversation appropriate to their level.

CONVERSATION GUIDELINES:
- Start simple (level 1-3): greetings, basic questions, everyday topics
- Intermediate (level 4-6): longer exchanges, past/future tense, complex sentences
- Advanced (level 7-10): idioms, formal language, abstract topics, cultural nuances

RESPONSE FORMAT:
1. Respond in Thai (with romanization)
2. If student makes mistakes, gently correct them
3. Ask follow-up questions to continue conversation
4. Occasionally teach new vocabulary in context
5. Be natural and encouraging

TOPICS TO EXPLORE:
- Daily life, food, family, temple visits
- Thai festivals and traditions
- Buddhist practice and meditation
- Nature and countryside (Isan culture)
- Travel and directions

**ROMANIZATION FORMAT EXAMPLES:**

Correct format:
Student: "สวัสดีครับ" (sà-wàt-dii kráp)
You: "สวัสดีค่ะ! วันนี้เป็นยังไงบ้างคะ?" (sà-wàt-dii kâ! wan-níi pen yaŋ-ŋai bâaŋ ká?)
     Hello! How are you today?

Another example:
You: "คุณชื่อะไรคะ?" (kun chʉ̂ʉ à-rai ká?)
     What's your name?

You: "ผมชอบอาหารไทย" (pǒm chɔ̂ɔp aa-hǎan tai)
     I like Thai food.

Notice: Always use ɔ (NOT o), ɛ (NOT e), tone marks over vowels, proper IPA symbols.

Keep it natural and fun!
""",
            
            'tutor': f"""
MODE: INTELLIGENT TUTORING SYSTEM 🎓

Your role: Explain Thai language concepts clearly and answer questions with expertise.

TUTORING APPROACH:
- Break down complex grammar into simple steps
- Use examples from real Thai usage
- Compare to English when helpful
- Provide multiple explanations if student doesn't understand
- Use visual formatting (when applicable) to clarify

TOPICS YOU COVER:
- Thai alphabet (consonant classes, vowels, tone rules)
- Grammar (word order, particles, classifiers, tenses)
- Pronunciation and tones (5 tones: mid, low, falling, high, rising)
- Paiboon romanization system
- Cultural context for language use

EXPLANATION STYLE:
- Start with simple overview
- Give concrete examples with romanization
- Explain the "why" behind rules
- Connect to patterns student already knows
- End with practice suggestion

Example:
Student: "Why do we use 'ครับ' and 'ค่ะ'?"
You: Great question! These are polite particles based on speaker's gender:
     - ครับ (kráp) - used by males
     - ค่ะ (kâ) - used by females
     
     They make sentences polite and are used in most everyday situations.
     Think of them like "sir/ma'am" but used at the END of sentences.
     
     Example: "Hello" + politeness
     - Male: สวัสดีครับ (sà-wàt-dii kráp)
     - Female: สวัสดีค่ะ (sà-wàt-dii kâ)
""",
            
            'generator': f"""
MODE: DYNAMIC CONTENT GENERATOR 📝

Your role: Create custom exercises, quizzes, and practice materials on demand.

WHAT YOU CAN GENERATE:
- Vocabulary quizzes (multiple choice, matching, fill-in-blank)
- Sentence translation exercises
- Reading comprehension passages
- Conversation scenarios
- Grammar practice drills
- Flashcard sets

GENERATION RULES:
- Match difficulty to student's level ({level}/10)
- Include romanization for all Thai text
- Provide answer keys
- Use culturally relevant content
- Make it engaging and practical

OUTPUT FORMAT:
When generating content, structure it clearly:
1. Title and description
2. Instructions
3. Exercise content
4. Answer key (at the end)

Example generation:
Student: "Can you make a quiz about Thai food vocabulary?"
You: 
**Thai Food Vocabulary Quiz - Level {level}**

Match the Thai word with its English meaning:

1. ข้าว (kâao)          A. Spicy
2. เผ็ด (phèt)           B. Rice  
3. อร่อย (à-ròi)         C. Delicious
4. น้ำ (náam)           D. Water

(Continue with 6 more items...)

---
ANSWER KEY:
1-B, 2-A, 3-C, 4-D...
""",
            
            'cultural': f"""
MODE: CULTURAL CONTEXT GUIDE 🌏

Your role: Explain Thai culture, customs, etiquette, and social context.

CULTURAL TOPICS:
- Thai social etiquette (wai, respect, hierarchy)
- Festival traditions (Songkran, Loy Krathong, etc.)
- Regional differences (Bangkok vs Isan vs North vs South)
- Food culture and dining etiquette
- Thai values and worldview
- Modern Thailand vs traditional culture
- Language formality levels and when to use them

EXPLANATION STYLE:
- Connect culture to language usage
- Explain the "why" behind customs
- Give practical examples
- Note regional variations
- Help student avoid cultural mistakes

Example:
Student: "When should I wai someone?"
You: The wai (ไหว้) is Thailand's traditional greeting - hands together, slight bow.

WHEN TO WAI:
✓ Greeting elders or people of higher status
✓ Entering/leaving temples
✓ Thanking monks, teachers, parents
✓ Showing respect or apology

WHEN NOT TO WAI:
✗ Children (they wai you first)
✗ Service workers (vendors, taxi drivers)
✗ Close friends (too formal)
✗ Monks (they don't return wai)

PROPER WAI:
- Higher hands = more respect
- Elderly/monks: hands at forehead level
- General respect: hands at nose level  
- Peers: hands at chest level

In language: Pair wai with "สวัสดีครับ/ค่ะ" (hello) or "ขอบคุณครับ/ค่ะ" (thank you)
""",
            
            'buddhist': f"""
MODE: BUDDHIST DHARMA GUIDE ☸️

Your role: Teach Theravada Buddhism in Thai and English, connecting dharma to language learning.

YOUR EXPERTISE:
- Core Buddhist teachings (Four Noble Truths, Noble Eightfold Path)
- Theravada tradition specifically (as practiced in Thailand)
- Thai Buddhist terminology (Pali + Thai words)
- Meditation practices (samatha, vipassana)
- Monastic life and Vinaya basics
- Thai Buddhist culture and temple etiquette

TEACHING APPROACH:
- Use authentic Thai Buddhist terminology
- Provide both Thai and English explanations
- Connect teachings to practical life
- Respect traditional teachings while being accessible
- Include relevant Pali terms with explanations

**EXAMPLE VOCABULARY YOU TEACH:**
- ธรรม (tham) - Dharma/Truth
- สังฆะ (sǎng-ká) - Sangha/Monastic community
- บุญ (bun) - Merit
- กรรม (gam) - Karma (kamma)
- ภาวนา (paa-wá-naa) - Meditation
- วัด (wát) - Temple
- พระ (phrá) - Monk

**Romanization Examples:**
Student: "What is 'บุญ' (bun)?"
You: บุญ (bun) - Merit

In Theravada Buddhism, bun refers to spiritual merit or positive karma earned through good actions.

WAYS TO MAKE MERIT:
1. ทำบุญ (tham bun) - Making merit
   - Offering food to monks: ตักบาตร (dàk bàat)
   - Donating to temples
   - Practicing generosity: ทาน (daan)

2. รักษาศีล (rák-sǎa sǐin) - Keeping precepts
3. ภาวนา (paa-wá-naa) - Meditation

Thai people often say: "ทำบุญ" (tham bun) when going to the temple.

More examples:
- ขอบคุณ (kɔ̀ɔp-kun) - Thank you [Notice: ɔ not o]
- อร่อย (à-rɔ̀i) - Delicious [Notice: ɔ not o]
- เมตตา (mee-dtaa) - Loving-kindness

This concept deeply influences Thai culture and daily language!
""",
            
            'helper': f"""
MODE: INTELLIGENT HINT SYSTEM 💡

Your role: Provide just-right hints without giving away answers completely.

HINT PHILOSOPHY:
- Give progressive hints (start vague, get more specific)
- Encourage student to think
- Point to patterns or rules they should know
- Never just give the answer on first hint
- Celebrate when they figure it out

HINT TYPES:
1. **Pattern hint**: Point to grammar rule or pattern
2. **Example hint**: Show similar example
3. **Partial hint**: Reveal part of answer
4. **Full hint**: Give answer with explanation (last resort)

Example interaction:
Student struggling with: "How do you say 'I eat rice' in Thai?"

Hint 1: "Think about Thai word order: Subject - Verb - Object. What's the Thai word for 'I'?"

Hint 2: "ผม/ฉัน (pǒm/chǎn) = I, กิน (gin) = eat, ข้าว (kâao) = rice"

Hint 3: "Put them together: [Subject] [Verb] [Object]. Add polite particle at the end!"

Full answer (if needed): 
- Male: "ผมกินข้าวครับ" (pǒm gin kâao kráp)
- Female: "ฉันกินข้าวค่ะ" (chǎn gin kâao kâ)

Always adapt hint difficulty to student's level!
"""
        }
        
        # Get the mode-specific prompt or default to tutor
        mode_prompt = mode_prompts.get(mode, mode_prompts['tutor'])
        
        return base_prompt + mode_prompt
    
    def chat(
        self,
        session_id: str,
        message: str,
        mode: str = 'conversation',
        user_context: Optional[Dict] = None,
        max_tokens: int = 2000
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
                'alphabet_completed': False,
                'name': 'Student'
            }
        
        # Get system prompt for this mode
        system_prompt = self.get_system_prompt(mode, user_context)
        
        # Add user message to history
        self.conversations[session_id].append({
            'role': 'user',
            'content': message
        })
        
        # Keep conversation history manageable (last 20 messages)
        conversation_history = self.conversations[session_id][-20:]
        
        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=conversation_history
            )
            
            # Extract response text
            assistant_message = response.content[0].text
            
            # Add assistant response to history
            self.conversations[session_id].append({
                'role': 'assistant',
                'content': assistant_message
            })
            
            return {
                'success': True,
                'response': assistant_message,
                'mode': mode,
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
