import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import random


class guessThePlace:
    def __init__(self, master, window) -> None:
        self._master = master
        self._gameFrame = tk.Frame(window, padx=10, pady=10)
        self._gameFrame.pack()
        self._images = os.listdir('images')
        # select random image for game
        file_name = random.choice(self._images)
        self._answer = file_name.split('.')[0]
        self._img_load = Image.open('images/'+file_name).resize((250, 250))
        self._img_render = ImageTk.PhotoImage(self._img_load)
        # add game elements to frame
        header = ttk.Label(self._gameFrame, text='Guess this U.S. state')
        header.pack()
        self._img_frame = tk.Label(master=self._gameFrame,
                                   background='white',
                                   image=self._img_render)
        # maintain a separate reference to avoid garbage collection
        self._img_frame.image = self._img_render
        self._img_frame.pack()
        guess_header = ttk.Label(self._gameFrame,
                                 text='I think this state is...')
        guess_header.pack()
        guess_frame = tk.Frame(self._gameFrame)
        guess_frame.pack()
        question_img = Image.open('questionIcon.png').resize((25, 25))
        question_render = ImageTk.PhotoImage(question_img)
        self._question = ttk.Label(guess_frame, image=question_render)
        self._question.image = question_render
        self._question.grid(row=0, column=0)
        self._options = ttk.Combobox(guess_frame)
        self._options['values'] = [x.split('.')[0] for x in self._images]
        self._options.grid(row=0, column=1)
        guess_button = ttk.Button(guess_frame, text='Guess',
                                  command=self.check_guess)
        guess_button.grid(row=0, column=2)
        past_guesses_label = ttk.Label(self._gameFrame, text='Past Guesses')
        past_guesses_label.pack()
        self._past_guesses_frame = tk.Frame(self._gameFrame)
        self._past_guesses_frame.pack()
        # ADD SOMETHING TO MANAGE & DISPLAY PAST GUESSES
        return_to_menu = ttk.Button(self._gameFrame,
                                    text='Return to menu',
                                    command=self.return_to_menu)
        return_to_menu.pack()

    def return_to_menu(self):
        """
        Removes the game from the window and returns the start menu. Note that
        this ends the game.
        """
        self._gameFrame.destroy()
        self._master.go_to_menu()

    def check_guess(self, guess):
        if guess == self._answer:
            # win state
            pass
        else:
            new_guess = ttk.Label(self._past_guesses_frame,
                                  text=guess)
            new_guess.pack()
