"""Beginner mode: a gentler romanisation for learners just starting out.

A final 'i' is written 'y' and a final 'o' is written 'w' (when it is the only
one in the word), so "bpai" reads "bpay". Applied on request to a vocabulary
list; the Thai is never touched. Pure functions, no imports.
"""


def apply_beginner_mode(text):
    """
    Apply beginner-friendly romanization:
    - Final 'i' becomes 'y' (if only one 'i' in word)
    - Final 'o' becomes 'w' (if only one 'o' in word)
    """
    words = text.split()
    converted_words = []
    
    for word in words:
        if word.count('i') == 1 and word.endswith('i'):
            word = word[:-1] + 'y'
        if word.count('o') == 1 and word.endswith('o'):
            word = word[:-1] + 'w'
        converted_words.append(word)
    
    return ' '.join(converted_words)


def get_vocab_with_mode(vocab_list, beginner_mode=False):
    """Return vocabulary with optional beginner mode applied"""
    if not beginner_mode:
        return vocab_list
    
    converted = []
    for item in vocab_list:
        new_item = item.copy()
        new_item['paiboon'] = apply_beginner_mode(item['paiboon'])
        converted.append(new_item)
    return converted
