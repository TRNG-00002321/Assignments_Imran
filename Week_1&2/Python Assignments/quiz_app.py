import json
import os

QUESTION_FILE = 'questions.json'

def load_questions():
    """Loads questions from the JSON file."""
    # Simple check to see if the file exists
    if not os.path.exists(QUESTION_FILE):
        print(f"Error: The file {QUESTION_FILE} was not found.")
        return []

    try:
        with open(QUESTION_FILE, 'r') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        print("Error: Could not read the JSON file. Check the formatting.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def run_quiz():
    """Runs the quiz, tracks score, and shows the result."""
    questions = load_questions()

    if not questions:
        print("Cannot start quiz: No questions loaded.")
        return

    score = 0
    total_questions = len(questions)

    print("\n--- Welcome to the Simple Quiz! ---\n")

    for i, q_data in enumerate(questions):
        # Display question number
        print(f"Question {i + 1} of {total_questions}:")

        # Ask the question
        user_answer = input(f"{q_data['question']} ").strip()

        # Get the correct answer and standardize both for comparison
        correct_answer = q_data['answer'].strip()

        # Simple string comparison (case insensitive)
        if user_answer.lower() == correct_answer.lower():
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect. The answer was: {correct_answer}\n")

    # Display final results
    print("--- Quiz Finished ---")
    print(f"Your final score is {score} out of {total_questions}.")
    print(f"That's a score of { (score / total_questions) * 100:.2f}%.")

if __name__ == "__main__":
    run_quiz()