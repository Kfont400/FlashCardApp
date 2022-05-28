from tkinter import *
import pandas as pd
import random


BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
unknown_words = pd.DataFrame(columns = ['Spanish', 'English'])
known_words = pd.DataFrame(columns = ['Spanish', 'English'])

try:
    data = pd.read_csv('./data/unknown_words.csv',encoding='latin-1')
except FileNotFoundError:
    original_data = pd.read_csv('./data/spanish/spanish_phrases.csv',encoding='latin-1')
    all_words = original_data.to_dict(orient='records')
else:    
    all_words = data.to_dict(orient='records')
#------------------------ Button functions -----------------------------#

def next_card():

    try:
        global current_word, flip_timer
        window.after_cancel(flip_timer)
        current_word = random.choice(all_words)
        canvas.itemconfig(language_choice,text='Spanish',fill='black')
        canvas.itemconfig(language_word,text=current_word['Spanish'],fill='black')
        canvas.itemconfig(current_card, image=card_front)
        flip_timer = window.after(3000,func=flip_card)
        
    except IndexError:
        canvas.itemconfig(language_choice,text='',fill='white')
        canvas.itemconfig(language_word,text='The end',fill='Black')
        unknown_words.to_csv('./data/spanish/unknown_words.csv',index=False)
        known_words.to_csv('./data/spanish/known_words.csv',index=False)
    except (ValueError, OSError):
        pass


def flip_card():
    
    canvas.itemconfig(language_choice,text='English',fill='white')
    canvas.itemconfig(language_word,text=current_word['English'],fill='white')
    canvas.itemconfig(current_card, image=card_back)

def is_known():
    global known_words
    all_words.remove(current_word)
    known_words = known_words.append(current_word,ignore_index=True)
    print(known_words)
    next_card()

def is_unknown():
    global unknown_words
    all_words.remove(current_word)
    unknown_words = unknown_words.append(current_word,ignore_index=True)
    print(unknown_words)
    next_card()

#-------------------------- Start Window -------------------------------#

#------------------------------- UI ------------------------------------#
#Create window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000,func=flip_card)

#Create all images
card_front = PhotoImage(file='./images/card_front.png')
card_back = PhotoImage(file='./images/card_back.png')
right_pic = PhotoImage(file='./images/right.png')
wrong_pic = PhotoImage(file='./images/wrong.png')

#Create background for window
canvas = Canvas(width=900, height=600, bg=BACKGROUND_COLOR, highlightthickness=0)
current_card = canvas.create_image(450, 300, image=card_front)
language_choice = canvas.create_text(450,150,text='', font=('Arial', 40, 'italic'))
language_word = canvas.create_text(450,300,text='', font=('Arial', 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

#Assign images with buttons
known_button = Button(image=right_pic,bg=BACKGROUND_COLOR,highlightthickness=0, bd=0,activebackground=BACKGROUND_COLOR,command=is_known)
unknown_button = Button(image=wrong_pic,bg=BACKGROUND_COLOR,highlightthickness=0, bd=0,activebackground=BACKGROUND_COLOR,command=is_unknown)

known_button.grid(column=1, row=1)
unknown_button.grid(column=0, row=1)

next_card()


window.mainloop()

