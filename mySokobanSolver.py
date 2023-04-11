
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2022-03-27  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
from itertools import combinations
import numpy as np
import search 
import sokoban


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (11028840, 'Chaz', 'Tan'), (10778209, 'Zach', 'Edwards'), (11039639, 'Harrison', 'Leach') ]
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag an 
    outside cell as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with the worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''

    '''
    Compute reachable cells in (x, y) tuple set. 
        A reachable cell falls within the outline of the outer most walls.
        Get a string representation of the warehouse and replace all chars that are not the walls and targets.
        Convert the warehouse into a list of lines by splitting over the line break \n.
            Go through each line from left to right, once a wall is encountered, if the next space is not a wall, start adding the coords to the set.
            Once a wall has been encountered again, and there are no more walls left on the line, then all the reachable squares for that line have been added.

    Compute reachable corners from within reachable cells set. 
        A corner has at least 1 wall above or below and at least one wall left or right.
        These are taboo.

    Consider all co-linear corners.
        Co liniear corners will have one coordinate in common and one different.
        A co linear corner pair will have a segment along/ adjacent to a wall between the corners.
        Any square between a co linear corner pair that is not a target is taboo.
    
    Use the list of lines represenation to implement the replacements at the given coords for the taboo squares.
    Convert back from list of lines to one string representation and return.
    '''

    # define char constants
    target_chars = ['.', '!', '*']
    removable_chars = ['$', '@']
    wall_char = '#'
    space_char = ' '
    taboo_char = 'X'

    # get string representation of warehouse
    warehouse_string = warehouse.__str__()

    # remove unessessary symbols
    for char in removable_chars:
        warehouse_string = warehouse_string.replace(char, " ")

    # split string into array of lines
    warehouse_lines = warehouse_string.split("\n")
    
    # each line in ware_house lines needs to be split into lists of individual chars
    warehouse_array = []
    for row in warehouse_lines:
        temp = []
        for char in row:
            temp.append(char)
        warehouse_array.append(temp)

    # should be left with
    # [
    # [' ', '#', '#', '#'], 
    # [line 2], 
    # [line 3]
    # ]

    # so index 1 is the row number and index 2 in the column number

    # iterate over 2d array and check between second to second last rows 
    # and second to second last columns if the elements
    # have wall chars either side of them in both directions.
    # If they do, these are considered inside the warehouse

    # we know the coords of the walls in self.walls
    # index in 2d array maps correctly but reversed array[y][x]

    reachable_corners = []

    for row in warehouse_array:
        for square in row:
            x_index = warehouse_array.index(row)
            y_index = row.index(square)
            # here, check if the element is inside the warehouse and is a corner
            # if the element is both of these things, add its coords to the reachable_corners list

            # to check if its is reachable non wall element, look at wall coords
            # if at least 1 wall exists either side of the element in the y and x direction, it is inside

            # wall check
            if square == wall_char:
                continue
            else:
                # collect horizontally colinear walls from warehouse.walls
                x_colin_wall_indices = []

                # min and max
                x_left_most_wall = min(x_colin_wall_indices)
                x_right_most_wall = max(x_colin_wall_indices)

                # collect vetcially colinear walls from warehouse.walls
                y_colin_wall_indices = []

                # min and max
                y_upper_most_wall = min(y_colin_wall_indices)
                y_lower_most_wall = max(y_colin_wall_indices)

                # horizontal check
                if (x_left_most_wall < x_index < x_right_most_wall):
                    # the square has a wall either side of it

                    # vertical check
                    if (y_upper_most_wall < y_index < y_lower_most_wall):
                        pass
                    else:
                        pass
                    pass
                else:
                    # not inside, move on
                    continue


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes

    
    def __init__(self, warehouse):
        #Do we need more information stored for the start_node?
        self.start_state = warehouse

        #DEBUG
        print(warehouse.boxes)
        print(warehouse.targets)


        # Generates all the possible combinations of a box on a target. Generates a tuple [[[(Box Start Cords), Weight], Target Cords]]
        # To index the box start cords you would do this goal_nodes[0][0][0]
        # To index the weight you would do this goal_nodes[0][0][1]
        # Finally to index the target cords you would do this goal_nodes[0][1][0]
        self.goal_states = []
        i=0
        for c1 in warehouse.boxes:
            c1 = [c1, warehouse.weights[i]]
            for c2 in warehouse.targets:
                self.goal_states.append([c1, c2])
            i += 1

        #DEBUG
        print(self.goal_states)

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """
        worker = state.worker
        #if (up, down, left, right) in state.walls:
        # Define the possible directions
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right

        # Initialize the result array with zeros
        actions = [1, 1, 1, 1]

        # Loop through each direction
        for i, direction in enumerate(directions):
            # Calculate the adjacent position based on the direction
            adjacent_pos = [worker[0] + direction[0], worker[1] + direction[1]]
            
            #Cool Hip Adjacent Square Checker, felt cute might turn into function later.
            if tuple(adjacent_pos) in state.walls: # Adjacent_pos made into tuple so in keyword can be used
                # If so, set the corresponding element in the result array to 0
                actions[i] = 0
            elif tuple(adjacent_pos) in state.boxes: #Checks if adjacent square has a box
                next_adjacent = tuple([adjacent_pos[0] + direction[0], adjacent_pos[1] + direction[1]])
                if next_adjacent in (state.boxes or state.walls): #If adjacent square has box then check if next adjacent is a box or wall
                    actions[i] = 0 #If next square a box or wall return 0
        return actions


    def result(self, state, action):
        raise NotImplementedError
    
    def print_solution(self, goal_node):
        raise NotImplementedError
    
    def goal_test(self, state):
        if state in self.goal_states:
            return 
        
    def path_cost(self, c, state1, action, state2):
        raise NotImplementedError
    
    def h(self, n):
        raise NotImplementedError
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    
    raise NotImplementedError()

from sokoban import Warehouse
if __name__ == "__main__":
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_155.txt")
    print(wh.walls)
    Puzzle = SokobanPuzzle(wh)
    print(Puzzle.goal_states[0][0][1]) #How to index the weight of the box of one of the possible goal states
    Puzzle.actions(wh)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

