1. Answer generator given question
2. Answer generator given constraints from board (word with gaps)
3. Answer generator given question + constraints from board
4. Answer critiquer given question, answer:
    - model critique
    - self-consistency of explanation given answer, question
5. Question parser given question
6. Question parser given question, answer
7. Answer critiquer given question, answer, parse
8. Answer generator given question, parse


General solution strategy:

0. Answer questions with no context
1. Answer questions with context
2. Some way to achieve a consistent board: e.g. if your answers
seem to lead to an impasse, you need a way to consider whether
alternatives might help.