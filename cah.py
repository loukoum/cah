import sys
import binascii

INIT_SIZE = 128
HASH_SIZE = 256

def str_to_hex(string):
    return format(int(str_to_bin(string), 2), 'x')

def str_to_bin(string):
    return ''.join('{0:08b}'.format(ord(x), 'b') for x in string)

def str_to_intarray(string):
    array = []
    for x in string:
        array.append(int(x))

    return array

def array_to_str(array):
    string = ""

    for c in array:
        string += str(c)

    return string

def xor_arrays(array0, array1):
    array = []

    for i in range(min(len(array0), len(array1))):
        array.append(array0[i] ^ array1[i])

    return array

# Create the initial array of INIT_SIZE size
# If the initial array has lenght > INIT_SIZE
# it cuts it in half and xor the two halfs into one
def create_initial(string):
    array = str_to_intarray(str_to_bin(string))

    while (len(array) > INIT_SIZE):
        array = xor_arrays(array[0:int(len(array) / 2)], array[int(len(array) / 2):])

    array = array + ([0] * (INIT_SIZE - len(array)))

    return array

# return the next state of the abc neighborhood
def get_next_state(a, b, c):
    if (a == 0 and b == 0 and c == 0):
        return 1
    if (a == 0 and b == 0 and c == 1):
        return 0
    if (a == 0 and b == 1 and c == 0):
        return 0
    if (a == 0 and b == 1 and c == 1):
        return 1
    if (a == 1 and b == 0 and c == 0):
        return 0
    if (a == 1 and b == 0 and c == 1):
        return 1
    if (a == 1 and b == 1 and c == 0):
        return 1
    if (a == 1 and b == 1 and c == 1):
        return 0

# Evolve the linear space
def evolve_array(array):
    evo = []
    last = 0

    evo.append(1)
    last = last ^ array[0]

    for i in range(1, len(array) - 1):
        evo.append(get_next_state(array[i - 1], array[i], array[i + 1]))
        last = last ^ array[i]

    last = last ^ array[-1]
    evo.append(last)

    return evo

def create_first_gen(array):
    return array + evolve_array(array)

# Creates the HASH_SIZE * HASH_SIZE grid
# by evolving the linear space HASH_SIZE times
def create_grid(first_gen):
    grid = []
    current_gen = first_gen

    for i in range(0, HASH_SIZE):
        current_gen = evolve_array(current_gen)
        grid.append(current_gen)

    return grid

# Evolve the grid using Conway's GOL rules
def next_grid_state(grid, row, col):
    ones = 0

    for i in range(row - 1, row + 1):
        for j in range(col - 1, col + 1):
            if (i > 0 and i < len(grid) and j > 0 and j < len(grid[i])):
                if (grid[i][j] == 1):
                    ones += 1

    if (grid[i][j] == 0 and ones == 3):
        return 1

    elif (grid[i][j] == 1 and (ones == 2 or ones == 3)):
        return 1
    
    return 0

def evolve_grid(grid):
    evo = []

    for i in range(0, len(grid)):
        evo_row = []
        for j in range(0, len(grid[i])):
            evo_row.append(next_grid_state(grid, i, j))

        evo.append(evo_row)

    return evo

# Creates the hash 
def get_hash(grid):
    hsh = grid[0]

    for i in range(1, len(grid)):
        hsh = xor_arrays(hsh, grid[i])

    hsh[0] = 1

    return hsh

def create_hash(string):
    init_array = create_initial(string)
    first_gen = create_first_gen(init_array)
    grid = create_grid(first_gen)
    grid = evolve_grid(grid)
    hsh = get_hash(grid)
    string_hash = array_to_str(hsh)
    return format(int(string_hash, 2), 'x')

def cah(password, salt, iterations):
    hsh = create_hash(password + salt)

    for i in range(1, iterations):
        hsh = create_hash(hsh)

    return hsh

print(cah(sys.argv[1], sys.argv[2], int(sys.argv[3])))
