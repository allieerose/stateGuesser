import tkinter as tk
from tkinter import ttk
from game import guessThePlace


class main_window:
    def __init__(self) -> None:
        self._window = tk.tix.Tk()
        self._window.title("State Guesser")
        self.set_window_dimensions(self)
        self._menuFrame = tk.Frame(self._window, padx=10, pady=10)
        self._add_start_menu_items()
        self.go_to_menu()
        self._window.mainloop()

    def set_window_dimensions(self):
        """
        Sets the default size of the application window to 4/10 x 7/10 of the
        user's screen.
        """
        width = str(4*self._window.winfo_screenwidth()//10)
        height = str(7*self._window.winfo_screenheight()//10)
        self._window.geometry(width+'x'+height)

    def go_to_menu(self):
        """
        Adds the start menu contents to the window.
        Note that it's assumed that the window is cleared (i.e., no
        other elements) when this is called.
        """
        self._menuFrame.pack()

    def start_game(self):
        """
        Removes the start menu contents from the window and starts the game.
        """
        self._menuFrame.pack_forget()  # remove start menu items from window
        guessThePlace(self, self._window)

    def _add_start_menu_items(self):
        """
        Adds the contents of the start menu to the menuFrame.
        """
        title = ttk.Label(self._menuFrame, text='Guess the U.S. State')
        title.pack()
        subtitle = ttk.Label(self._menuFrame,
                             text='Click the start button to play!')
        subtitle.pack()
        startButton = ttk.Button(self._menuFrame, text="Start",
                                 command=self.start_game)
        startButton.pack()


main_window()
