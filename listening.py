"""Listening comprehension questions for the Sentences page conversations.

The 🎧 Listen & answer mode hides a conversation's text, plays it line by line,
then asks these questions. They are in English on purpose: the test is whether
the learner understood what they HEARD, not whether they can read the answer
off the page.

Every question is answerable from the audio alone, and the right answer is
always something actually said in the dialogue (sentence_content.CONVERSATIONS).
The wrong options are plausible for the setting but are not said, so a learner
who caught the key word can tell them apart.

⚠️ Waiting for native-speaker review: the questions and answers are checked
against the English glosses in CONVERSATIONS, which are themselves part of the
review. A correction to a line's meaning may change a question here too.
"""

# conversation id (a key of sentence_content.CONVERSATIONS) -> its questions.
# 'answer' is the right option; 'wrong' are the three distractors.
QUESTIONS = {
    'restaurant': [
        {'question': 'What does the man order?',
         'answer': 'One plate of fried rice',
         'wrong': ['Papaya salad', 'A bowl of noodle soup', 'Green curry with rice']},
        {'question': 'How does the woman want her papaya salad?',
         'answer': 'Not spicy',
         'wrong': ['Very spicy', 'With extra lime', 'Without peanuts']},
        {'question': 'What does the man have to drink?',
         'answer': 'Plain water',
         'wrong': ['Iced tea', 'A beer', 'Orange juice']},
    ],
    'meeting': [
        {'question': "What is the woman's name?",
         'answer': 'Nida',
         'wrong': ['Nok', 'Malee', 'Ploy']},
        {'question': 'Where is the woman from?',
         'answer': 'Bangkok',
         'wrong': ['Chiang Mai', 'Phuket', 'America']},
        {'question': 'What does John say about his Thai?',
         'answer': "He's still learning",
         'wrong': ["He's fluent", 'He learned it at school', 'He only speaks a little English']},
    ],
    'shopping': [
        {'question': 'What does the customer want to look at?',
         'answer': 'A shirt',
         'wrong': ['A pair of shoes', 'A bag', 'A hat']},
        {'question': 'What size does she ask for?',
         'answer': 'M',
         'wrong': ['S', 'L', 'XL']},
        {'question': 'What price do they agree on?',
         'answer': '250 baht',
         'wrong': ['300 baht', '200 baht', '150 baht']},
    ],
    'directions': [
        {'question': 'Where does the tourist want to go?',
         'answer': 'Wat Phra Kaew',
         'wrong': ['Wat Arun', 'The railway station', 'The Grand Palace hotel']},
        {'question': 'Which way should he go?',
         'answer': 'Straight on, then turn left',
         'wrong': ['Straight on, then turn right', 'Turn left, then go back', 'Take a taxi']},
        {'question': 'How far is it?',
         'answer': 'About 10 minutes on foot',
         'wrong': ['About an hour on foot', 'Two minutes by car', 'Very far away']},
    ],
    'daily_routine': [
        {'question': 'What did the woman do this morning?',
         'answer': 'She went to exercise',
         'wrong': ['She went to work', 'She went to the market', 'She stayed at home']},
        {'question': 'When is the man going to exercise?',
         'answer': 'This evening',
         'wrong': ['Tomorrow morning', 'He already went', 'At the weekend']},
        {'question': 'What do they decide to do together?',
         'answer': 'Go and eat',
         'wrong': ['Go to the gym', 'Go shopping', 'Go to work']},
    ],
    'taxi': [
        {'question': 'Where is the passenger going?',
         'answer': 'Siam Paragon',
         'wrong': ['The airport', 'Khao San Road', 'Chatuchak Market']},
        {'question': 'What does the passenger ask the driver to use?',
         'answer': 'The meter',
         'wrong': ['The motorway', 'The air conditioning', 'A map']},
        {'question': 'How much is the fare?',
         'answer': '90 baht',
         'wrong': ['19 baht', '900 baht', '9 baht']},
    ],
    'market': [
        {'question': 'What is the first price the vendor gives?',
         'answer': '200 baht',
         'wrong': ['150 baht', '120 baht', '250 baht']},
        {'question': 'What price does the customer ask for?',
         'answer': '120 baht',
         'wrong': ['150 baht', '100 baht', '50 baht']},
        {'question': 'Does the vendor agree to her price?',
         'answer': 'Yes',
         'wrong': ['No, he refuses', 'Only if she buys two', 'He meets her halfway']},
    ],
    'temple_visit': [
        {'question': 'What must the visitor take off before going in?',
         'answer': 'Her shoes',
         'wrong': ['Her hat', 'Her sunglasses', 'Her bag']},
        {'question': 'What should she cover?',
         'answer': 'Her shoulders and knees',
         'wrong': ['Her head', 'Her hands and feet', 'Her hair']},
        {'question': 'What must she not do when taking photos?',
         'answer': 'Turn her back to the Buddha image',
         'wrong': ['Use a flash', 'Photograph the monks', 'Stand on the steps']},
    ],
    'offering_alms': [
        {'question': 'What is the woman offering the monk?',
         'answer': 'Food',
         'wrong': ['Flowers', 'Money', 'Robes']},
        {'question': 'What does she wish for the monk?',
         'answer': 'Good health',
         'wrong': ['A safe journey', 'Good luck', 'A long rest']},
        {'question': 'What does the monk wish for her?',
         'answer': 'Happiness and a long life',
         'wrong': ['Wealth and success', 'A safe journey home', 'Good weather']},
    ],
    'learning_meditation': [
        {'question': 'What does the layperson want to learn?',
         'answer': 'How to start meditating',
         'wrong': ['How to chant', 'How to become a monk', 'How to make an offering']},
        {'question': 'What does the monk say to begin with?',
         'answer': 'The breath',
         'wrong': ['Walking', 'Chanting', 'Counting beads']},
        {'question': 'How long should a beginner sit at first?',
         'answer': 'Ten minutes',
         'wrong': ['One hour', 'Two minutes', 'Thirty minutes']},
    ],
}
