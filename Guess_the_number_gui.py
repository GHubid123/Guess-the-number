import random
import tkinter as tk


# ======================================================================
# ORIGINAL CODE
# ======================================================================
class attempt:
    def __init__(self, secret_number: int, max_attempts: int = 7):
        self.secret_number = secret_number
        self.max_attempts = max_attempts
        self.attempts_used = 0

    def read_guess(self):
        """Prompt the user for a valid guess and return it."""
        guess = int(input("\nEnter a whole number between 1 and 100 (inclusive): "))
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
                low = guess + 1
            else:
                high = guess - 1

            print(
                f"The number is between {low} and {high}, inclusive. "
                f"You can guess {low} and {high} too.")

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
        guess = int(input("\nEnter a whole number between 1 and 100 (inclusive): "))
        if guess < 1 or guess > 100:
            raise ValueError
        return guess

    def check_guess(self, guess: int):
        if guess < self.secret_number:
            print("Too low, go higher")
            return False
        if guess > self.secret_number:
            print("Too high, go lower")
            return False

        print("Congrats! You got it.")
        return True


# ======================================================================
#  GUI LAYER
#  A GUI cannot use input()/print()/a blocking while-loop, so this small
#  subclass keeps your game rules and swaps only those two things:
#  the typed text comes from the window, and the message is stored
#  instead of printed.
# ======================================================================
class GuiNumberGame(NumberGuessingGame):
    message = ""

    def parse_guess(self, text: str):
        """Same validation as read_guess, but takes the text from the GUI."""
        guess = int(text.strip())
        if guess < 1 or guess > 100:
            raise ValueError
        return guess

    def parse_final_guess(self, text: str, choices: tuple[int, int]) -> int:
        """Validate a GUI guess against the two allowed final choices."""
        guess = self.parse_guess(text)
        if guess not in choices:
            raise ValueError
        return guess

    def check_guess(self, guess: int):
        """Same checks as your version, but stores the message for the GUI."""
        if guess < self.secret_number:
            self.message = "Too low, go higher"
            return False
        if guess > self.secret_number:
            self.message = "Too high, go lower"
            return False

        self.message = "Congrats! You got it."
        return True


# ---- look and feel ----------------------------------------------------
BG = "#1b1b2b"
CARD = "#26263a"
TEXT = "#ececf5"
MUTED = "#8e8eab"
ACCENT = "#7c9cff"
GOOD = "#4ade80"
BAD = "#f87171"
WARN = "#fbbf24"
TRACK = "#35354d"

BAR_W, BAR_H = 360, 22
FONT = "Segoe UI"


class GameWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Guess the Number")
        root.configure(bg=BG)
        root.resizable(False, False)

        card = tk.Frame(root, bg=CARD, padx=30, pady=24)
        card.pack(padx=24, pady=24)

        tk.Label(card, text="Guess the Number", bg=CARD, fg=TEXT,
                 font=(FONT, 22, "bold")).pack()
        self.subtitle = tk.Label(card, bg=CARD, fg=MUTED, font=(FONT, 10))
        self.subtitle.pack(pady=(2, 14))

        # range display: shows where the secret number can still be
        self.range_label = tk.Label(card, bg=CARD, fg=TEXT, font=(FONT, 12),
                                    wraplength=BAR_W, justify="center")
        self.range_label.pack()
        self.bar = tk.Canvas(card, width=BAR_W, height=BAR_H + 6, bg=CARD,
                             highlightthickness=0)
        self.bar.pack(pady=(6, 4))
        scale = tk.Frame(card, bg=CARD, width=BAR_W)
        scale.pack(fill="x")
        tk.Label(scale, text="1", bg=CARD, fg=MUTED, font=(FONT, 9)).pack(side="left")
        tk.Label(scale, text="100", bg=CARD, fg=MUTED, font=(FONT, 9)).pack(side="right")

        # attempts left, drawn as dots
        self.dots = tk.Canvas(card, height=34, bg=CARD, highlightthickness=0)
        self.dots.pack(pady=(14, 0))
        self.attempts_label = tk.Label(card, bg=CARD, fg=MUTED, font=(FONT, 10))
        self.attempts_label.pack()

        # input
        self.entry = tk.Entry(card, justify="center", font=(FONT, 20, "bold"),
                              width=6, bg=TRACK, fg=TEXT, insertbackground=TEXT,
                              relief="flat", highlightthickness=2,
                              highlightbackground=TRACK, highlightcolor=ACCENT)
        self.entry.pack(pady=(14, 8), ipady=6)

        self.guess_btn = tk.Button(card, text="Guess", command=self.submit,
                                   font=(FONT, 12, "bold"), bg=ACCENT, fg="#101020",
                                   activebackground="#9db4ff", relief="flat",
                                   cursor="hand2", width=14, pady=6)
        self.guess_btn.pack()

        # feedback
        self.feedback = tk.Label(card, bg=CARD, fg=TEXT, font=(FONT, 14, "bold"),
                                 height=2, wraplength=BAR_W, justify="center")
        self.feedback.pack(pady=(14, 0))
        self.detail = tk.Label(card, bg=CARD, fg=MUTED, font=(FONT, 10),
                               wraplength=BAR_W, justify="center")
        self.detail.pack()

        self.again_btn = tk.Button(card, text="Play again", command=self.new_game,
                                   font=(FONT, 11, "bold"), bg=GOOD, fg="#101020",
                                   activebackground="#86efac", relief="flat",
                                   cursor="hand2", width=14, pady=5)

        root.bind("<Return>", self.on_enter)
        self.new_game()

    # ---- game flow ----
    def new_game(self):
        self.game = GuiNumberGame(random.randint(1, 100))
        self.low, self.high = 1, 100
        self.final_choice = None
        self.cur_l, self.cur_r = 0.0, float(BAR_W)   # animated bar edges
        self.over = False
        self.result_color = None

        self.subtitle.config(
            text=f"Only {self.game.max_attempts} attempts are allowed to win the game.")
        self.feedback.config(text="Make your first guess!", fg=MUTED)
        self.detail.config(text="")
        self.again_btn.pack_forget()
        self.guess_btn.config(state="normal", bg=ACCENT)
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus_set()
        self.refresh()
        self.animate_bar()

    def on_enter(self, event: tk.Event | None = None) -> None:
        if self.over:
            self.new_game()
        else:
            self.submit()

    def submit(self):
        if self.over:
            return

        try:
            if self.final_choice is None:
                guess = self.game.parse_guess(self.entry.get())
            else:
                guess = self.game.parse_final_guess(
                    self.entry.get(), self.final_choice)
        except ValueError:
            if self.final_choice is None:
                message = "Invalid input. Enter a whole number from 1 to 100."
            else:
                message = (
                    f"Final choice: enter only {self.final_choice[0]} "
                    f"or {self.final_choice[1]}.")
            self.set_feedback(message, WARN)
            self.shake()
            self.entry.select_range(0, tk.END)
            return

        is_final_choice = self.final_choice is not None
        self.game.attempts_used += 1
        self.entry.delete(0, tk.END)

        if self.game.check_guess(guess):
            self.finish(won=True)
            return

        if is_final_choice:
            self.finish(won=False, final_choice=True)
            return

        # narrow the range of numbers still possible
        if guess < self.game.secret_number:
            self.low = max(self.low, guess + 1)
            self.set_feedback("▲  " + self.game.message, ACCENT)
        else:
            self.high = min(self.high, guess - 1)
            self.set_feedback("▼  " + self.game.message, "#fb923c")

        self.refresh()
        self.animate_bar()

        if self.high - self.low == 1:
            self.final_choice = (self.low, self.high)
            self.set_feedback(
                f"Final choice: choose {self.low} or {self.high}. "
                "Your next guess decides the game.", WARN)

        if (self.game.attempts_used >= self.game.max_attempts
                and self.final_choice is None):
            self.finish(won=False)

    def finish(self, won: bool, final_choice: bool = False) -> None:
        g = self.game
        self.over = True
        self.result_color = GOOD if won else BAD

        if won and g.attempts_used <= 3:
            msg = f"Guessed in {g.attempts_used} attempts. Genius!!"
        elif won:
            msg = f"Guessed in {g.attempts_used} attempts."
        elif final_choice:
            msg = "Wrong final choice.\nOut!"
        else:
            msg = "Attempts over.\nOut!"

        self.set_feedback(msg, self.result_color)
        self.detail.config(text=f"The secret number was: {g.secret_number}")
        if won:
            self.low = self.high = g.secret_number
        self.entry.config(state="disabled")
        self.guess_btn.config(state="disabled", bg=TRACK)
        self.again_btn.pack(pady=(12, 0))
        self.refresh()
        self.animate_bar()

    # ---- drawing ----
    def set_feedback(self, text: str, color: str) -> None:
        self.feedback.config(text=text, fg=color)

    def refresh(self):
        g = self.game
        left = max(0, g.max_attempts - g.attempts_used)
        self.attempts_label.config(text=f"Attempts left: {left}")

        if self.low == self.high:
            self.range_label.config(text=f"The number is {self.low}")
        else:
            self.range_label.config(
                text=(f"The number is between {self.low} and {self.high}, inclusive. "
                      f"You can guess {self.low} and {self.high} too."))

        # dots: bright = attempts left, dim/colored = used
        self.dots.delete("all")
        n, size, gap = g.max_attempts, 18, 10
        total = n * size + (n - 1) * gap
        self.dots.config(width=total + 4)
        for i in range(n):
            x = 2 + i * (size + gap)
            if i < g.attempts_used:
                color = self.result_color if (self.result_color and i == g.attempts_used - 1) else TRACK
            else:
                color = ACCENT
            self.dots.create_oval(x, 8, x + size, 8 + size, fill=color, outline="")

    def animate_bar(self):
        """Smoothly slide the highlighted part of the bar to the new range."""
        target_l = (self.low - 1) / 100 * BAR_W
        target_r = self.high / 100 * BAR_W
        self.cur_l += (target_l - self.cur_l) * 0.3
        self.cur_r += (target_r - self.cur_r) * 0.3

        c = self.bar
        c.delete("all")
        c.create_rectangle(0, 3, BAR_W, 3 + BAR_H, fill=TRACK, outline="")
        color = self.result_color or ACCENT
        right = max(self.cur_r, self.cur_l + 4)
        c.create_rectangle(self.cur_l, 3, right, 3 + BAR_H, fill=color, outline="")

        if abs(target_l - self.cur_l) > 0.5 or abs(target_r - self.cur_r) > 0.5:
            self.root.after(16, self.animate_bar)

    def shake(self, step: int = 0):
        """Quick left-right wiggle of the window on invalid input."""
        offsets = [10, -10, 7, -7, 3, -3, 0]
        if step == 0:
            self.root.update_idletasks()
            self._x, self._y = self.root.winfo_x(), self.root.winfo_y()
        if step < len(offsets):
            self.root.geometry(f"+{self._x + offsets[step]}+{self._y}")
            self.root.after(25, lambda: self.shake(step + 1))


if __name__ == "__main__":
    root = tk.Tk()
    GameWindow(root)
    root.mainloop()
