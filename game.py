import tkinter as tk
from tkinter import ttk, messagebox, tix
from PIL import Image, ImageTk
import os
import random
import zmq


class guessThePlace:
    def __init__(self, master, window) -> None:
        self._master = master
        self._window = window
        self._socket = None
        self.connect_to_socket()
        self._game_frame = tk.Frame(self._window, padx=10, pady=10)
        self._guess_frame = tk.Frame(self._game_frame)
        self._past_guesses_frame = tk.Frame(self._game_frame)
        self._options = os.listdir('images')
        self._guess_header = ttk.Label(self._game_frame,
                                       text='I think this state is...')
        self._guess = None
        self._answer = None
        self.add_game_elements()

    def connect_to_socket(self):
        """
        Connects to the ZeroMQ socket for communication with the microservice.
        """
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        self._socket.connect('tcp://localhost:5555')

    def add_label_to_game_frame(self, text):
        """
        Adds a ttk Label widget to the game frame with the given text.
        """
        new_label = ttk.Label(self._game_frame, text=text)
        new_label.pack()

    def add_game_elements(self):
        """
        Constructs and adds all elements of the game to the game_frame.
        """
        self._game_frame.pack()
        self.add_label_to_game_frame('Guess this U.S. state')
        self.pick_answer()
        self._guess_header.pack()
        self.add_guess_frame()
        self.add_label_to_game_frame('Past Guesses')
        self._past_guesses_frame.pack()
        self.return_to_menu_button()

    def pick_answer(self):
        """
        Picks a random option from the images directory, setting the choice as
        the answer for the generated game.
        """
        file_name = random.choice(self._options)
        self._answer = file_name.split('.')[0]
        img_load = Image.open('images/'+file_name).resize((250, 250))
        img_render = ImageTk.PhotoImage(img_load)
        img_frame = tk.Label(master=self._game_frame, background='white',
                             image=img_render)
        # maintain a separate reference to avoid garbage collection
        img_frame.image = img_render
        img_frame.pack()

    def add_guess_frame(self):
        """
        Sets up and packs a frame with a question icon for users to get more
        information on how to submit a guess, a Combobox drop-down for the
        user to enter their guess, and a button to submit a guess. This frame
        is then packed within the game frame.
        """
        self._guess_frame.pack()
        self.question_help_icon()
        self.guess_drop_down()
        self.guess_button()

    def question_help_icon(self):
        """
        Adds a question mark icon to the left of the guess frame with a hover
        feature that provides instructions to the user on how to use the guess
        drop-down.
        """
        question_img = Image.open('questionIcon.png').resize((25, 25))
        question_render = ImageTk.PhotoImage(question_img)
        question = tk.Label(self._guess_frame, image=question_render)
        question.image = question_render
        question.grid(row=0, column=0)
        hover_text = 'Choose a guess from the drop-down or\ntype your guess '\
                     ' in the box. Note that typed\nguesses must match (case-'\
                     'insensitive) a valid\noption to be counted as a guess.\n'
        self.add_hover_feature(question, hover_text)

    def add_hover_feature(self, object, text):
        """
        Adds a feature to the supplied tkInter widget so that a box with the
        provided text pops up when the mouse hovers over the object.
        """
        balloon = tix.Balloon(self._window)
        balloon.bind_widget(object, balloonmsg=text)
        # change background color of balloon
        for subwidget in balloon.subwidgets_all():
            subwidget['bg'] = 'white'
        self._window['bg'] = 'SystemButtonFace'

    def guess_drop_down(self):
        """
        Adds a Combobox drop-down with the possible guess options (as provided
        by the image names in the images directory) to center of the guess
        frame.
        """
        self._guess = ttk.Combobox(self._guess_frame)
        #  reformat options for later guess matching
        self._options = [x.split('.')[0] for x in self._options]
        self._guess['values'] = self._options
        self._guess.grid(row=0, column=1)

    def guess_button(self):
        """
        Adds a button with label "Guess" to the right of the guess frame.
        When the button is clicked, whatever option is selected in the
        guess drop-down (stored in self._guess) will be ran through the
        check_guess() function.
        """
        guess_button = ttk.Button(self._guess_frame, text='Guess',
                                  command=self.check_guess)
        guess_button.grid(row=0, column=2)

    def return_to_menu_button(self):
        """
        Sets up and packs the button that will return the user to the starting
        menu.
        """
        return_to_menu = ttk.Button(self._game_frame,
                                    text='Return to menu',
                                    command=self.return_to_menu)
        return_to_menu.pack(side='left')

    def return_to_menu(self):
        """
        Provides a pop-up for the user to confirm their choice to return to
        the menu. If confirmed, removes the game from the window and returns
        to the start menu. Note that this ends the game.
        If not confirmed, the pop-up is removed and no change occurs in the
        game window.
        """
        confirm = messagebox.askquestion(title='Return to menu?',
                                         message='Are you sure you want to '
                                                 'return to the menu? This '
                                                 'will end the current game.')
        if confirm == 'yes':
            self._game_frame.destroy()
            self._master.go_to_menu()

    def get_distance_direction(self, guess):
        """
        Gets and returns the distance between and direction from the guess to
        the answer by communicating with the microservice.
        """
        self._socket.send_json([guess, self._answer])
        return self._socket.recv_json()

    def check_guess(self):
        """
        Checks the new guess for validity and correctness, triggering the
        appropriate actions depending on the results (i.e., invalid guess
        causes a pop-up warning, a valid but incorrect guess gets added to
        the past guesses list with a hint, and a correct guess ends the game).
        """
        guess = self._guess.get().title()
        if not self.valid_guess(guess):
            return
        elif guess == self._answer:
            self.win_game()
        else:
            self.add_new_guess_w_hint(guess)

    def valid_guess(self, guess):
        """
        Takes a guess and validates that it's valid based off the list of
        valid guesses in self._options. Returns True for a valid guess
        and False for an invalid guess.
        """
        if guess in self._options:
            return True
        # else, invalid guess
        messagebox.showwarning(title='Invalid guess',
                               message='Your guess did not match any of '
                               'the valid options. Check your entry for '
                               'typos or browse the drop-down list of '
                               'guesses for valid options.')
        return False

    def win_game(self):
        """
        Changes content in the window to reflect a completed (won) game, adding
        buttons for the user to start a new game or quit playing.
        """
        self._guess_header['text'] = 'Correct! \n The state is ' + self._answer
        for item in self._guess_frame.winfo_children():
            item.destroy()
        new_game = ttk.Button(self._guess_frame, text='New game',
                              command=self.start_new_game)
        new_game.grid(row=0, column=0)
        quit = ttk.Button(self._guess_frame, text='Quit',
                          command=self._window.destroy)
        quit.grid(row=0, column=1)

    def add_new_guess_w_hint(self, guess):
        """
        Adds the given guess to the past guesses list with a hint indicating
        direction and distance from guess to the correct answer.
        """
        (distance, direction) = self.get_distance_direction(guess)
        new_guess_frame = ttk.Frame(self._past_guesses_frame)
        new_guess_frame.pack()
        new_guess = ttk.Label(new_guess_frame, text=guess)
        new_guess.grid(row=0, column=0)
        hint = ' - Go ' + str(distance) + ' miles ' + str(direction)
        hint_dist_direction = ttk.Label(new_guess_frame, text=hint)
        hint_dist_direction.grid(row=0, column=1)

    def start_new_game(self):
        """
        Ends the current game and starts a new one.
        """
        self._game_frame.destroy()
        self._master.start_game()
