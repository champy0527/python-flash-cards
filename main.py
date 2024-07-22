from tkinter import *
import pandas as pd
from random import choice

# ---------------------------- CONSTANTS ------------------------------- #

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")


# ---------------------------- WORDS ------------------------------- #

word_library = pd.read_csv("data/french_words.csv")
frequency_dictionary = {row["French"]: row["English"] for (index, row) in word_library.iterrows()}
# frequency_dictionary = pd.DataFrame.to_dict(word_library)


print(frequency_dictionary)


def pick_random_word():
    french_word = choice(list(frequency_dictionary.keys()))
    canvas.itemconfig(word_text, text=f"{french_word}")


# print(pick_random_word())

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

"""FRONT CARD UI"""

canvas = Canvas(width=800, height=624, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2, sticky=EW)

"""Text on card"""
langauge_text = canvas.create_text(400, 150, text="Language", font=LANGUAGE_FONT)
word_text = canvas.create_text(400, 263, text="", font=WORD_FONT)

"""Buttons"""
wrong_img = PhotoImage(file="./images/wrong.png")
wrong_img_item = canvas.create_image(200, 576, image=wrong_img)
canvas.tag_bind(wrong_img_item, '<Button-1>', lambda event: pick_random_word())
canvas.grid(column=0, row=1)

right_img = PhotoImage(file="./images/right.png")
right_img_item = canvas.create_image(600, 576, image=right_img)
canvas.grid(column=1, row=1)


window.mainloop()
