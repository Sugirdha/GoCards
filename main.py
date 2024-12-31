import random
from tkinter import *
import pandas as pd
from extract import RTFExtractor


BACKGROUND_COLOR = "#a8dadc"
current_card = {}
to_learn = {}

# Path to the RTF file
rtf_file_path = 'data/japanese_frequent_words.rtf'

# Create an instance of the extractor
extractor = RTFExtractor(rtf_file_path)


def extract_df():
    # Extract the DataFrame
    try:
        df = extractor.extract_dataframe()
        print("DataFrame created successfully!")
        return df
    except FileNotFoundError as e:
        print(e)
    except RuntimeError as e:
        print(e)


try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = extract_df()
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Kanji / Kana", fill="black")
    canvas.itemconfig(card_word, text=f"{current_card['Kanji']} / {current_card['Kana']}", font=("Ariel", 60, "bold"))
    canvas.itemconfig(card_background, image=img_card_front)
    flip_timer = window.after(4000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], font=("Ariel", 40, "bold"), width=600)
    canvas.itemconfig(card_background, image=img_card_back)


def is_known():
    global data
    if len(to_learn) > 1:
        to_learn.remove(current_card)
    print(f"Words left to learn: {len(to_learn)}")
    canvas.itemconfig(label_count, text=f"{len(to_learn)} words left to learn", fill="black")
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flash Cards App")
window.config(padx=100, pady=100, background=BACKGROUND_COLOR)

flip_timer = window.after(4000, func=flip_card)

canvas = Canvas(height=526, width=800)
img_card_front = PhotoImage(file="images/card_front.png")
img_card_back = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(410, 263, image=img_card_front)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="Word", fill="black")
label_count = canvas.create_text(400, 420,
                                 text=f"Words left to learn: {len(to_learn)}",
                                 font=("Ariel", 20, "italic"),
                                 fill="black")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

icon_unknown = PhotoImage(file="images/wrong.png")
button_unknown = Button(image=icon_unknown, highlightthickness=0, command=next_card, borderwidth=0)
button_unknown.grid(row=1, column=0)

icon_known = PhotoImage(file="images/right.png")
button_known = Button(image=icon_known, highlightthickness=0, command=is_known, borderwidth=0)
button_known.grid(row=1, column=1)

next_card()

window.mainloop()
