import tkinter as tk
from tkinter import *
menu = tk.Tk() #creates the menu box and sets its geometry and title
menu.geometry("400x500")
menu.title("Menu")
menu.configure(bg="orange")
def start(): #starts the main method
    menu.withdraw()
    import main
    from main import root
    restart() #restarts the game buy running method
    root.mainloop() #starts the code
def restart():
    from main import restart # restarts game by running method in main called restart
    restart()
def tutorial(): #will create a tutorial image (not finished)
    tutorial = tk.Tk()
    tutorial.title("Tutorial")
    # Load a PNG image
    image = PhotoImage(master=tutorial, width=471, height=636, file="rules.png")
    # Create a Label widget to display the image
    label = tk.Label(tutorial, image=image)
    label.image = image  # Keep a reference to the image
    label.pack()
#adjusts the menu by creating a text box and two buttons and places them in correct order/assigns their height
text = Label(menu, text="MANCALA GAME", fg="BLUE", bg="ORANGE", font=("Helvetica", 18))
text.place(x=100,y=0)
start = tk.Button(menu, width=10, height=10, text=f"START",command=start, bg="blue", fg="orange",font=("Helvetica", 12))
start.place(x=150,y=50)
tutorial = tk.Button(menu, width=10, height=10, text=f"TUTORIAL",command=tutorial, bg="blue", fg="orange",font=("Helvetica", 12))
tutorial.place(x=150,y=260)
#runs a mainloop that restarts the code
menu.mainloop()