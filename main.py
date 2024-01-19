import tkinter as tk
from tkinter import *
# Create the main window
root=tk.Tk()
root.configure(bg="orange")
main = tk.Tk()
main.withdraw()
root.geometry("1200x600") #sets geometry of mancala board
main.geometry("80x150") #sets geometry of text box at end of game
root.title("Mancala") #sets title for mancala board
#counter is used to determine player turns counter==0 means player 1 counter==1 means player 2
counter=0
#parameter for col
b=0
#parameter for row
c=0
# Create a function to handle button clicks
def button_click(b,c):
    global counter
    #checks if row and col are correct for params
    print(f"{c}")
    print(f"{b}")
    #sets parameters as given varaibles
    row=c
    col=b
    #if row 1 has been and it is player 2s turn or if row 0 has been selected and it is player 1s turn it runs
    if ((row==1 and counter==1) or (row==0 and counter==0)) and (grid[row][col]!=0):
        for i in range(grid[c][b]): #runs a for loop that traverses the amount of elements for each bead in the selected array, adds 1 to each element until out of beads
            grid[c][b]=grid[c][b]-1
            if(row==1): #If row is 1 then it adds 1 to the elements, with increasing cols
                if(col+1>6): #if the bead is past the last col then it places it in the next corresponding thing which is the other players first mancala
                    #sets the col and the row to that element
                    col=6
                    row=0
                    grid[0][6]=grid[0][6]+1
                else:
                    grid[row][col+1]=grid[row][col+1]+1
                    col=col+1
            elif(row==0): #If row is 0 then it adds 1 to the elements, with decreasing cols
                if (col-1<0): #if the bead is past the last col then it places it in the next corresponding thing which is the other players first mancala
                    # sets the col and the row to that element
                    col = 0
                    row = 1
                    grid[1][0]=grid[1][0]+1
                else:
                    grid[row][col-1] = grid[row][col - 1]+1
                    col = col-1
        if (counter==0 and (col!=0 or row!=0)): #if it is player ones turn and the last bead does not land in their own bank
            #changes the turn
            counter=1
        elif(counter==1 and (col!=6 or row!=1)): #Vice versa for player 2
            #changes the turn
            counter=0
        check_steal(row, col)

    print(f"grid={grid[c][b]}")
    #runs def that checks the winner
    check_winner()
    #then it updates the text of the code
    update_text()
def update_text():
    #runs a for loop that updates the text to corresponding values of the array
    for i in range(2):
        for j in range(7):
            buttons[i][j].config(text=f"{grid[i][j]}")
def check_steal(row, col):
    print(f"its running {row} {col}")
    if ((row==1) and (counter==1)) or ((row==0) and (counter==0)):
        return
    if (row==1 and col==6)or(row==0 and col==0):
        return
    if counter == 1 : # if it's player 1 turn
        if grid[row][col] == 1 and grid[1][col-1]>0: # if the last pit is 0
            print(f"steal {row} {col}")
            grid[0][0] = grid[0][0] + grid[row][col] # player 1 mancala adds the token that stole(1)
            grid[0][0] = grid[0][0] + grid[1][col-1] # player 1 mancala adds the stolen tokens
            grid[row][col] = 0 # reset player 1 button to 0
            grid[1][col-1] = 0 # reset player 2 button to 0
    else: # if it's player 2 turn
        if grid[row][col] == 1 and grid[0][col+1]>0:
            print(f"steal {row} {col}")
            grid[1][6] = grid[1][6] + grid[row][col]  # player 2 mancala adds the token that stole(1)
            grid[1][6] = grid[1][6] + grid[0][col+1]  # player 2 mancala adds the stolen tokens
            grid[row][col] = 0  # reset player 2 button to 0
            grid[0][col+1] = 0  # reset player 1 button to 0
def check_winner():
    #makes a for loop that sums all the reamining beads up
    sum=0
    for i in range(6):
        sum=sum+grid[0][i+1]
    sum2=0
    for j in range(6):
        sum2=sum2+grid[1][j]
    #if player 1 is out of beads then it puts all beads in player 2s mancala in
    if(sum==0):
        grid[1][6]=sum2+grid[1][6]
        for j in range(6):
            # sets all the remaining mancalas to 0
            grid[1][j]=0
        #runs def that shows the winner
        show_winner()
    # if player 2 is out of beads then it puts all beads in player 1s mancala in
    elif(sum2==0):
        grid[0][0] = sum + grid[0][0]
        for i in range(6):
            #sets all the remaining mancalas to 0
            grid[0][i + 1]=0
        # runs def that shows the winner
        show_winner()
def show_winner():
    #if the bank of player 1 is greater than player two
    if (grid[0][0] > grid[1][6]):
        #shows the win text box with multiple adjustments
        main.deiconify()
        main.title("Player 1 Wins!")
        text = Label(main, text="PLAYER 1 WINS")
        #creates button that has command to go back to menu
        back = tk.Button(main, width=3, height=3, text=f"BACK", command=back_to_menu)
        back.pack()
        #creates a button that has command to exit both applications
        exit = tk.Button(main, width=3, height=3, text=f"EXIT", command=exit_application)
        exit.pack()
        #adjusts each buttons location
        text.place(x=0,y=0)
        exit.place(x=35, y=30)
        back.place(x=35, y=80)
        # if the bank of player 2 is greater than player one
    elif (grid[0][0] < grid[1][6]):
        # shows the win text box with multiple adjustments
        main.deiconify()
        main.title("Player 2 Wins!")
        text = Label(main, text="PLAYER 2 WINS")
        # creates button that has command to go back to menu
        back = tk.Button(main, width=3, height=3, text=f"BACK", command=back_to_menu)
        back.pack()
        # creates a button that has command to exit both applications
        exit = tk.Button(main, width=3, height=3, text=f"EXIT", command=exit_application)
        exit.pack()
        # adjusts each buttons location
        text.place(x=0, y=0)
        exit.place(x=35, y=30)
        back.place(x=35, y=80)
        #if both banks are equal to eachother
    else:
        # shows the win text box with multiple adjustments
        main.deiconify()
        main.title("Tie")
        text = Label(main, text="TIE")
        # creates button that has command to go back to menu
        back = tk.Button(main, width=3, height=3, text=f"BACK", command=back_to_menu)
        back.pack()
        # creates a button that has command to exit both applications
        exit = tk.Button(main, width=3, height=3, text=f"EXIT", command=exit_application)
        exit.pack()
        # adjusts each buttons location
        text.place(x=0, y=0)
        exit.place(x=35, y=30)
        back.place(x=35, y=80)
def exit_application(): #exits each application
    main.withdraw()
    root.withdraw()
def back_to_menu(): #exits back to the menu
    main.withdraw()
    root.withdraw()
    from start import menu
    menu.deiconify()

# Create a 2x7 grid of buttons
buttons = [[1, 2, 3, 4, 5, 6, 7],[1, 2, 3, 4, 5, 6, 7]]
#creates a 2x7 array of the buttons bead values
grid = [[0, 4, 4, 4, 4, 4, 4],[4, 4, 4, 4, 4, 4, 0]]
def restart(): #this method restarts the game
    #resets the grids to their assigned values at start by using a for loop that traverses each elements
    for i in range(2):
        for j in range(7):
            grid[i][j]=4
            #if it is a bank then it then it sets its value to 0
            if (i == 1 and j == 6)or(i==0 and j==0):
                grid[i][j]=0
    #sets it to player 1s turn
    main.counter=0
    #updates the board text
    update_text()
    #makes the board reappear
    root.deiconify()


#runs a for loop that creates the 2x7 array of buttons and board
for i in range(2):
    #sets b or the col back to zero
    b=0
    for j in range(7):
        #if it is a bank it has seperate rules
        if ((i==0 and j==0)or(i==1 and j==6)):
            #creates button that is larger than other buttons
            button = tk.Button(root, width=12, height=24,text=f"{grid[c][b]}", bg="blue", fg="orange",font=("Helvetica",15,"bold"))
        else:
            #otherwise if it is a normal button or a pit makes it smaller and gives it a command
            button = tk.Button(root, width=12, height=13, text=f"{grid[c][b]}", command=lambda b=b, c=c: button_click(b, c),bg="blue", fg="orange", font=("Helvetica",13,"bold"))
        #iterates the col
        b=b+1
        print(f"{b}")
        #sets its location in a grid
        button.grid(row=i, column=j)
        if (i==0):
            #places the button if row is 0 given settings
            button.place(x=75+j*132,y=20)
        if (i==1):
            # places the button if row is 1 given settings
            button.place(x=207+j*132,y=300)
        if(i==0 and j==0):
            # places the button if row is 0 and is bank given settings
            button.place(x=50, y=0)
        if (i == 1 and j == 6):
            # places the button if row is 1 and is bank given settings
            button.place(x=220 + j * 130, y=0)
        buttons[i][j] = button
    #iterates the row
    c = c + 1
# Start the tkinter main loop
root.mainloop()