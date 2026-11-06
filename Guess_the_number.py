import random


class attempt:
    def __init__(self, secret_number: int, max_attempts: int = 7):
        self.secret_number = secret_number
        self.max_attempts = max_attempts
        self.attempts_used = 0

    def read_guess(self):
        """Prompt the user for a valid guess and return it."""
        guess = int(input("\nEnter a number between 1 to 100: "))
        if not 1 <= guess <= 100:
            raise ValueError
        return guess

    def read_final_guess(self, low: int, high: int) -> int:
        """Prompt for one final choice from the two remaining numbers."""
        guess = int(input(f"\nFinal choice: enter {low} or {high}: "))
        if guess not in (low, high):
            raise ValueError
        return guess

    def check_guess(self, guess: int) -> bool:
        """Check whether the guess is correct and return True if it is."""
        if guess < self.secret_number:
            print("Too low, go higher")
            return False
        if guess > self.secret_number:
            print("Too high, go lower")
            return False

        print("Congrats! You got it.")
        return True

    def play(self):
        low, high = 1, 100
        while self.attempts_used < self.max_attempts:
            try:
                guess = self.read_guess()
            except ValueError:
                print("\nInvalid input. Enter a whole number from 1 to 100.")
                continue

            self.attempts_used += 1

            if self.check_guess(guess):
                return True

            if guess < self.secret_number:
                low = max(low, guess + 1)
            else:
                high = min(high, guess - 1)

            print(f"The number is between {low} and {high}, inclusive.")

            if high - low == 1:
                print(f"\nOnly {low} and {high} remain. Your next guess is final.")
                while True:
                    try:
                        final_guess = self.read_final_guess(low, high)
                    except ValueError:
                        print(f"\nInvalid choice. Enter only {low} or {high}.")
                        continue

                    self.attempts_used += 1
                    if self.check_guess(final_guess):
                        return True

                    print(f"Wrong final choice. You lose. The number was {self.secret_number}.")
                    return False

        return False


class NumberGuessingGame(attempt):
    def read_guess(self):
        guess = int(input("\nEnter a number between 1 to 100: "))
        if guess < 1 or guess > 100:
            raise ValueError
        return guess

    def check_guess(self, guess: int) -> bool:
        if guess < self.secret_number:
            print("Too low, go higher")
            return False
        if guess > self.secret_number:
            print("Too high, go lower")
            return False

        print("Congrats! You got it.")
        return True


secret = random.randint(1, 100)
game = NumberGuessingGame(secret)

print("Only 7 attempts are allowed to win the game.")

won = game.play()
if not won:
    print("Attempts over.\nOut!")
elif game.attempts_used <= 3:
    print(f"Guessed in {game.attempts_used} attempts. Genius!!")
else:
    print(f"Guessed in {game.attempts_used} attempts.")


print(f"The secret number was: {secret}")