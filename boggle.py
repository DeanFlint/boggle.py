from string import ascii_uppercase
from random import choice

def make_grid(width, height):
    """
    Creates a grid that will hold all of the
    tiles for a boggle game.
    """
    return {(row, col): choice(ascii_uppercase) 
        for row in range(height)
        for col in range(width)}
        
    
def neighbours_of_position(coords):
    """
    Get neighbours of a given position
    """
    row = coords[0]
    col = coords[1]
    
    # Assign each of the neighbours
    # Top-left to top-right.
    top_left = (row - 1, col - 1)
    top_center = (row - 1, col)
    top_right = (row - 1, col + 1)
    
    # Left to right
    left = (row, col - 1)
    # Center not needed as those co-ordinates are passed to
    # this function.
    right = (row, col + 1)
    
    # Bottom left to bottom right
    bottom_left = (row + 1, col - 1)
    bottom_center = (row + 1, col)
    bottom_right = (row + 1, col + 1)
    
    return [top_left, top_center, top_right, 
            left, right,
            bottom_left, bottom_center, bottom_right]
            
def all_grid_neighbours(grid):
    """
    Get all of the possible neighbours for each position
    in the grid
    """
    neighbours = {}
    for position in grid:
        position_neighbours = neighbours_of_position(position)
        neighbours[position] = [p for p in position_neighbours if p in grid]
    return neighbours
  
    
def path_to_word(grid, path):
    """
    Add all of the letters on the path to a string
    """
    return ''.join([grid[p] for p in path])


def search(grid, dictionary):
    """
    Search through the paths to locate the words by matching
    strings to words in a dictionary
    """
    neighbours = all_grid_neighbours(grid)
    paths = [] 
    full_words, stems = dictionary
    """
    The reason for this is that a letter could be repeated
    in the grid several times if we had two letter A's and we saved 
    a word with an A in it how would we know which A it is.
    """
    
    def do_search(path):
        word = path_to_word(grid, path)
        if word in full_words:
            paths.append(path)
        if word not in stems:
            return
        for next_pos in neighbours[path[-1]]:
            if next_pos not in path:
                do_search(path + [next_pos])
    """
    The do search function can be called by the search
    function and can call itself recursively to build up paths. The search function
    starts to search by passing a single position to the do_search. This is a path
    of one letter. The do_search function converts whatever path that's given into
    a word and checks if it's in the dictionary. If the path makes a word it's
    added to the paths list whether the path is a word or not. do_search gets each of
    the neighbors of the last letter checks to make sure the neighboring letter
    isn't already in the path and then continues the searching from that letter
    """

    for position in grid:
        do_search([position])
        
    """
    So do_search call itself eight times for each
    starting position and again for each of the various neighbors of each neighbor
    and so on.
    """ 

    words = []
    for path in paths:
        words.append(path_to_word(grid, path))
    return set(words)

    """
    For each position in the grid we do a search and convert all the paths
    and make valid words into words and return them in a list.
    A recursive function or data structure is simply one that is defined in terms of itself. 
    In this case we want to search the neighbors or neighbors of positions you can 
    imagine a sort of tree like search space. Trees or tree like data structures are the classic 
    example of where recursion simplifies everything you can imagine a function that searches
    a tree to do so it must search multiple branches but those branches are merely
    smaller trees so the function can pass the branches it must search to itself so
    that they can be searched the end result being that as those branches split and
    so on all of those splits are automatically handled by the search
    function treating each branch the same and searching its children
    """
    
def get_dictionary(dictionary_file):
    """
    Load Dictionary file
    """
    full_words, stems = set(), set()
    
    with open(dictionary_file) as f:
        for word in f:
            word = word.strip().upper()
            full_words.add(word)
            
            for i in range(1, len(word)):
                stems.add(word[:i])
                
    return full_words, stems
        
def main():
    """
    This is the function that will run the whole project
    """
    grid = make_grid(100, 100)
    dictionary = get_dictionary('words.txt')
    words = search(grid, dictionary)
    for word in words:
        print(word)
    print("Found %s words" % len(words))
    
"""
When you import a file it gets executed. Your unit test file
test_boggle.py imports boggle.py and then and in the process
boggle.py gets executed this was fine when boggle.py only contained functions
they got to find but only actually executed by the tests themselves. Now
however you've added a line of code to the bottom of boggle.py that execute
the boggle solver that line of code should only be run when we actually run
boggle.py from the command line it should be ignored if we're simply
importing boggle.py into another file. To avoid running code when the file is
imported we use the following if statement the code within this statement.
will only execute when the file is run directly. In our case we want to
conditionally run the main statement. Now you can run your unit tests without the
whole boggle solver running. 
"""

if __name__ == "__main__":
    main()
