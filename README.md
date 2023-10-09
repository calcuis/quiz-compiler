## Quiz Game
*You should compile your itemset via `Editor` first before kicking start with the `Quiz`.

**Game:** Quiz

**Editor:** Item Panel

## code review
This Python code (game.py) defines a simple quiz application using the `tkinter` library for the GUI. Here's a brief explanation of its structure and functionality:

**Imports:**
- import `json`: Allows working with JSON data.
- import `tkinter` as `tk`: Imports the `tkinter` library for creating the GUI.
- from `tkinter` import `messagebox`: Imports a specific function from `tkinter` to display message boxes.

**Quiz Class:**
- The Quiz class represents the quiz application.
- It loads questions from a JSON file, displays questions and options, allows users to select answers, evaluates the quiz, and displays the results.

**Methods in the Quiz Class:**
- `__init__(self, master)`: Initializes the Quiz object, loads questions from a file, and creates the initial GUI widgets.
- `load_questions(self, filename)`: Loads questions from a JSON file.
- `create_widgets(self)`: Creates GUI widgets (question label).
- `display_question(self)`: Displays the current question.
- `get_user_answer(self)`: Gets the user's answer and processes it.
- `next_question(self)`: Moves to the next question or ends the quiz if all questions have been answered.
- `display_option(self)`: Displays the answer options for the current question.
- `evaluate_quiz(self)`: Evaluates the quiz and displays the user's score and ratio of correct answers.
- `start_quiz(self)`: Initializes the quiz, displays the first question, and sets up the interface.

**Main Section:**
- Creates a `tkinter` window (root) for the quiz application.
- Initializes a Quiz object and starts the quiz using the `start_quiz()` method.
- Sets up the GUI window, including title and dimensions.
- Starts the tkinter main event loop with `root.mainloop()` to handle user interactions.

The application allows the user to take a quiz with multiple-choice questions, providing feedback on each answer and displaying the final score at the end. The questions and options are loaded from a JSON file (questions.json).

*Please refer to item-editor-json repo for Editor's code review.
