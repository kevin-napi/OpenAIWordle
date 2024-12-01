import openai
import random


openai.api_key = HIDDEN_API_KEY


WORD_LIST = ["local", "track", "newly", "whose", "chain", "laser", "fiber"]

def get_feedback(target, guess):
    feedback = []
    for i, char in enumerate(guess):
        if char == target[i]:
            feedback.append("G")  # Green: correct position
        elif char in target:
            feedback.append("Y")  # Yellow: wrong position
        else:
            feedback.append("B")  # Gray: not in word
    return feedback

def get_ai_recommendation(previous_guesses, feedbacks):
    """OPENAI implementation"""
    prompt = (
        "You are an AI assisting in a Wordle game. The target word is a 5-letter word.\n"
        "Based on the following guesses and feedbacks, suggest the next word:\n\n"
    )
    for guess, feedback in zip(previous_guesses, feedbacks):
        prompt += f"Guess: {guess}, Feedback: {''.join(feedback)}\n"

    prompt += "Recommend a valid next word:"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=10,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def wordle_game():
    target_word = random.choice(WORD_LIST)
    attempts = 6
    previous_guesses = []
    feedbacks = []

    print("Welcome to AI-Enhanced Wordle!")
    print(f"You have {attempts} attempts to guess the 5-letter word.")

    for attempt in range(1, attempts + 1):
        print(f"\nAttempt {attempt}/{attempts}")

        # Get AI recommendation
        if previous_guesses:
            ai_suggestion = get_ai_recommendation(previous_guesses, feedbacks)
            print("AI recommends:", ai_suggestion)

        guess = input("Enter your 5-letter word guess: ").lower()

        if len(guess) != 5 or guess not in WORD_LIST:
            print("Invalid word. Please guess a valid 5-letter word.")
            continue

        feedback = get_feedback(target_word, guess)
        print("Feedback:", "".join(feedback))

        previous_guesses.append(guess)
        feedbacks.append(feedback)

        if guess == target_word:
            print("You guessed the word!")
            return

    print(f"Out of attempts! The word was: {target_word}")

if __name__ == "__main__":
    wordle_game()
