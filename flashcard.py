"""
flashcard.py
    Flashcard GUI
"""

# -*- coding: UTF-8 -*-

from tkinter import *
import pandas as pd
import os
import random

BACKGROUND_COLOR = "#B1DDC6"


def prepare_words() -> (dict[str, str], dict[str, str]):
    """
    Reading words from .csv file
    :return: a dictionary containing words and their translation, another contains the languages indicators
    """
    data_to_read = './data/german_words.csv'
    if os.path.isfile('./data/words_to_learn.csv') and os.stat('./data/words_to_learn.csv').st_size > 0:
        data_to_read = './data/words_to_learn.csv'

    with open(data_to_read, 'r', newline='') as to_learn_csv:
        to_learn_df = pd.read_csv(to_learn_csv, index_col=None)
        to_learn_dict = to_learn_df.to_dict(orient='split')
        translated_dict = dict(to_learn_dict['data'])
        languages = to_learn_dict['columns']
        return translated_dict, languages


class FlashCardApp:
    """
    Class for flash card
    """
    def __init__(self):
        self.dictionary, self.languages = prepare_words()
        self.front = None
        self.back = None
        self.flip_timer = None

    def create_flashcard(self) -> [str, str]:
        """
        Select a word and its translation randomly
        :return: word to learn and translated word
        """
        return random.choice(list(self.dictionary.items()))

    def remove_learned_flashcard(self) -> None:
        """
        Remove a learned word
        """
        if self.front is not None and self.back is not None:
            self.dictionary.pop(self.front)

    def save_progress(self) -> None:
        """
        Add words that still remained to a .csv file after a learning session
        """
        with open('./data/words_to_learn.csv', 'w', newline='') as left_over_data:
            left_over_data.write(f'{self.languages[0]},{self.languages[1]}\n')
            for key, value in self.dictionary.items():
                left_over_data.write(f'{key},{value}\n')

    def create_gui(self) -> None:
        """
        Create the GUI for Flash Card App
        """
        def next_card():
            if self.flip_timer is not None:
                window.after_cancel(self.flip_timer)
            self.front, self.back = self.create_flashcard()
            canvas.itemconfig(background, image=front_card_img)
            canvas.itemconfig(language_text, text=self.languages[0], fill='black')
            canvas.itemconfig(word_text, text=self.front, fill='black')
            self.flip_timer = window.after(3000, func=flip_card)

        def flip_card():
            """
            Show the translation of a word
            """
            canvas.itemconfig(background, image=back_card_img)
            canvas.itemconfig(language_text, text=self.languages[1], fill='white')
            canvas.itemconfig(word_text, text=self.back, fill='white')

        def check_right():
            """
            Mark a word as learned
            """
            self.remove_learned_flashcard()
            canvas.delete(start_text)
            next_card()

        def check_wrong():
            """
            Mark a word as unlearned
            """
            canvas.delete(start_text)
            next_card()

        window = Tk()
        window.title('Flash Cards App')
        window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

        front_card_img = PhotoImage(file='./images/card_front.png')
        back_card_img = PhotoImage(file='./images/card_back.png')

        canvas = Canvas(window, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
        background = canvas.create_image(400, 213, image=front_card_img)
        start_text = canvas.create_text(400, 213, text="Press ✓ to start learning!", font=('Arial', 20, 'bold'))
        language_text = canvas.create_text(400, 183, text='', font=('Arial', 20, 'italic'))
        word_text = canvas.create_text(400, 243, text='', font=('Arial', 32, 'bold'))
        canvas.grid(row=0, column=0, columnspan=2, sticky='nsew')

        right_img = PhotoImage(file='./images/right.png')
        right_button = Button(image=right_img, highlightthickness=0, bd=0, command=check_right)
        right_button.grid(row=1, column=1)

        wrong_img = PhotoImage(file='./images/wrong.png')
        wrong_button = Button(image=wrong_img, highlightthickness=0, bd=0, command=check_wrong)
        wrong_button.grid(row=1, column=0)

        window.mainloop()

        self.save_progress()
