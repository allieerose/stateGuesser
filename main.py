import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title("State Guesser")
window.iconbitmap('')  # ADD FILE PATH TO FAVICON

# start menu items
startMenu = tk.Frame(window, padx=10, pady=10)
startMenu.pack()
title = ttk.Label(startMenu, text='Guess the U.S. State')
title.pack()
subtitle = ttk.Label(startMenu, text='Click the start button to play!')
subtitle.pack()
startButton = ttk.Button(startMenu, text="Start", command=)

window.mainloop()
