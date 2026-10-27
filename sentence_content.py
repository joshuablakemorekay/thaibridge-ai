"""Content for the Sentences page: patterns, conversations and "glue" phrases.

SENTENCE_PATTERNS teaches aspect markers and question forms. CONVERSATIONS are
the real-world dialogues — also played by Listen & answer, whose questions live
in listening.py. CONVERSATIONAL_PHRASES are the small phrases that keep talk
moving.

Data only, moved out of app.py so other modules can use it without importing
app.py. app.py imports these names back unchanged.
"""

# ============================================
# SENTENCE PATTERNS & CONVERSATIONS
# ============================================

SENTENCE_PATTERNS = {
    'aspect_markers': {
        'title': 'Aspect Markers - Showing Time & Completion',
        'explanation': 'Thai uses particles to show whether actions are ongoing, completed, or future. These are ESSENTIAL for fluency!',
        
        'progressive': {
            'name': 'Progressive: กำลัง (gam-laŋ) - "am/is/are -ing"',
            'pattern': 'Subject + กำลัง + Verb',
            'usage': 'Shows action happening RIGHT NOW',
            'examples': {
                'male': [
                    {
                        'thai': 'ผมกำลังกินข้าวครับ',
                        'paiboon': 'pǒm gam-laŋ gin kâao kráp',
                        'english': 'I am eating rice',
                        'breakdown': 'ผม (I) + กำลัง (progressive) + กิน (eat) + ข้าว (rice) + ครับ (polite particle)'
                    },
                    {
                        'thai': 'ผมกำลังทำงานครับ',
                        'paiboon': 'pǒm gam-laŋ tam ŋaan kráp',
                        'english': 'I am working',
                        'breakdown': 'ผม (I) + กำลัง (progressive) + ทำงาน (work) + ครับ (polite particle)'
                    },
                    {
                        'thai': 'เขากำลังอ่านหนังสือครับ',
                        'paiboon': 'kǎo gam-laŋ àan nǎŋ-sʉ̌ʉ kráp',
                        'english': 'He/She is reading a book',
                        'breakdown': 'เขา (he/she) + กำลัง (progressive) + อ่าน (read) + หนังสือ (book) + ครับ (polite particle)'
                    }
                ],
                'female': [
                    {
                        'thai': 'ดิฉันกำลังกินข้าวค่ะ',
                        'paiboon': 'dì-chǎn gam-laŋ gin kâao kâ',
                        'english': 'I am eating rice',
                        'breakdown': 'ดิฉัน (I) + กำลัง (progressive) + กิน (eat) + ข้าว (rice) + ค่ะ (polite particle)'
                    },
                    {
                        'thai': 'ดิฉันกำลังทำงานค่ะ',
                        'paiboon': 'dì-chǎn gam-laŋ tam ŋaan kâ',
                        'english': 'I am working',
                        'breakdown': 'ดิฉัน (I) + กำลัง (progressive) + ทำงาน (work) + ค่ะ (polite particle)'
                    },
                    {
                        'thai': 'เขากำลังอ่านหนังสือค่ะ',
                        'paiboon': 'kǎo gam-laŋ àan nǎŋ-sʉ̌ʉ kâ',
                        'english': 'He/She is reading a book',
                        'breakdown': 'เขา (he/she) + กำลัง (progressive) + อ่าน (read) + หนังสือ (book) + ค่ะ (polite particle)'
                    }
                ]
            }
        },
        
        'completed': {
            'name': 'Completed: แล้ว (lɛ́ɛo) - "already"',
            'pattern': 'Subject + Verb + แล้ว',
            'usage': 'Shows action is FINISHED/COMPLETED',
            'examples': {
                'male': [
                    {
                        'thai': 'ผมกินข้าวแล้วครับ',
                        'paiboon': 'pǒm gin kâao lɛ́ɛo kráp',
                        'english': 'I already ate / I have eaten',
                        'breakdown': 'ผม (I) + กิน (eat) + ข้าว (rice) + แล้ว (already) + ครับ (polite particle)'
                    },
                    {
                        'thai': 'ผมทำงานเสร็จแล้วครับ',
                        'paiboon': 'pǒm tam ŋaan sèt lɛ́ɛo kráp',
                        'english': 'I finished working already',
                        'breakdown': 'ผม (I) + ทำงาน (work) + เสร็จ (finish) + แล้ว (already) + ครับ (polite particle)'
                    },
                    {
                        'thai': 'เขาไปแล้วครับ',
                        'paiboon': 'kǎo bpai lɛ́ɛo kráp',
                        'english': 'He/She already went / has gone',
                        'breakdown': 'เขา (he/she) + ไป (go) + แล้ว (already) + ครับ (polite particle)'
                    }
                ],
                'female': [
                    {
                        'thai': 'ดิฉันกินข้าวแล้วค่ะ',
                        'paiboon': 'dì-chǎn gin kâao lɛ́ɛo kâ',
                        'english': 'I already ate / I have eaten',
                        'breakdown': 'ดิฉัน (I) + กิน (eat) + ข้าว (rice) + แล้ว (already) + ค่ะ (polite particle)'
                    },
                    {
                        'thai': 'ดิฉันทำงานเสร็จแล้วค่ะ',
                        'paiboon': 'dì-chǎn tam ŋaan sèt lɛ́ɛo kâ',
                        'english': 'I finished working already',
                        'breakdown': 'ดิฉัน (I) + ทำงาน (work) + เสร็จ (finish) + แล้ว (already) + ค่ะ (polite particle)'
                    },
                    {
                        'thai': 'เขาไปแล้วค่ะ',
                        'paiboon': 'kǎo bpai lɛ́ɛo kâ',
                        'english': 'He/She already went / has gone',
                        'breakdown': 'เขา (he/she) + ไป (go) + แล้ว (already) + ค่ะ (polite particle)'
                    }
                ]
            }
        },
        
        'future': {
            'name': 'Future: จะ (jà) - "will"',
            'pattern': 'Subject + จะ + Verb',
            'usage': 'Shows action WILL HAPPEN in the future',
            'examples': {
                'male': [
                    {
                        'thai': 'ผมจะกินข้าวครับ',
                        'paiboon': 'pǒm jà gin kâao kráp',
                        'english': 'I will eat rice',
                        'breakdown': 'ผม (I) + จะ (will) + กิน (eat) + ข้าว (rice) + ครับ (polite particle)'
                    },
                    {
                        'thai': 'ผมจะไปเมืองไทยครับ',
                        'paiboon': 'pǒm jà bpai mʉaŋ-tai kráp',
                        'english': 'I will go to Thailand',
                        'breakdown': 'ผม (I) + จะ (will) + ไป (go) + เมืองไทย (Thailand) + ครับ (polite particle)'
                    },
                    {
                        'thai': 'เขาจะมาพรุ่งนี้ครับ',
                        'paiboon': 'kǎo jà maa prûŋ-níi kráp',
                        'english': 'He/She will come tomorrow',
                        'breakdown': 'เขา (he/she) + จะ (will) + มา (come) + พรุ่งนี้ (tomorrow) + ครับ (polite particle)'
                    }
                ],
                'female': [
                    {
                        'thai': 'ดิฉันจะกินข้าวค่ะ',
                        'paiboon': 'dì-chǎn jà gin kâao kâ',
                        'english': 'I will eat rice',
                        'breakdown': 'ดิฉัน (I) + จะ (will) + กิน (eat) + ข้าว (rice) + ค่ะ (polite particle)'
                    },
                    {
                        'thai': 'ดิฉันจะไปเมืองไทยค่ะ',
                        'paiboon': 'dì-chǎn jà bpai mʉaŋ-tai kâ',
                        'english': 'I will go to Thailand',
                        'breakdown': 'ดิฉัน (I) + จะ (will) + ไป (go) + เมืองไทย (Thailand) + ค่ะ (polite particle)'
                    },
                    {
                        'thai': 'เขาจะมาพรุ่งนี้ค่ะ',
                        'paiboon': 'kǎo jà maa prûŋ-níi kâ',
                        'english': 'He/She will come tomorrow',
                        'breakdown': 'เขา (he/she) + จะ (will) + มา (come) + พรุ่งนี้ (tomorrow) + ค่ะ (polite particle)'
                    }
                ]
            }
        },
        
        'combined': {
            'name': 'Combined Patterns - Multiple Markers',
            'pattern': 'Mix markers for precise meaning',
            'usage': 'Combine to show complex time relationships',
            'examples': {
                'male': [
                    {
                        'thai': 'ผมกำลังจะไปครับ',
                        'paiboon': 'pǒm gam-laŋ jà bpai kráp',
                        'english': 'I am about to go',
                        'breakdown': 'ผม (I) + กำลัง (progressive) + จะ (will) + ไป (go) + ครับ (polite particle)',
                        'note': 'Progressive + Future = "about to"'
                    },
                    {
                        'thai': 'ผมกินข้าวแล้วจะไปครับ',
                        'paiboon': 'pǒm gin kâao lɛ́ɛo jà bpai kráp',
                        'english': 'After I eat, I will go',
                        'breakdown': 'ผม (I) + กิน (eat) + ข้าว (rice) + แล้ว (after) + จะ (will) + ไป (go) + ครับ (polite particle)',
                        'note': 'Completed + Future = sequential actions'
                    }
                ],
                'female': [
                    {
                        'thai': 'ดิฉันกำลังจะไปค่ะ',
                        'paiboon': 'dì-chǎn gam-laŋ jà bpai kâ',
                        'english': 'I am about to go',
                        'breakdown': 'ดิฉัน (I) + กำลัง (progressive) + จะ (will) + ไป (go) + ค่ะ (polite particle)',
                        'note': 'Progressive + Future = "about to"'
                    },
                    {
                        'thai': 'ดิฉันกินข้าวแล้วจะไปค่ะ',
                        'paiboon': 'dì-chǎn gin kâao lɛ́ɛo jà bpai kâ',
                        'english': 'After I eat, I will go',
                        'breakdown': 'ดิฉัน (I) + กิน (eat) + ข้าว (rice) + แล้ว (after) + จะ (will) + ไป (go) + ค่ะ (polite particle)',
                        'note': 'Completed + Future = sequential actions'
                    }
                ]
            }
        }
    },
    
    'question_patterns': {
        'title': 'Question Formation',
        'explanation': 'Thai questions use the particle มั๊ย (mái) for yes/no and question words for information. '
                       'It is written ไหม in books and on signs, but Thai people say it shorter and higher, '
                       'like มั๊ย, so that is how this app writes it.',
        
        'yes_no': {
            'name': 'Yes/No Questions: มั๊ย (mái)',
            'pattern': 'Statement + มั๊ย + particle',
            'examples': {
                'male': [
                    {
                        'thai': 'คุณกินข้าวมั๊ยครับ',
                        'paiboon': 'kun gin kâao mái kráp',
                        'english': 'Do you eat rice? / Have you eaten?',
                        'breakdown': 'คุณ (you) + กิน (eat) + ข้าว (rice) + มั๊ย (question) + ครับ (polite)'
                    },
                    {
                        'thai': 'คุณพูดไทยได้มั๊ยครับ',
                        'paiboon': 'kun pûut tai dâi mái kráp',
                        'english': 'Can you speak Thai?',
                        'breakdown': 'คุณ (you) + พูด (speak) + ไทย (Thai) + ได้ (can) + มั๊ย (question) + ครับ (polite)'
                    }
                ],
                'female': [
                    {
                        'thai': 'คุณกินข้าวมั๊ยคะ',
                        'paiboon': 'kun gin kâao mái ká',
                        'english': 'Do you eat rice? / Have you eaten?',
                        'breakdown': 'คุณ (you) + กิน (eat) + ข้าว (rice) + มั๊ย (question) + คะ (polite)'
                    },
                    {
                        'thai': 'คุณพูดไทยได้มั๊ยคะ',
                        'paiboon': 'kun pûut tai dâi mái ká',
                        'english': 'Can you speak Thai?',
                        'breakdown': 'คุณ (you) + พูด (speak) + ไทย (Thai) + ได้ (can) + มั๊ย (question) + คะ (polite)'
                    }
                ]
            }
        },
        
        'wh_questions': {
            'name': 'Information Questions: Question Words',
            'pattern': 'Question word replaces the answer',
            'examples': {
                'male': [
                    {
                        'thai': 'คุณชื่ออะไรครับ',
                        'paiboon': 'kun chʉ̂ʉ à-rai kráp',
                        'english': "What's your name?",
                        'breakdown': 'คุณ (you) + ชื่อ (name) + อะไร (what) + ครับ (polite)',
                        'note': 'อะไร (à-rai) = what'
                    },
                    {
                        'thai': 'คุณไปไหนครับ',
                        'paiboon': 'kun bpai nǎi kráp',
                        'english': 'Where are you going?',
                        'breakdown': 'คุณ (you) + ไป (go) + ไหน (where) + ครับ (polite)',
                        'note': 'ไหน (nǎi) = where'
                    },
                    {
                        'thai': 'ทำไมครับ',
                        'paiboon': 'tam-mai kráp',
                        'english': 'Why?',
                        'breakdown': 'ทำไม (why) + ครับ (polite)',
                        'note': 'ทำไม (tam-mai) = why'
                    }
                ],
                'female': [
                    {
                        'thai': 'คุณชื่ออะไรคะ',
                        'paiboon': 'kun chʉ̂ʉ à-rai ká',
                        'english': "What's your name?",
                        'breakdown': 'คุณ (you) + ชื่อ (name) + อะไร (what) + คะ (polite)',
                        'note': 'อะไร (à-rai) = what'
                    },
                    {
                        'thai': 'คุณไปไหนคะ',
                        'paiboon': 'kun bpai nǎi ká',
                        'english': 'Where are you going?',
                        'breakdown': 'คุณ (you) + ไป (go) + ไหน (where) + คะ (polite)',
                        'note': 'ไหน (nǎi) = where'
                    },
                    {
                        'thai': 'ทำไมคะ',
                        'paiboon': 'tam-mai ká',
                        'english': 'Why?',
                        'breakdown': 'ทำไม (why) + คะ (polite)',
                        'note': 'ทำไม (tam-mai) = why'
                    }
                ]
            }
        }
    },

    # How to ANSWER the questions above. The page taught asking ไปมั๊ย but
    # never replying to it, and the reply is where Thai differs most from
    # English: there is no all-purpose "yes" or "no". The bare rules for ไม่
    # live on the Grammar page (Negation); this is them in use, as replies.
    # DRAFT Thai — not yet checked by a native speaker.
    'answering': {
        'title': 'Answering Questions — Yes, No & Not Yet',
        'explanation': 'Thai has no single word for "yes" or "no". You answer by '
                       'repeating the key word from the question — on its own for '
                       'yes, with ไม่ (mâi) in front of it for no.',
        'patterns': [
            {
                'key': 'repeat_verb',
                'name': 'Repeat the verb: ไป → ไป / ไม่ไป',
                'pattern': 'Yes = Verb + particle  ·  No = ไม่ + Verb + particle',
                'tip': 'Whatever word comes before มั๊ย is the word you answer '
                       'with. Women: the question ends in คะ (ká, high tone), the '
                       'answer ends in ค่ะ (kâ, falling tone).',
                'examples': {
                    'male': [
                        {'q': {'thai': 'ไปมั๊ยครับ', 'paiboon': 'bpai mái kráp', 'english': 'Are you going? / Want to go?'},
                         'yes': {'thai': 'ไปครับ', 'paiboon': 'bpai kráp', 'english': 'Yes, I am. (go)'},
                         'no': {'thai': 'ไม่ไปครับ', 'paiboon': 'mâi bpai kráp', 'english': "No, I'm not. (not go)"}},
                        {'q': {'thai': 'คุณพูดไทยได้มั๊ยครับ', 'paiboon': 'kun pûut tai dâi mái kráp', 'english': 'Can you speak Thai?'},
                         'yes': {'thai': 'ได้ครับ', 'paiboon': 'dâi kráp', 'english': 'Yes, I can. (can)'},
                         'no': {'thai': 'ไม่ได้ครับ', 'paiboon': 'mâi dâi kráp', 'english': "No, I can't. (not can)"}},
                        {'q': {'thai': 'เผ็ดมั๊ยครับ', 'paiboon': 'pèt mái kráp', 'english': 'Is it spicy?'},
                         'yes': {'thai': 'เผ็ดครับ', 'paiboon': 'pèt kráp', 'english': "Yes, it is. (spicy)"},
                         'no': {'thai': 'ไม่เผ็ดครับ', 'paiboon': 'mâi pèt kráp', 'english': "No, it isn't. (not spicy)"}},
                    ],
                    'female': [
                        {'q': {'thai': 'ไปมั๊ยคะ', 'paiboon': 'bpai mái ká', 'english': 'Are you going? / Want to go?'},
                         'yes': {'thai': 'ไปค่ะ', 'paiboon': 'bpai kâ', 'english': 'Yes, I am. (go)'},
                         'no': {'thai': 'ไม่ไปค่ะ', 'paiboon': 'mâi bpai kâ', 'english': "No, I'm not. (not go)"}},
                        {'q': {'thai': 'คุณพูดไทยได้มั๊ยคะ', 'paiboon': 'kun pûut tai dâi mái ká', 'english': 'Can you speak Thai?'},
                         'yes': {'thai': 'ได้ค่ะ', 'paiboon': 'dâi kâ', 'english': 'Yes, I can. (can)'},
                         'no': {'thai': 'ไม่ได้ค่ะ', 'paiboon': 'mâi dâi kâ', 'english': "No, I can't. (not can)"}},
                        {'q': {'thai': 'เผ็ดมั๊ยคะ', 'paiboon': 'pèt mái ká', 'english': 'Is it spicy?'},
                         'yes': {'thai': 'เผ็ดค่ะ', 'paiboon': 'pèt kâ', 'english': "Yes, it is. (spicy)"},
                         'no': {'thai': 'ไม่เผ็ดค่ะ', 'paiboon': 'mâi pèt kâ', 'english': "No, it isn't. (not spicy)"}},
                    ],
                },
            },
            {
                'key': 'chai',
                'name': '"Right?" questions: ใช่ / ไม่ใช่',
                'pattern': 'Statement + ใช่มั๊ย  →  ใช่ / ไม่ใช่ + particle',
                'tip': 'ใช่ (châi) means "that\'s right" — use it to confirm a '
                       'fact, not to agree to an action. Answering ไปมั๊ย with ใช่ '
                       'is a classic learner mistake: say ไป.',
                'examples': {
                    'male': [
                        {'q': {'thai': 'นี่ของคุณใช่มั๊ยครับ', 'paiboon': 'nîi kɔ̌ɔŋ kun châi mái kráp', 'english': 'This is yours, right?'},
                         'yes': {'thai': 'ใช่ครับ', 'paiboon': 'châi kráp', 'english': "Yes, that's right."},
                         'no': {'thai': 'ไม่ใช่ครับ', 'paiboon': 'mâi châi kráp', 'english': "No, it isn't."}},
                    ],
                    'female': [
                        {'q': {'thai': 'นี่ของคุณใช่มั๊ยคะ', 'paiboon': 'nîi kɔ̌ɔŋ kun châi mái ká', 'english': 'This is yours, right?'},
                         'yes': {'thai': 'ใช่ค่ะ', 'paiboon': 'châi kâ', 'english': "Yes, that's right."},
                         'no': {'thai': 'ไม่ใช่ค่ะ', 'paiboon': 'mâi châi kâ', 'english': "No, it isn't."}},
                    ],
                },
            },
            {
                'key': 'not_yet',
                'name': 'Already or not yet: แล้ว / ยังไม่',
                'pattern': '…แล้วรึยัง  →  Verb + แล้ว / ยังไม่ + Verb',
                'tip': 'A แล้ว question is never answered with plain ไม่. '
                       'If it hasn\'t happened, it hasn\'t happened YET — ยังไม่ '
                       '(yaŋ mâi). Just ยังครับ / ยังค่ะ on its own also works.',
                'examples': {
                    'male': [
                        {'q': {'thai': 'กินข้าวแล้วรึยังครับ', 'paiboon': 'gin kâao lɛ́ɛo rʉ́ yaŋ kráp', 'english': 'Have you eaten yet?'},
                         'yes': {'thai': 'กินแล้วครับ', 'paiboon': 'gin lɛ́ɛo kráp', 'english': "Yes, I've eaten. (eat already)"},
                         'no': {'thai': 'ยังไม่ได้กินครับ', 'paiboon': 'yaŋ mâi dâi gin kráp', 'english': "Not yet. (still not eaten)"}},
                        {'q': {'thai': 'ถึงแล้วรึยังครับ', 'paiboon': 'tʉ̌ŋ lɛ́ɛo rʉ́ yaŋ kráp', 'english': 'Have we arrived yet?'},
                         'yes': {'thai': 'ถึงแล้วครับ', 'paiboon': 'tʉ̌ŋ lɛ́ɛo kráp', 'english': "Yes, we're here. (arrive already)"},
                         'no': {'thai': 'ยังไม่ถึงครับ', 'paiboon': 'yaŋ mâi tʉ̌ŋ kráp', 'english': "Not yet. (still not arrive)"}},
                    ],
                    'female': [
                        {'q': {'thai': 'กินข้าวแล้วรึยังคะ', 'paiboon': 'gin kâao lɛ́ɛo rʉ́ yaŋ ká', 'english': 'Have you eaten yet?'},
                         'yes': {'thai': 'กินแล้วค่ะ', 'paiboon': 'gin lɛ́ɛo kâ', 'english': "Yes, I've eaten. (eat already)"},
                         'no': {'thai': 'ยังไม่ได้กินค่ะ', 'paiboon': 'yaŋ mâi dâi gin kâ', 'english': "Not yet. (still not eaten)"}},
                        {'q': {'thai': 'ถึงแล้วรึยังคะ', 'paiboon': 'tʉ̌ŋ lɛ́ɛo rʉ́ yaŋ ká', 'english': 'Have we arrived yet?'},
                         'yes': {'thai': 'ถึงแล้วค่ะ', 'paiboon': 'tʉ̌ŋ lɛ́ɛo kâ', 'english': "Yes, we're here. (arrive already)"},
                         'no': {'thai': 'ยังไม่ถึงค่ะ', 'paiboon': 'yaŋ mâi tʉ̌ŋ kâ', 'english': "Not yet. (still not arrive)"}},
                    ],
                },
            },
            {
                'key': 'didnt',
                'name': "Didn't: ไม่ได้ + Verb",
                'pattern': 'ไม่ได้ + Verb = didn\'t …',
                'tip': 'Word order changes the meaning. ไม่ได้ไป (mâi dâi bpai) '
                       '= "didn\'t go". ไปไม่ได้ (bpai mâi dâi) = "can\'t go".',
                'examples': {
                    'male': [
                        {'q': {'thai': 'เมื่อวานไปทำงานมั๊ยครับ', 'paiboon': 'mʉ̂a waan bpai tam ŋaan mái kráp', 'english': 'Did you go to work yesterday?'},
                         'yes': {'thai': 'ไปครับ', 'paiboon': 'bpai kráp', 'english': 'Yes, I did. (go)'},
                         'no': {'thai': 'ไม่ได้ไปครับ', 'paiboon': 'mâi dâi bpai kráp', 'english': "No, I didn't. (didn't go)"}},
                    ],
                    'female': [
                        {'q': {'thai': 'เมื่อวานไปทำงานมั๊ยคะ', 'paiboon': 'mʉ̂a waan bpai tam ŋaan mái ká', 'english': 'Did you go to work yesterday?'},
                         'yes': {'thai': 'ไปค่ะ', 'paiboon': 'bpai kâ', 'english': 'Yes, I did. (go)'},
                         'no': {'thai': 'ไม่ได้ไปค่ะ', 'paiboon': 'mâi dâi bpai kâ', 'english': "No, I didn't. (didn't go)"}},
                    ],
                },
            },
        ],
    },

    # Joining two ideas into one longer sentence — the step after single
    # patterns. DRAFT Thai — not yet checked by a native speaker.
    'joining': {
        'title': 'Joining Ideas — Longer Sentences',
        'explanation': 'Real conversation strings ideas together. These linking words turn two short sentences into one longer one — and Thai keeps the same word order inside each half, so everything above still applies.',
        'patterns': [
            {
                'key': 'but',
                'name': 'แต่ (dtɛ̀ɛ) — but',
                'pattern': 'Idea 1 + แต่ + Idea 2',
                'tip': 'The second half usually drops "I" — Thai doesn\'t repeat what\'s obvious.',
                'examples': {
                    'male': [
                        {'thai': 'ผมอยากไปแต่ไม่มีเวลาครับ', 'paiboon': 'pǒm yàak bpai dtɛ̀ɛ mâi mii wee-laa kráp', 'english': "I want to go, but I don't have time.", 'breakdown': 'ผม (I) + อยาก (want) + ไป (go) + แต่ (but) + ไม่มี (not have) + เวลา (time) + ครับ (polite)'},
                    ],
                    'female': [
                        {'thai': 'ดิฉันอยากไปแต่ไม่มีเวลาค่ะ', 'paiboon': 'dì-chǎn yàak bpai dtɛ̀ɛ mâi mii wee-laa kâ', 'english': "I want to go, but I don't have time.", 'breakdown': 'ดิฉัน (I) + อยาก (want) + ไป (go) + แต่ (but) + ไม่มี (not have) + เวลา (time) + ค่ะ (polite)'},
                    ],
                },
            },
            {
                'key': 'because',
                'name': 'เพราะ (prɔ́) — because',
                'pattern': 'What happens + เพราะ + the reason',
                'tip': 'ไม่สบาย — literally "not comfortable" — is how Thais say they\'re ill.',
                'examples': {
                    'male': [
                        {'thai': 'ผมไม่ไปทำงานเพราะไม่สบายครับ', 'paiboon': 'pǒm mâi bpai tam ŋaan prɔ́ mâi sà-baai kráp', 'english': "I'm not going to work because I'm not well.", 'breakdown': 'ผม (I) + ไม่ไป (not go) + ทำงาน (work) + เพราะ (because) + ไม่สบาย (unwell) + ครับ (polite)'},
                    ],
                    'female': [
                        {'thai': 'ดิฉันไม่ไปทำงานเพราะไม่สบายค่ะ', 'paiboon': 'dì-chǎn mâi bpai tam ŋaan prɔ́ mâi sà-baai kâ', 'english': "I'm not going to work because I'm not well.", 'breakdown': 'ดิฉัน (I) + ไม่ไป (not go) + ทำงาน (work) + เพราะ (because) + ไม่สบาย (unwell) + ค่ะ (polite)'},
                    ],
                },
            },
            {
                'key': 'if',
                'name': 'ถ้า … ก็ (tâa … gɔ̂ɔ) — if … then',
                'pattern': 'ถ้า + condition, (subject) + ก็ + result',
                'tip': 'ก็ goes after the subject of the second half and before its verb: ผมก็จะ…',
                'examples': {
                    'male': [
                        {'thai': 'ถ้าฝนตก ผมก็จะอยู่บ้านครับ', 'paiboon': 'tâa fǒn dtòk pǒm gɔ̂ɔ jà yùu bâan kráp', 'english': "If it rains, I'll stay at home.", 'breakdown': 'ถ้า (if) + ฝนตก (it rains) + ผม (I) + ก็ (then) + จะ (will) + อยู่บ้าน (stay home) + ครับ (polite)'},
                    ],
                    'female': [
                        {'thai': 'ถ้าฝนตก ดิฉันก็จะอยู่บ้านค่ะ', 'paiboon': 'tâa fǒn dtòk dì-chǎn gɔ̂ɔ jà yùu bâan kâ', 'english': "If it rains, I'll stay at home.", 'breakdown': 'ถ้า (if) + ฝนตก (it rains) + ดิฉัน (I) + ก็ (then) + จะ (will) + อยู่บ้าน (stay home) + ค่ะ (polite)'},
                    ],
                },
            },
            {
                'key': 'after',
                'name': 'หลังจาก / ก่อน (lǎŋ-jàak / gɔ̀ɔn) — after / before',
                'pattern': 'Main idea + หลังจาก/ก่อน + the other event — or the other way round',
                'tip': 'Either half can come first. Starting with the time word puts the stress on when.',
                'examples': {
                    'male': [
                        {'thai': 'ผมจะโทรหาคุณหลังจากกินข้าวครับ', 'paiboon': 'pǒm jà too hǎa kun lǎŋ-jàak gin kâao kráp', 'english': "I'll call you after I eat.", 'breakdown': 'ผม (I) + จะ (will) + โทรหา (call) + คุณ (you) + หลังจาก (after) + กินข้าว (eat) + ครับ (polite)'},
                        {'thai': 'ก่อนนอนผมอ่านหนังสือทุกคืนครับ', 'paiboon': 'gɔ̀ɔn nɔɔn pǒm àan nǎŋ-sʉ̌ʉ túk kʉʉn kráp', 'english': 'I read every night before bed.', 'breakdown': 'ก่อน (before) + นอน (sleep) + ผม (I) + อ่านหนังสือ (read) + ทุกคืน (every night) + ครับ (polite)'},
                    ],
                    'female': [
                        {'thai': 'ดิฉันจะโทรหาคุณหลังจากกินข้าวค่ะ', 'paiboon': 'dì-chǎn jà too hǎa kun lǎŋ-jàak gin kâao kâ', 'english': "I'll call you after I eat.", 'breakdown': 'ดิฉัน (I) + จะ (will) + โทรหา (call) + คุณ (you) + หลังจาก (after) + กินข้าว (eat) + ค่ะ (polite)'},
                        {'thai': 'ก่อนนอนดิฉันอ่านหนังสือทุกคืนค่ะ', 'paiboon': 'gɔ̀ɔn nɔɔn dì-chǎn àan nǎŋ-sʉ̌ʉ túk kʉʉn kâ', 'english': 'I read every night before bed.', 'breakdown': 'ก่อน (before) + นอน (sleep) + ดิฉัน (I) + อ่านหนังสือ (read) + ทุกคืน (every night) + ค่ะ (polite)'},
                    ],
                },
            },
            {
                'key': 'when',
                'name': 'ตอนที่ (dtɔɔn-tîi) — when',
                'pattern': 'ตอนที่ + situation, then what happened',
                'tip': 'There is no past tense — ตอนที่ already tells the listener when.',
                'examples': {
                    'male': [
                        {'thai': 'ตอนที่ผมอยู่เมืองไทย ผมเรียนภาษาไทยทุกวันครับ', 'paiboon': 'dtɔɔn-tîi pǒm yùu mʉaŋ-tai pǒm rian paa-sǎa tai túk wan kráp', 'english': 'When I was in Thailand, I studied Thai every day.', 'breakdown': 'ตอนที่ (when) + ผมอยู่เมืองไทย (I was in Thailand) + ผมเรียนภาษาไทย (I studied Thai) + ทุกวัน (every day) + ครับ (polite)'},
                    ],
                    'female': [
                        {'thai': 'ตอนที่ดิฉันอยู่เมืองไทย ดิฉันเรียนภาษาไทยทุกวันค่ะ', 'paiboon': 'dtɔɔn-tîi dì-chǎn yùu mʉaŋ-tai dì-chǎn rian paa-sǎa tai túk wan kâ', 'english': 'When I was in Thailand, I studied Thai every day.', 'breakdown': 'ตอนที่ (when) + ดิฉันอยู่เมืองไทย (I was in Thailand) + ดิฉันเรียนภาษาไทย (I studied Thai) + ทุกวัน (every day) + ค่ะ (polite)'},
                    ],
                },
            },
            {
                'key': 'that_which',
                'name': 'ที่ (tîi) — that / which / who',
                'pattern': 'Noun + ที่ + description',
                'tip': 'The noun comes first, then ที่ and everything that describes it — the opposite of English adjectives.',
                'examples': {
                    'male': [
                        {'thai': 'ร้านที่เราไปเมื่อวานอร่อยมากครับ', 'paiboon': 'ráan tîi rao bpai mʉ̂a waan à-rɔ̀i mâak kráp', 'english': 'The restaurant we went to yesterday was really good.', 'breakdown': 'ร้าน (restaurant) + ที่ (that) + เราไปเมื่อวาน (we went yesterday) + อร่อยมาก (very tasty) + ครับ (polite)'},
                    ],
                    'female': [
                        {'thai': 'ร้านที่เราไปเมื่อวานอร่อยมากค่ะ', 'paiboon': 'ráan tîi rao bpai mʉ̂a waan à-rɔ̀i mâak kâ', 'english': 'The restaurant we went to yesterday was really good.', 'breakdown': 'ร้าน (restaurant) + ที่ (that) + เราไปเมื่อวาน (we went yesterday) + อร่อยมาก (very tasty) + ค่ะ (polite)'},
                    ],
                },
            },
            {
                'key': 'think_say',
                'name': 'ว่า (wâa) — that (after think / say / know)',
                'pattern': 'คิด / บอก / รู้ + ว่า + what',
                'tip': 'ว่า follows verbs of thinking and saying: คิดว่า (think that), บอกว่า (said that), รู้ว่า (know that).',
                'examples': {
                    'male': [
                        {'thai': 'ผมคิดว่าพรุ่งนี้ฝนจะตกครับ', 'paiboon': 'pǒm kít wâa prûŋ níi fǒn jà dtòk kráp', 'english': 'I think it will rain tomorrow.', 'breakdown': 'ผม (I) + คิด (think) + ว่า (that) + พรุ่งนี้ (tomorrow) + ฝนจะตก (it will rain) + ครับ (polite)'},
                    ],
                    'female': [
                        {'thai': 'ดิฉันคิดว่าพรุ่งนี้ฝนจะตกค่ะ', 'paiboon': 'dì-chǎn kít wâa prûŋ níi fǒn jà dtòk kâ', 'english': 'I think it will rain tomorrow.', 'breakdown': 'ดิฉัน (I) + คิด (think) + ว่า (that) + พรุ่งนี้ (tomorrow) + ฝนจะตก (it will rain) + ค่ะ (polite)'},
                    ],
                },
            },
        ],
    },

    'common_verbs': {
        'title': 'Essential Verbs in Context',
        'explanation': 'Practice common verbs with aspect markers',
        'verbs': [
            {
                'verb': 'ไป (bpai) - go',
                'present': {'thai': 'ไป', 'paiboon': 'bpai'},
                'progressive': {'thai': 'กำลังไป', 'paiboon': 'gam-laŋ bpai', 'english': 'am/is/are going'},
                'completed': {'thai': 'ไปแล้ว', 'paiboon': 'bpai lɛ́ɛo', 'english': 'already went / have gone'},
                'future': {'thai': 'จะไป', 'paiboon': 'jà bpai', 'english': 'will go'}
            },
            {
                'verb': 'มา (maa) - come',
                'present': {'thai': 'มา', 'paiboon': 'maa'},
                'progressive': {'thai': 'กำลังมา', 'paiboon': 'gam-laŋ maa', 'english': 'am/is/are coming'},
                'completed': {'thai': 'มาแล้ว', 'paiboon': 'maa lɛ́ɛo', 'english': 'already came / have come'},
                'future': {'thai': 'จะมา', 'paiboon': 'jà maa', 'english': 'will come'}
            },
            {
                'verb': 'กิน (gin) - eat',
                'present': {'thai': 'กิน', 'paiboon': 'gin'},
                'progressive': {'thai': 'กำลังกิน', 'paiboon': 'gam-laŋ gin', 'english': 'am/is/are eating'},
                'completed': {'thai': 'กินแล้ว', 'paiboon': 'gin lɛ́ɛo', 'english': 'already ate / have eaten'},
                'future': {'thai': 'จะกิน', 'paiboon': 'jà gin', 'english': 'will eat'}
            },
            {
                'verb': 'ทำงาน (tam ŋaan) - work',
                'present': {'thai': 'ทำงาน', 'paiboon': 'tam ŋaan'},
                'progressive': {'thai': 'กำลังทำงาน', 'paiboon': 'gam-laŋ tam ŋaan', 'english': 'am/is/are working'},
                'completed': {'thai': 'ทำงานแล้ว', 'paiboon': 'tam ŋaan lɛ́ɛo', 'english': 'already worked / have worked'},
                'future': {'thai': 'จะทำงาน', 'paiboon': 'jà tam ŋaan', 'english': 'will work'}
            },
            {
                'verb': 'เรียน (rian) - study',
                'present': {'thai': 'เรียน', 'paiboon': 'rian'},
                'progressive': {'thai': 'กำลังเรียน', 'paiboon': 'gam-laŋ rian', 'english': 'am/is/are studying'},
                'completed': {'thai': 'เรียนแล้ว', 'paiboon': 'rian lɛ́ɛo', 'english': 'already studied / have studied'},
                'future': {'thai': 'จะเรียน', 'paiboon': 'jà rian', 'english': 'will study'}
            }
        ]
    }
}


CONVERSATIONS = {
    'restaurant': {
        'title': 'At a Restaurant (ที่ร้านอาหาร)',
        'setting': 'Ordering food at a Thai restaurant',
        'difficulty': 'beginner',
        'dialogue': [
            {
                'speaker': 'waiter',
                'thai': 'สวัสดีครับ รับอะไรดีครับ',
                'paiboon': 'sà-wàt-dii kráp, ráp à-rai dii kráp',
                'english': 'Hello, what would you like to order?',
                'note': 'Waiter greeting'
            },
            {
                'speaker': 'customer_male',
                'thai': 'ผมขอข้าวผัดหนึ่งจานครับ',
                'paiboon': 'pǒm kɔ̌ɔ kâao pàt nʉ̀ŋ jaan kráp',
                'english': "I'd like one fried rice please",
                'note': 'Male customer ordering'
            },
            {
                'speaker': 'customer_female',
                'thai': 'ดิฉันขอส้มตำค่ะ',
                'paiboon': 'dì-chǎn kɔ̌ɔ sôm-tam kâ',
                'english': "I'd like papaya salad please",
                'note': 'Female customer ordering'
            },
            {
                'speaker': 'waiter',
                'thai': 'เผ็ดมั๊ยครับ',
                'paiboon': 'pèt mái kráp',
                'english': 'Spicy?',
                'note': 'Asking about spice level'
            },
            {
                'speaker': 'customer_female',
                'thai': 'ไม่เผ็ดค่ะ',
                'paiboon': 'mâi pèt kâ',
                'english': 'Not spicy please',
                'note': 'Declining spice'
            },
            {
                'speaker': 'waiter',
                'thai': 'รับน้ำอะไรครับ',
                'paiboon': 'ráp náam à-rai kráp',
                'english': 'What would you like to drink?',
                'note': 'Asking about beverages'
            },
            {
                'speaker': 'customer_male',
                'thai': 'เอาน้ำเปล่าครับ',
                'paiboon': 'ao náam bplào kráp',
                'english': "I'll have water",
                'note': 'Ordering water'
            }
        ]
    },
    
    'meeting': {
        'title': 'Meeting Someone (การพบปะ)',
        'setting': 'First time meeting someone',
        'difficulty': 'beginner',
        'dialogue': [
            {
                'speaker': 'person1_male',
                'thai': 'สวัสดีครับ ผมชื่อจอห์น',
                'paiboon': 'sà-wàt-dii kráp, pǒm chʉ̂ʉ John',
                'english': "Hello, I'm John",
                'note': 'Male introduction'
            },
            {
                'speaker': 'person2_female',
                'thai': 'สวัสดีค่ะ ดิฉันชื่อนิดา ยินดีที่ได้รู้จักค่ะ',
                'paiboon': 'sà-wàt-dii kâ, dì-chǎn chʉ̂ʉ Nida, yin-dii tîi dâi rúu-jàk kâ',
                'english': "Hello, I'm Nida, nice to meet you",
                'note': 'Female introduction'
            },
            {
                'speaker': 'person1_male',
                'thai': 'ยินดีที่ได้รู้จักเช่นกันครับ คุณมาจากไหนครับ',
                'paiboon': 'yin-dii tîi dâi rúu-jàk chên-gan kráp, kun maa jàak nǎi kráp',
                'english': 'Nice to meet you too. Where are you from?',
                'note': 'Asking origin'
            },
            {
                'speaker': 'person2_female',
                'thai': 'ดิฉันมาจากกรุงเทพค่ะ แล้วคุณล่ะคะ',
                'paiboon': 'dì-chǎn maa jàak gruŋ-têep kâ, lɛ́ɛo kun lâ ká',
                'english': "I'm from Bangkok. And you?",
                'note': 'Responding and asking back'
            },
            {
                'speaker': 'person1_male',
                'thai': 'ผมมาจากอเมริกาครับ',
                'paiboon': 'pǒm maa jàak à-mee-rí-gaa kráp',
                'english': "I'm from America",
                'note': 'Country name'
            },
            {
                'speaker': 'person2_female',
                'thai': 'คุณพูดไทยเก่งมากเลยค่ะ',
                'paiboon': 'kun pûut tai gèŋ mâak ləəi kâ',
                'english': 'You speak Thai very well!',
                'note': 'Compliment'
            },
            {
                'speaker': 'person1_male',
                'thai': 'ขอบคุณครับ ผมกำลังเรียนอยู่ครับ',
                'paiboon': 'kɔ̀ɔp-kun kráp, pǒm gam-laŋ rian yùu kráp',
                'english': "Thank you, I'm still learning",
                'note': 'Using progressive + อยู่'
            }
        ]
    },
    
    'shopping': {
        'title': 'Shopping (การซื้อของ)',
        'setting': 'Buying something at a market',
        'difficulty': 'intermediate',
        'dialogue': [
            {
                'speaker': 'customer_female',
                'thai': 'ขอดูเสื้อตัวนี้หน่อยค่ะ',
                'paiboon': 'kɔ̌ɔ duu sʉ̂a dtua níi nɔ̀ɔi kâ',
                'english': 'Can I see this shirt please?',
                'note': 'Polite request with หน่อย'
            },
            {
                'speaker': 'seller',
                'thai': 'ได้ครับ ขนาดอะไรครับ',
                'paiboon': 'dâi kráp, kà-nàat à-rai kráp',
                'english': 'Sure, what size?',
                'note': 'Asking about size'
            },
            {
                'speaker': 'customer_female',
                'thai': 'ขนาดเอ็มค่ะ ราคาเท่าไหร่คะ',
                'paiboon': 'kà-nàat M kâ, raa-kaa tâo-rài ká',
                'english': 'Size M. How much is it?',
                'note': 'Asking price'
            },
            {
                'speaker': 'seller',
                'thai': 'สามร้อยบาทครับ',
                'paiboon': 'sǎam rɔ́ɔi bàat kráp',
                'english': '300 baht',
                'note': 'Price'
            },
            {
                'speaker': 'customer_female',
                'thai': 'แพงไปหน่อยค่ะ ลดได้มั๊ยคะ',
                'paiboon': 'pɛɛŋ bpai nɔ̀ɔi kâ, lót dâi mái ká',
                'english': "It's a bit expensive. Can you reduce the price?",
                'note': 'Negotiating'
            },
            {
                'speaker': 'seller',
                'thai': 'ลดให้สองร้อยห้าสิบบาทครับ',
                'paiboon': 'lót hâi sɔ̌ɔŋ rɔ́ɔi hâa-sìp bàat kráp',
                'english': "I'll reduce it to 250 baht",
                'note': 'Counter offer'
            },
            {
                'speaker': 'customer_female',
                'thai': 'โอเคค่ะ เอาค่ะ',
                'paiboon': 'oo-kee kâ, ao kâ',
                'english': "OK, I'll take it",
                'note': 'Accepting'
            }
        ]
    },
    
    'directions': {
        'title': 'Asking for Directions (ถามทาง)',
        'setting': 'Getting directions to a place',
        'difficulty': 'intermediate',
        'dialogue': [
            {
                'speaker': 'tourist_male',
                'thai': 'ขอโทษครับ วัดพระแก้วอยู่ที่ไหนครับ',
                'paiboon': 'kɔ̌ɔ-tôot kráp, wát prá-gɛ̂ɛo yùu tîi-nǎi kráp',
                'english': 'Excuse me, where is Wat Phra Kaew?',
                'note': 'Polite question'
            },
            {
                'speaker': 'local',
                'thai': 'ตรงไปแล้วเลี้ยวซ้ายครับ',
                'paiboon': 'dtroŋ bpai lɛ́ɛo líao sáai kráp',
                'english': 'Go straight then turn left',
                'note': 'Giving directions'
            },
            {
                'speaker': 'tourist_male',
                'thai': 'ไกลมั๊ยครับ',
                'paiboon': 'glai mái kráp',
                'english': 'Is it far?',
                'note': 'Asking about distance'
            },
            {
                'speaker': 'local',
                'thai': 'ไม่ไกลครับ เดินประมาณสิบนาทีครับ',
                'paiboon': 'mâi glai kráp, dəən bprà-maan sìp naa-tii kráp',
                'english': "Not far, about 10 minutes walk",
                'note': 'Time estimate'
            },
            {
                'speaker': 'tourist_male',
                'thai': 'ขอบคุณมากครับ',
                'paiboon': 'kɔ̀ɔp-kun mâak kráp',
                'english': 'Thank you very much',
                'note': 'Thanking'
            },
            {
                'speaker': 'local',
                'thai': 'ไม่เป็นไรครับ',
                'paiboon': 'mâi bpen rai kráp',
                'english': "You're welcome / No problem",
                'note': 'Standard response'
            }
        ]
    },
    
    'daily_routine': {
        'title': 'Daily Routine (กิจวัตรประจำวัน)',
        'setting': 'Talking about your day',
        'difficulty': 'intermediate',
        'dialogue': [
            {
                'speaker': 'friend1_male',
                'thai': 'เช้านี้คุณทำอะไรครับ',
                'paiboon': 'cháao níi kun tam à-rai kráp',
                'english': 'What did you do this morning?',
                'note': 'Past question'
            },
            {
                'speaker': 'friend2_female',
                'thai': 'ดิฉันไปออกกำลังกายค่ะ แล้วคุณล่ะคะ',
                'paiboon': 'dì-chǎn bpai ɔ̀ɔk gam-laŋ gaai kâ, lɛ́ɛo kun lâ ká',
                'english': 'I went to exercise. And you?',
                'note': 'Past completed + asking back'
            },
            {
                'speaker': 'friend1_male',
                'thai': 'ผมยังไม่ได้ไปครับ ผมกำลังจะไปตอนเย็นครับ',
                'paiboon': 'pǒm yaŋ mâi dâi bpai kráp, pǒm gam-laŋ jà bpai dtɔɔn yen kráp',
                'english': "I haven't gone yet. I'm going to go in the evening",
                'note': 'Negative + progressive future'
            },
            {
                'speaker': 'friend2_female',
                'thai': 'ตอนนี้คุณกำลังทำอะไรอยู่คะ',
                'paiboon': 'dtɔɔn níi kun gam-laŋ tam à-rai yùu ká',
                'english': 'What are you doing now?',
                'note': 'Progressive with อยู่'
            },
            {
                'speaker': 'friend1_male',
                'thai': 'ผมกำลังทำงานอยู่ครับ แล้วเดี๋ยวจะไปกินข้าวครับ',
                'paiboon': 'pǒm gam-laŋ tam ŋaan yùu kráp, lɛ́ɛo dǐao jà bpai gin kâao kráp',
                'english': "I'm working now, then I'll go eat soon",
                'note': 'Progressive + future'
            },
            {
                'speaker': 'friend2_female',
                'thai': 'ไปกินด้วยกันมั๊ยคะ',
                'paiboon': 'bpai gin dûai gan mái ká',
                'english': 'Want to eat together?',
                'note': 'Invitation'
            },
            {
                'speaker': 'friend1_male',
                'thai': 'ได้ครับ ไปกันเลยครับ',
                'paiboon': 'dâi kráp, bpai gan ləəi kráp',
                'english': "Sure, let's go!",
                'note': 'Accepting + suggesting action'
            }
        ]
    },

    # ── Phase 2 additions (2026-07-23) — DRAFT Thai, pending native-speaker
    # review (esp. the Dhamma dialogues' monastic register). ────────────────
    'taxi': {
        'title': 'Taking a Taxi (นั่งแท็กซี่)',
        'setting': 'Getting a taxi to a destination and paying by the meter',
        'difficulty': 'beginner',
        'dialogue': [
            {'speaker': 'passenger_male', 'thai': 'ไปสยามพารากอนครับ', 'paiboon': 'bpai sà-yǎam paa-raa-gɔɔn kráp', 'english': 'To Siam Paragon, please.', 'note': 'Stating the destination'},
            {'speaker': 'driver_male', 'thai': 'ได้ครับ เชิญขึ้นเลยครับ', 'paiboon': 'dâi kráp, chəən kʉ̂n ləəi kráp', 'english': 'Sure, please get in.', 'note': 'เชิญ = please (inviting)'},
            {'speaker': 'passenger_male', 'thai': 'ใช้มิเตอร์ได้มั๊ยครับ', 'paiboon': 'chái mí-təə dâi mái kráp', 'english': 'Can you use the meter?', 'note': 'Helps get a fair fare'},
            {'speaker': 'driver_male', 'thai': 'ได้ครับ รถติดนิดหน่อยนะครับ', 'paiboon': 'dâi kráp, rót tìt nít-nɔ̀i ná kráp', 'english': "Sure. There's a bit of traffic.", 'note': 'รถติด = traffic jam'},
            {'speaker': 'passenger_male', 'thai': 'ไม่เป็นไรครับ จอดตรงนี้ได้มั๊ยครับ', 'paiboon': 'mâi bpen rai kráp, jɔ̀ɔt dtroŋ níi dâi mái kráp', 'english': "It's fine. Can you stop right here?", 'note': 'จอด = to stop/park'},
            {'speaker': 'passenger_male', 'thai': 'เท่าไหร่ครับ', 'paiboon': 'tâo-rài kráp', 'english': 'How much is it?', 'note': ''},
            {'speaker': 'driver_male', 'thai': 'เก้าสิบบาทครับ', 'paiboon': 'gâo-sìp bàat kráp', 'english': 'Ninety baht.', 'note': ''}
        ]
    },

    'market': {
        'title': 'Bargaining at the Market (ต่อราคาที่ตลาด)',
        'setting': 'Haggling politely for a better price',
        'difficulty': 'intermediate',
        'dialogue': [
            {'speaker': 'customer_female', 'thai': 'อันนี้เท่าไหร่คะ', 'paiboon': 'an níi tâo-rài ká', 'english': 'How much is this one?', 'note': 'อันนี้ = this one'},
            {'speaker': 'vendor_male', 'thai': 'สองร้อยบาทครับ', 'paiboon': 'sɔ̌ɔŋ rɔ́ɔi bàat kráp', 'english': 'Two hundred baht.', 'note': ''},
            {'speaker': 'customer_female', 'thai': 'แพงไปหน่อยค่ะ ลดได้มั๊ยคะ', 'paiboon': 'pɛɛŋ bpai nɔ̀ɔi kâ, lót dâi mái ká', 'english': "It's a bit expensive. Can you lower it?", 'note': 'ลด = to reduce the price'},
            {'speaker': 'vendor_male', 'thai': 'ลดให้ห้าสิบ เหลือร้อยห้าสิบครับ', 'paiboon': 'lót hâi hâa-sìp, lʉ̌a rɔ́ɔi hâa-sìp kráp', 'english': "I'll take off fifty — a hundred and fifty.", 'note': 'เหลือ = leaving (remaining)'},
            {'speaker': 'customer_female', 'thai': 'ร้อยยี่สิบได้มั๊ยคะ', 'paiboon': 'rɔ́ɔi yîi-sìp dâi mái ká', 'english': 'Could you do a hundred and twenty?', 'note': 'A counter-offer'},
            {'speaker': 'vendor_male', 'thai': 'ได้ครับ เอาไปเลย', 'paiboon': 'dâi kráp, ao bpai ləəi', 'english': "Alright, it's yours.", 'note': 'Agreeing to the deal'}
        ]
    },

    'temple_visit': {
        'title': 'Visiting a Temple (ไปวัด)',
        'setting': 'Asking about temple etiquette before going in',
        'difficulty': 'beginner',
        'dialogue': [
            {'speaker': 'visitor_female', 'thai': 'ขอโทษค่ะ ต้องถอดรองเท้ามั๊ยคะ', 'paiboon': 'kɔ̌ɔ-tôot kâ, dtɔ̂ŋ tɔ̀ɔt rɔɔŋ-táao mái ká', 'english': 'Excuse me, do I need to take off my shoes?', 'note': 'ถอดรองเท้า = remove shoes'},
            {'speaker': 'attendant_male', 'thai': 'ต้องถอดครับ ก่อนเข้าในโบสถ์', 'paiboon': 'dtɔ̂ŋ tɔ̀ɔt kráp, gɔ̀ɔn kâo nai bòot', 'english': 'Yes, before entering the ordination hall.', 'note': 'โบสถ์ = the ubosot (ordination hall)'},
            {'speaker': 'visitor_female', 'thai': 'แต่งตัวแบบนี้เข้าได้มั๊ยคะ', 'paiboon': 'tɛ̀ŋ-tua bɛ̀ɛp níi kâo dâi mái ká', 'english': 'Is it ok to go in dressed like this?', 'note': 'Asking about the dress code'},
            {'speaker': 'attendant_male', 'thai': 'ควรปิดไหล่กับหัวเข่าครับ', 'paiboon': 'kuan bpìt lài gàp hǔa-kào kráp', 'english': 'You should cover your shoulders and knees.', 'note': 'Temple dress etiquette'},
            {'speaker': 'visitor_female', 'thai': 'ถ่ายรูปได้มั๊ยคะ', 'paiboon': 'tàai-rûup dâi mái ká', 'english': 'Can I take photos?', 'note': ''},
            {'speaker': 'attendant_male', 'thai': 'ได้ครับ แต่อย่าหันหลังให้พระพุทธรูป', 'paiboon': 'dâi kráp, tɛ̀ɛ yàa hǎn lǎŋ hâi prá-pút-tá-rûup', 'english': "Yes, but don't turn your back to the Buddha image.", 'note': 'Showing respect to the Buddha image'}
        ]
    },

    'offering_alms': {
        'title': 'Offering Alms (ตักบาตร)',
        'setting': 'Offering food to a monk on his morning alms round',
        'difficulty': 'beginner',
        'dialogue': [
            {'speaker': 'layperson_female', 'thai': 'นิมนต์ค่ะ', 'paiboon': 'ní-mon kâ', 'english': 'Please receive (inviting the monk).', 'note': 'นิมนต์ = the respectful word for inviting a monk'},
            {'speaker': 'layperson_female', 'thai': 'ดิฉันขอถวายอาหารค่ะ', 'paiboon': 'dì-chǎn kɔ̌ɔ tà-wǎai aa-hǎan kâ', 'english': 'I would like to offer food.', 'note': 'ถวาย = to offer (to a monk)'},
            {'speaker': 'monk', 'thai': 'เจริญพร', 'paiboon': 'jà-rəən-pɔɔn', 'english': 'Blessings.', 'note': 'A monk answers with เจริญพร, not ครับ/ค่ะ'},
            {'speaker': 'layperson_female', 'thai': 'ขอให้พระอาจารย์สุขภาพแข็งแรงค่ะ', 'paiboon': 'kɔ̌ɔ hâi prá aa-jaan sùk-kà-pâap kɛ̌ŋ-rɛɛŋ kâ', 'english': 'May you be in good health, Ajahn.', 'note': 'A good wish while offering'},
            {'speaker': 'monk', 'thai': 'ขอให้โยมมีความสุข มีอายุยืน', 'paiboon': 'kɔ̌ɔ hâi yoom mii kwaam-sùk, mii aa-yú yʉʉn', 'english': 'May you be happy and live long.', 'note': "The monk's blessing in return; โยม = layperson"}
        ]
    },

    'learning_meditation': {
        'title': 'Learning Meditation from a Monk (เรียนสมาธิกับพระ)',
        'setting': 'A layperson respectfully asks a monk how to begin meditating',
        'difficulty': 'intermediate',
        'dialogue': [
            {'speaker': 'layperson_male', 'thai': 'กราบนมัสการครับ พระอาจารย์', 'paiboon': 'gràap ná-mát-sà-gaan kráp, prá aa-jaan', 'english': 'I pay respect, Ajahn.', 'note': 'Greeting a monk — not สวัสดี'},
            {'speaker': 'monk', 'thai': 'เจริญพร โยม', 'paiboon': 'jà-rəən-pɔɔn, yoom', 'english': 'Blessings, layperson.', 'note': 'โยม = how a monk addresses a lay person'},
            {'speaker': 'layperson_male', 'thai': 'ผมอยากเริ่มนั่งสมาธิครับ ควรเริ่มยังไงดีครับ', 'paiboon': 'pǒm yàak rə̂əm nâŋ sà-maa-tí kráp, kuan rə̂əm yaŋ-ŋai dii kráp', 'english': 'I would like to start meditating. How should I begin?', 'note': 'นั่งสมาธิ = to meditate'},
            {'speaker': 'monk', 'thai': 'เริ่มจากลมหายใจ หายใจเข้าก็รู้ หายใจออกก็รู้', 'paiboon': 'rə̂əm jàak lom hǎai-jai, hǎai-jai kâo gɔ̂ɔ rúu, hǎai-jai ɔ̀ɔk gɔ̂ɔ rúu', 'english': 'Begin with the breath. Breathing in, know it; breathing out, know it.', 'note': 'Mindfulness of breathing (ānāpānasati)'},
            {'speaker': 'layperson_male', 'thai': 'ต้องนั่งนานมั๊ยครับ', 'paiboon': 'dtɔ̂ŋ nâŋ naan mái kráp', 'english': 'Do I need to sit for long?', 'note': 'Yes/no question'},
            {'speaker': 'monk', 'thai': 'เริ่มจากสิบนาทีก่อน แล้วค่อยๆ เพิ่มขึ้น', 'paiboon': 'rə̂əm jàak sìp naa-tii gɔ̀ɔn, lɛ́ɛo kɔ̂i-kɔ̂i pə̂əm kʉ̂n', 'english': 'Start with ten minutes, then gradually increase.', 'note': 'ค่อยๆ = gradually'}
        ]
    }
}


# The "glue" of real conversation — the phrases textbooks skip that keep talk
# moving when you don't catch every word. Grouped for the Sentences page.
# DRAFT Thai (2026-07-23), pending native-speaker review. Particles shown with
# ครับ (male speaker); a female speaker swaps ครับ -> ค่ะ, as the first group notes.
CONVERSATIONAL_PHRASES = [
    {
        'title': 'Keep the conversation going',
        'icon': '💬',
        'intro': "When you miss something, these keep you in the conversation instead of freezing up.",
        'phrases': [
            {'thai': 'พูดอีกทีได้มั๊ยครับ', 'paiboon': 'pûut ìik tii dâi mái kráp', 'english': 'Could you say that again?'},
            {'thai': 'พูดช้าๆ ได้มั๊ยครับ', 'paiboon': 'pûut cháa-cháa dâi mái kráp', 'english': 'Could you speak slowly?'},
            {'thai': 'ผมยังไม่เข้าใจครับ', 'paiboon': 'pǒm yaŋ mâi kâo-jai kráp', 'english': "I don't understand yet."},
            {'thai': 'อ๋อ เข้าใจแล้วครับ', 'paiboon': 'ɔ̌ɔ, kâo-jai lɛ́ɛo kráp', 'english': 'Oh, I understand now.'},
            {'thai': 'อันนี้ภาษาไทยพูดว่าอะไรครับ', 'paiboon': 'an níi paa-sǎa tai pûut wâa à-rai kráp', 'english': 'How do you say this in Thai?'},
            {'thai': 'คำนี้แปลว่าอะไรครับ', 'paiboon': 'kam níi bplɛɛ wâa à-rai kráp', 'english': 'What does this word mean?'}
        ]
    },
    {
        'title': 'Buying a little time',
        'icon': '⏳',
        'intro': 'Natural fillers give you a moment to think — they sound far less awkward than silence.',
        'phrases': [
            {'thai': 'เอ่อ...', 'paiboon': 'ə̀ə...', 'english': 'Er… / Um…'},
            {'thai': 'คือว่า...', 'paiboon': 'kʉʉ wâa...', 'english': 'The thing is… / Well…'},
            {'thai': 'แบบว่า...', 'paiboon': 'bɛ̀ɛp wâa...', 'english': 'Like… / Sort of…'},
            {'thai': 'เดี๋ยวนะครับ', 'paiboon': 'dǐao ná kráp', 'english': 'Hold on a second.'},
            {'thai': 'ขอคิดแป๊บนึงครับ', 'paiboon': 'kɔ̌ɔ kít bpɛ́p nʉ̀ŋ kráp', 'english': 'Let me think for a moment.'}
        ]
    },
    {
        'title': 'Reacting & agreeing',
        'icon': '👍',
        'intro': 'Small responses that show you are listening and keep the other person talking.',
        'phrases': [
            {'thai': 'จริงเหรอครับ', 'paiboon': 'jiŋ rə̌ə kráp', 'english': 'Really?'},
            {'thai': 'โอเคครับ', 'paiboon': 'oo-kee kráp', 'english': 'Ok.'},
            {'thai': 'ได้เลยครับ', 'paiboon': 'dâi ləəi kráp', 'english': 'Sure / No problem.'},
            {'thai': 'เยี่ยมเลยครับ', 'paiboon': 'yîam ləəi kráp', 'english': 'Great!'},
            {'thai': 'น่าสนใจนะครับ', 'paiboon': 'nâa-sǒn-jai ná kráp', 'english': "That's interesting."}
        ]
    },
    {
        'title': 'Being polite',
        'icon': '🙏',
        'intro': 'The particle ครับ (men) / ค่ะ (women) ends almost every polite sentence; these soften any request.',
        'phrases': [
            {'thai': 'ขอโทษครับ', 'paiboon': 'kɔ̌ɔ-tôot kráp', 'english': 'Excuse me / Sorry.'},
            {'thai': 'ไม่เป็นไรครับ', 'paiboon': 'mâi bpen rai kráp', 'english': "It's ok / No worries."},
            {'thai': 'ขอบคุณมากครับ', 'paiboon': 'kɔ̀ɔp-kun mâak kráp', 'english': 'Thank you very much.'},
            {'thai': 'รบกวนหน่อยครับ', 'paiboon': 'róp-guan nɔ̀i kráp', 'english': 'Sorry to trouble you… (before a request)'}
        ]
    }
]
