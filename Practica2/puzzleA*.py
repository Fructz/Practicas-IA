#!/usr/bin/env python3

import tkinter as tk 
import heapq

class PuzzleGUI():

    def __init__(self, initial_state, solution_path):
        self.state = initial_state
        self.path = solution_path
        self.root = tk.Tk() # Create the principal window
        self.root.title("15 Puzzle") # Title
        self.buttons = [] # Create a list to save buttons
        self.draw_grid() # Starting to drawing 

        # Button start
        start_btn = tk.Button(self.root, text="Start", command=self.start_animation) # Create button with text 'Start' and call function 'start_animation'
        start_btn.grid(row=4, column=0, columnspan=4, sticky="we") # Styles of the button start

    def draw_grid(self):
        for i in range(16):
            val = self.state[i] # Get the current value for each
            text = str(val) if val != 0 else " " # Convert to string the val variable to better the structure and the conditional is for print empty if we have a 0
            btn = tk.Button(self.root, text=text, width = 5, height = 2, font = ("Arial", 16)) # Specific requirements to create a simple window
            btn.grid(row=i//4, column = i%4)
            self.buttons.append(btn) # To add the buttons with all requirements
        
    def update_board(self, state):
        for i in range(16):
            val = state[i] # For each element
            self.buttons[i]['text'] = str(val) if val != 0 else " " # Change each text depend of his value
        self.root.update() # refresh

    def start_animation(self):
        self.animation(0)

    def animation(self, index):
        if index < len(self.path):
            self.update_board(self.path[index])
            self.root.after(500, self.animation, index + 1)

    def run(self):
        self.root.mainloop() # Loop to still in the program (until the user quit the window)

class PuzzleList():
    
    def __init__(self, state=None):
        self.state = state if state else [] # If the list not recieve data -> is empty
    
    # Request User to enter 15 numbers to resolve the puzzle
    def requestList(self):
        self.state = [] # Create empty list
        while len(self.state) < 16:
            try:
                val = int(input(f"Enter index[{len(self.state)}]: ")) 
                if val < 0 or val > 15:
                    print(f"[!] Invalid Number, the range is [0-15]") # If the user put numbers greather than 15 or less than 0
                    continue
                if val in self.state:
                    print(f"[!] Invalid number, already on the list") # If the user put 1 number that already exists on the list
                    continue
                self.state.append(val) # Add each element
            except ValueError:
                print(f"[!] Incorrect input, try again...\n") # If the user put strange characters

    def print_state(self, state):
        for i in range(0,16,4):
            print(state[i:i+4]) # Print each element

    # Get the state when value of index is 0
    def get_empty(self, state):
        return state.index(0) # return the value of 0
    
    def get_neighbors(self, state):
        neighbors = [] # Create a empty list to save the neighbors
        emptyx = self.get_empty(state) # We can support with the function that we already have 'get_empty'
        row, col = emptyx // 4, emptyx % 4 # Get the row and column exactly when the '0' already there in the list
        # How '//' and '%' works? Well, for example:
        # When we have 16 // 4 is for count, how many times can you multiply 4 to get 16, in this case, it will be '4', because 4 * 4 is 16
        # When we have 11 // 4 is for the rest, we know that -> 4 * 2 = 8, in this case we do not have to multiply for 4, because is greather than (16 > 11) so the rest is 3 (11-8)
        moves = [(-1,0),(1,0),(0,1),(0,-1)] # Up, left, right, down

        for rd, cd in moves: # For each direction in row and columns, move in literally list 'moves', rd = row direction, cd = column direction
            new_row = row + rd # Get the current index to get the position with sum of current row and rd
            new_column = col + cd # Get the current index to get the position with sum of current column and cd
            if 0 <= new_row < 4 and 0 <= new_column < 4:
                new_index = new_row * 4 + new_column # Convert new position to lineal index
                new_state = state.copy() # Copy the current list to save 
                new_state[emptyx], new_state[new_index] =  new_state[new_index], new_state[emptyx] # Change 0 to the number of new position, SWAP
                neighbors.append(new_state) # Add the data in neighbors list
        return neighbors
    
    def calculate_manhattan_distance(self, state):
        total_manhattan_distance = 0 # This variable will help us to add the final correct distance
        for i in range(16):
            card = state[i] # We add the card to assign the first value and continue iterating
            if card != 0: # Ignorate the '0' card
                current_row, current_col = i // 4, i % 4 # To get the current position for each card
                objective_row, objective_col = (card - 1) // 4, (card - 1) % 4 # Find the objetive position of the card, like if we have the first element (1) so -> (0,0)
                total_manhattan_distance += abs(current_row - objective_row) + abs(current_col - objective_col)# both Rows + both Columns -> both in absolute (because it could be negative number )
        return total_manhattan_distance
    
    def AlgorithmA(self, inicial_state):
        expective = [1,2,3,4, 
                     5,6,7,8,
                     9,10,11,12,
                     13,14,15,0] # List that we want to arrive
        open_set = [] # First list
        closed_set = set() # We use set to use tuples to save nodes visited

        g = 0 # actual cost (how much does it cost me for each step)
        h = self.calculate_manhattan_distance(inicial_state) # Calculate with function manhattan to get all the values for each node
        f = g + h # Calculate sum of actual cost and heuristics
        path = [] # A simple list to save each step -> like 0 (0,1) -> (0,2)

        heapq.heappush(open_set, (f, g, inicial_state, path)) # Save all the heuristics in open_set

        while open_set: 
            f, g, state, path = heapq.heappop(open_set) # Extract the less state for get the best way to arrive 

            # if is the objective, we finish
            if state == expective:
                return path + [state] # return the puzzle result and all the ways to achieve the result
            
            closed_set.add(tuple(state)) # Current node like visited
            
            for neighbor in self.get_neighbors(state):
                if tuple(neighbor) in closed_set: # If we already visited, continue
                    continue

                new_g = g + 1 # New value of g (iterative)
                new_h = self.calculate_manhattan_distance(neighbor) # Calculate for each neigbors (up, down, left, right)
                new_f = new_g + new_h

                heapq.heappush(open_set, (new_f, new_g, neighbor, path + [state]))
        
        return None

# ---------------- Main ----------------
if __name__ == "__main__":
    try:
        puzzle = PuzzleList()
        puzzle.requestList()
        solution_path = puzzle.AlgorithmA(puzzle.state)

        if solution_path:
            gui = PuzzleGUI(solution_path[0], solution_path)
            gui.run()
        else:
            print("No solution")
    except KeyboardInterrupt:
        print(f"[!] Keyboard was interrupted, leaving...")
