from tkinter import *
import pandas as pd
from random import choice

# ---------------------------- CONSTANTS ------------------------------- #

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")

french_word = ""

# ----------------------- WORD/LANGUAGE SETUP ---------------------------- #
""" This is now interchangeable depending on the language of the csv file you import."""
try:
    word_library_df = pd.read_csv("data/words_to_learn.csv")

except FileNotFoundError:
    word_library_df = pd.read_csv("data/tagalog_words.csv")

word_library_df.columns = list(word_library_df)  # to put header inside data frame
language = list(word_library_df.columns)
print(language)

frequency_dictionary = {row.iloc[0]: row.iloc[1] for (index, row) in word_library_df.iterrows()}
# This allows to assign the header based on any language imported from the csv

print(frequency_dictionary)  # debugger
words_to_learn = frequency_dictionary.copy()


# -------------------------- CARD FLIP ----------------------------- #

def show_foreign_card():
    global french_word
    french_word = choice(list(frequency_dictionary.keys()))
    canvas.itemconfig(language_text, text=f"{language[0]}", fill="black")
    canvas.itemconfig(word_text, text=f"{french_word}", fill="black")
    canvas.itemconfig(card_bg, image=card_front)
    window.after(3000, func=show_english_translation)


def show_english_translation():
    global french_word
    english_word = frequency_dictionary.get(french_word)
    canvas.itemconfig(language_text, text=f"{language[1]}", fill="white")
    canvas.itemconfig(word_text, text=f"{english_word}", fill="white")
    canvas.itemconfig(card_bg, image=card_back)


# ------------------------- SAVE FOR LATER ---------------------------- #

"""Pops the learnt word so that it doesn't show up the next time a programme is run"""
def save_for_later():
    global french_word
    if french_word in words_to_learn:
        words_to_learn.pop(french_word)
    print(f"Remaining words {len(words_to_learn)} out of {len(frequency_dictionary)}")
    words_to_learn_data = pd.DataFrame(list(words_to_learn.items()), columns=[f"{language[0]}", f"{language[1]}"])
    words_to_learn_data.to_csv("data/words_to_learn.csv", index=False)
    show_foreign_card()

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

"""FRONT CARD UI"""

canvas = Canvas(width=800, height=624, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
card_bg = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2, sticky=EW)

"""Text on card"""
language_text = canvas.create_text(400, 150, text="Language", font=LANGUAGE_FONT)
word_text = canvas.create_text(400, 263, text="", font=WORD_FONT)

"""Wrong and Right Buttons"""
wrong_img = PhotoImage(file="./images/wrong.png")
wrong_img_item = canvas.create_image(200, 576, image=wrong_img)
canvas.tag_bind(wrong_img_item, '<Button-1>', lambda event: show_foreign_card())
canvas.grid(column=0, row=1)


right_img = PhotoImage(file="./images/right.png")
right_img_item = canvas.create_image(600, 576, image=right_img)
canvas.tag_bind(right_img_item, '<Button-1>', lambda event: save_for_later())
canvas.grid(column=1, row=1)

"""Initialises the first word"""
show_foreign_card()

window.mainloop()
