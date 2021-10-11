"""
main.py
    Main class for the FlashCardLearner.
    This simple application is designed to learn new german words.
    Each german word will be shown in 3 seconds, and then english translation.
    If user already remembered that word, check mark should be clicked and next word will shown.
    Otherwise, x mark will be clicked, the word will be marked as unlearned and appear at some point in the future
    Words are scraped from wikipedia
"""
from flashcard import FlashCardApp


def main():
    app = FlashCardApp()
    app.create_gui()


main()
