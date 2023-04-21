
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
import math
import search 
import sokoban


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (11028840, 'Chaz', 'Tan'), (10778209, 'Zach', 'Edwards'), (11039639, 'Harrison', 'Leach') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def is_corner(walls, x, y):
    '''
    Return a boolean after checking if the given x,y coord is classified as a corner in the given warehouse.
    A square is a corner if it has at least one wall adjacent to it vertically and at least one wall adjacent to it horizontally.
    Exceptions are squares with walls on all sides.
    
    '''
    x_adj = [(x-1, y), (x+1, y)]
    y_adj = [(x, y+1), (x, y-1)]
    # check the square in question
    if any(coord in x_adj for coord in walls):
        if any(coord in y_adj for coord in walls):
            # is the square in question surrounded
            if all(coord in walls for coord in x_adj) and all(coord in walls for coord in y_adj):
                # square is surrounded and not a corner
                return False
            else:
                # square is not surrounded and passes corner test
                return True
        else:
            # not both
            return False
    else:
        # not both
        return False

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
        warehouse_string = warehouse_string.replace(char, space_char)

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

    y_index = -1
    for row in warehouse_array:
        y_index += 1
        x_index = -1
        for square in row:
            x_index += 1
            # here, check if the element is inside the warehouse and is a corner
            # if the element is both of these things, add its coords to the reachable_corners list

            # to check if its is reachable non wall element, look at wall coords
            # if at least 1 wall exists either side of the element in the y and x direction, it is inside

            # wall check
            if square == wall_char:
                continue
            else:
                # is the square a corner
                if is_corner(warehouse.walls, x_index, y_index):
                    # it is a corner square so we should check if its inside
                    # if it is inside, it is a reachable corner

                    # collect horizontally colinear walls x indicies on same row
                    x_colin_wall_indices = []
                    for coord in warehouse.walls:
                        if coord[1] == y_index:
                            # the wall is on the same row
                            # record its x position
                            x_colin_wall_indices.append(coord[0])
                    
                    # min and max
                    x_left_most_wall = min(x_colin_wall_indices)
                    x_right_most_wall = max(x_colin_wall_indices)

                    # horizontal check
                    if (x_left_most_wall < x_index < x_right_most_wall):
                        # the square has a wall either side of it

                        # collect vetcially colinear walls y indicies in same column
                        y_colin_wall_indices = []
                        for coord in warehouse.walls:
                            if coord[0] == x_index:
                                # the wall is on the same column
                                # record its y position
                                y_colin_wall_indices.append(coord[1])

                        # min and max
                        y_upper_most_wall = min(y_colin_wall_indices)
                        y_lower_most_wall = max(y_colin_wall_indices)
                        # vertical check
                        if (y_upper_most_wall < y_index < y_lower_most_wall):
                            # the square is a corner, and is inside the warehouse
                            # it is a reachable corner, add it to the list
                            reachable_corners.append([x_index, y_index])

                            # TEST SHOW REACHABLE CORNERS
                            if warehouse_array[y_index][x_index] not in target_chars:
                                warehouse_array[y_index][x_index] = taboo_char
                        else:
                            # it is a corner but not inside vertical range, move to next square
                            continue
                    else:
                        # it is a corner but not inside horizontal range, move to next square
                        continue
                else:
                    # it is not a corner, move to next square
                    continue
    
    # check each reachable corner to see if it has a colinear match in the set
    # a true pair will have nothing but space between them on the segment and any pair with no segment between should be considered
    # once a pair is established
    # check if the line between them, adjacent segment, exists on either side
    # if the segment exists, all squares between the corners that are not targets are taboo
    # add them to the taboo cells list and add the reachable corners that are not targets to the list as well
    # replace all elements with the indicies in the taboo list with 'X' and remove all other elements

    sorted(reachable_corners , key=lambda k: [k[1], k[0]])
    print("CORNERS:")
    print(reachable_corners)

    # vertically co linear check
    corner_set = sorted(reachable_corners , key=lambda k: [k[1], k[0]])
    for corner in corner_set:
        for possible_pair in corner_set:
            distance_between = math.dist(corner, possible_pair)
            if ((corner[0] == possible_pair[0]) and (distance_between>1)):
                # this possible pair is co linear with the corner (y dimension) and has space between the points
                # check if there is a wall segment adjacent to the segment between the points
                segment = []
                left_seg = []
                right_seg = []

                if corner[1]<possible_pair[1]:
                    for delta in range(1, int(distance_between)):
                        segment.append((corner[0], corner[1]+delta))
                else:
                    for delta in range(1, int(distance_between)):
                        segment.append((possible_pair[0], possible_pair[1]+delta))

                for seg_coord in segment:
                    left_seg.append((seg_coord[0]-1, seg_coord[1]))

                for seg_coord in segment:
                    right_seg.append((seg_coord[0]+1, seg_coord[1]))
            
                if ((all(coord in warehouse.walls for coord in left_seg) or all(coord in warehouse.walls for coord in right_seg)) and not (any(coord in warehouse.walls for coord in segment) or any(coord in warehouse.targets for coord in segment))):
                    if (not any(coord in warehouse.targets for coord in segment)) and ((corner[0], corner[1]) not in warehouse.targets) and ((possible_pair[0], possible_pair[1]) not in warehouse.targets):
                        for seg_coord in segment:
                            warehouse_array[seg_coord[1]][seg_coord[0]] = taboo_char
        corner_set.remove(corner)

    # horizontal colinear check
    corner_set = sorted(reachable_corners , key=lambda k: [k[1], k[0]])
    for corner in corner_set:
        for possible_pair in corner_set:
            distance_between = math.dist(corner, possible_pair)
            print("Checking "+str(corner)+" against "+str(possible_pair)+ " distance = "+str(distance_between))
            if ((corner[1] == possible_pair[1]) and (distance_between>1)):
                # this possible pair is co linear with the corner (x dimension) and has space between the points
                # check if there is a wall segment adjacent to the segment between the points
                segment = []
                top_seg = []
                bottom_seg = []

                if corner[0]<possible_pair[0]:
                    for delta in range(1, int(distance_between)):
                        segment.append((corner[0]+delta, corner[1]))
                else:
                    for delta in range(1, int(distance_between)):
                        segment.append((possible_pair[0]+delta, possible_pair[1]))

                for seg_coord in segment:
                    top_seg.append((seg_coord[0], seg_coord[1]-1))

                for seg_coord in segment:
                    bottom_seg.append((seg_coord[0], seg_coord[1]+1))
                
                print(str(corner) + ' is co linear with ' + str(possible_pair))
                print(segment)

                if ((all(coord in warehouse.walls for coord in top_seg) or all(coord in warehouse.walls for coord in bottom_seg)) and not (any(coord in warehouse.walls for coord in segment) or any(coord in warehouse.targets for coord in segment))):
                    if (not any(coord in warehouse.targets for coord in segment)) and ((corner[0], corner[1]) not in warehouse.targets) and ((possible_pair[0], possible_pair[1]) not in warehouse.targets):
                        for seg_coord in segment:
                            warehouse_array[seg_coord[1]][seg_coord[0]] = taboo_char
        corner_set.remove(corner)

    # condense array back into string
    # condense each line
    warehouse_lines = []
    for row in warehouse_array:
        warehouse_lines.append(''.join(row))

    # join each line to make one string
    warehouse_string = '\n'.join(warehouse_lines)

    # remove unessessary symbols
    for char in target_chars:
        warehouse_string = warehouse_string.replace(char, space_char)

    # return string representation
    return warehouse_string


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
        #print(warehouse.boxes)
        #print(warehouse.targets)
        # Converts start state to goal state excluding worker.
        warehouse_str = warehouse.__str__()
        warehouse_str = warehouse_str.replace(".", "*")
        warehouse_str = warehouse_str.replace("@", " ").replace("$", " ")
        self.goal_state = warehouse_str

        # Generates all the possible combinations of a box on a target. Generates a tuple [[[(Box Start Cords), Weight], Target Cords]]
        # To index the box start cords you would do this goal_nodes[0][0][0]
        # To index the weight you would do this goal_nodes[0][0][1]
        # Finally to index the target cords you would do this goal_nodes[0][1][0] 
    
        #self.goal_states = []
        #i=0
        #for c1 in warehouse.boxes:
        #    c1 = [c1, warehouse.weights[i]]
        #    for c2 in warehouse.targets:
        #        self.goal_states.append([c1, c2])
        #    i += 1

        #DEBUG
        #print(self.goal_state)

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """
        worker = state.worker
        #if (up, down, left, right) in state.walls:
        # Define the possible directions
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # down, up left, right

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

    # Creates a warehouse object of the resulting state after action. Will have to convert current warehouse to string, compute new state, covert back to warehouse object.
    def result(self, state, action):
        raise NotImplementedError
    
    def print_solution(self, goal_node):
        print(goal_node)

    def goal_test(self, state):
        if state in self.goal_states:
            return 
        
    def path_cost(self, c, state1, action, state2):
        return c + 1 + state1.weights
    
    def h(self, n):
        target_box_arr =[] # This array will store (box, target, distWorkerBox + distBoxTarget*boxWeight)
        used_target = [] # This array will store targets with a box on them
        satisfied_box = [] # This array will store boxes that have been placed on a target
        # check through every box
        for i, box_pos in enumerate(wh.boxes):
            # check through every target for each box
            for j, tar_pos in enumerate(wh.targets):
                # find distance of box to target
                if wh.weights[i] == 0:
                    weight_dist = dist(box_pos, tar_pos)
                else:
                    weight_dist = dist(box_pos, tar_pos) * wh.weights[i]
                # if a box is on a target, take note of both
                if weight_dist == 0:
                    satisfied_box.append(i)
                    used_target.append(j)
                target_box_arr.append((i, j, dist(wh.worker, box_pos) + weight_dist))

        # will be used to find what value to return
        h_candidates = []
        for i in range(len(target_box_arr)):
            # if a box is satisfied or a target is used, we no longer need to check for it
            if target_box_arr[i][0] in satisfied_box or target_box_arr[i][1] in used_target:
                pass
            else:
                h_candidates.append(target_box_arr[i])

        # sorts by distWorkerBox + distBoxTarget*boxWeight
        h_candidates.sort(key=lambda a: a[2])
        return h_candidates[0][2]
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

## Helper functions
def dist(coor1, coor2):
    return np.sqrt(((coor2[0] - coor1[0]) ** 2) +((coor2[1] - coor1[1]) ** 2))

from sokoban import Warehouse
if __name__ == "__main__":
    wh = Warehouse()
    

    '''
    wh.load_warehouse("./warehouses/warehouse_155.txt")
    print(wh.walls)
    Puzzle = SokobanPuzzle(wh)
    print(Puzzle.goal_states[0][0][1]) #How to index the weight of the box of one of the possible goal states
    Puzzle.actions(wh)
    '''

    # Harry TESTS
   
    wh.load_warehouse("./warehouses/warehouse_01_a.txt")
    
    target_box_arr =[] # This array will store (box, target, distWorkerBox + distBoxTarget*boxWeight)
    used_target = [] # This array will store targets with a box on them
    satisfied_box = [] # This array will store boxes that have been placed on a target
    # check through every box
    for i, box_pos in enumerate(wh.boxes):
        # check through every target for each box
        for j, tar_pos in enumerate(wh.targets):
            # find distance of box to target
            if wh.weights[i] == 0:
                weight_dist = dist(box_pos, tar_pos)
            else:
                weight_dist = dist(box_pos, tar_pos) * wh.weights[i]
            # if a box is on a target, take note of both
            if weight_dist == 0:
                satisfied_box.append(i)
                used_target.append(j)
            target_box_arr.append((i, j, dist(wh.worker, box_pos) + weight_dist))

    # will be used to find what value to return
    h_candidates = []
    for i in range(len(target_box_arr)):
        # if a box is satisfied or a target is used, we no longer need to check for it
        if target_box_arr[i][0] in satisfied_box or target_box_arr[i][1] in used_target:
            pass
        else:
            h_candidates.append(target_box_arr[i])

    # sorts by distWorkerBox + distBoxTarget*boxWeight
    h_candidates.sort(key=lambda a: a[2])
    print(h_candidates[0][2])
            

    # CHAZ TESTS
    wh.load_warehouse("./warehouses/warehouse_155.txt")
    Puzzle = SokobanPuzzle(wh)
    #wh.load_warehouse("./warehouses/warehouse_125.txt")
    #print(wh.walls)
    #print(wh.__str__())
    #print("\n")
    #print(taboo_cells(wh))
    #print("\n")
    #print(wh.__str__())

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

