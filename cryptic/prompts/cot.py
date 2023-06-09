ben_v1 = {
    "prompt": """I will answer some clues:
    1. Boy captures the work of Shakespeare, for example (7)
    Answer: SONNETS (examples of works of Shakespeare) - SON (boy) + NETS (captures)
    2. Country folk appearing in operatic piece (7)
    Answer: ARMENIA (country) - ARIA (operatic piece) + MEN (folk)
    3. Where men are on board ship beside revolutionary (5)
    Answer: CHESS (where men are on board) - CHE (Revolutionary, Che Guevara) + SS (designation for a ship)
    4. Amputate limbs to remove weapons (6)
    Answer: DISARM (Remove weapons  - DIS-ARM (amputating limbs)
    5. Accuse one politician apiece (7)
    Answer: IMPEACH (accuse) - I (one) + MP (politician) + EACH (apiece)
    6. Orchestra was taken aback by cutting machine (7)
    Answer: BANDSAW (cutting machine) - BAND (orchestra) + SAW (was, 'taken aback' i.e. backwards)
    7. Concerning drama in second game after draw (6)
    Answer: REPLAY (a second game, typically following a drawn result in the first) - RE (meaning concerning) + PLAY (a type of drama)
    Answer this clue in the same style, making sure not to give any verbal explanation, following 'Answer:'.

    Clue: {clue} {num_letters}
    """,
    "example_output": "Answer: REPLAY (a second game, typically following a drawn result in the first) - RE (meaning concerning) + PLAY (a type of drama)",
    "answer_pattern": r"Answer: (?P<answer>[\w\s]+) \((?P<definition>[\w\s,\.:;']+)\) - (?P<wordplay>.+)",
    "subclue_separator": " + ",
    "sub_answer_pattern": r"(?P<answer>[\w\s]+) \((?P<definition>[\w\s,\.:;']+)\)",
}

ben_letters = {
    "prompt": """
    I will answer some clues:
    1. Boy captures the work of Shakespeare, for example (7)
    Letters: _ON__S
    Answer: SONNETS (examples of works of Shakespeare) - SON (boy) + NETS (captures)
    2. Country folk appearing in operatic piece (7)
    Letters: _______
    Answer: ARMENIA (country) - ARIA (operatic piece) + MEN (folk)
    3. Where men are on board ship beside revolutionary (5)
    Letters: C____
    Answer: CHESS (where men are on board) - CHE (Revolutionary, Che Guevara) + SS (designation for a ship)
    4. Amputate limbs to remove weapons (6)
    Letters: __S___
    Answer: DISARM (Remove weapons  - DIS-ARM (amputating limbs)
    5. Accuse one politician apiece (7)
    Letters: I_____H
    Answer: IMPEACH (accuse) - I (one) + MP (politician) + EACH (apiece)
    6. Orchestra was taken aback by cutting machine (7)
    Letters: ____S__
    Answer: BANDSAW (cutting machine) - BAND (orchestra) + SAW (was, 'taken aback' i.e. backwards)
    7. Concerning drama in second game after draw (6)
    Letters: __P_A_
    Answer: REPLAY (a second game, typically following a drawn result in the first) - RE (meaning concerning) + PLAY (a type of drama)
    Answer this clue in the same style, making sure not to give any verbal explanation, following 'Answer:'.
    """
}


ben_v1_mod = {
    "prompt": """
    I will answer some clues. Answer in the same style, making sure not to give any verbal explanation.

    Clue: Boy captures the work of Shakespeare, for example (7)
    Answer: SONNETS (examples of works of Shakespeare) - SON (boy) + NETS (captures)

    Clue: Country folk appearing in operatic piece (7)
    Answer: ARMENIA (country) - ARIA (operatic piece) + MEN (folk)

    Clue: Where men are on board ship beside revolutionary (5)
    Answer: CHESS (where men are on board) - CHE (Revolutionary, Che Guevara) + SS (designation for a ship)

    Clue: Amputate limbs to remove weapons (6)
    Answer: DISARM (Remove weapons  - DIS-ARM (amputating limbs)

    Clue: Accuse one politician apiece (7)
    Answer: IMPEACH (accuse) - I (one) + MP (politician) + EACH (apiece)

    Clue: Orchestra was taken aback by cutting machine (7)
    Answer: BANDSAW (cutting machine) - BAND (orchestra) + SAW (was, 'taken aback' i.e. backwards)

    Clue: Concerning drama in second game after draw (6)
    Answer: REPLAY (a second game, typically following a drawn result in the first) - RE (meaning concerning) + PLAY (a type of drama)

    Clue: {clue} {num_letters}
    Answer: 
    """,
    "answer_pattern": r"Answer: (?P<answer>[\w\s]+) \((?P<definition>[\w\s,\.:;']+)\) - (?P<wordplay>.+)",
    "example_output": "REPLAY (a second game, typically following a drawn result in the first) - RE (meaning concerning) + PLAY (a type of drama)",
    "subclue_separator": " + ",
    "sub_answer_pattern": r"(?P<answer>[\w\s]+) \((?P<definition>[\w\s,\.:;']+)\)",
}
