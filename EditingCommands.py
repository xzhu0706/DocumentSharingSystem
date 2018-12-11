# Reference:
# https://people.cs.pitt.edu/~kirk/cs1501/Pruhs/Spring2006/assignments/editdistance/Levenshtein%20Distance.htm
# https://web.stanford.edu/class/cs124/lec/med.pdf

import numpy as np

# *****************
#    Functions
# *****************


# return a list containing the minimum edit path
def get_path(path_matrix):
    def aux(i, j):
        if i == 0 and j == 0:
            return
        else:
            temp_path.append([i, j])

        if path_matrix[i][j] == 'U':
            aux(i - 1, j)
        elif path_matrix[i][j] == 'L':
            aux(i, j - 1)
        else:
            aux(i - 1, j - 1)

    temp_path = []
    aux(path_matrix.shape[0] - 1, path_matrix.shape[1] - 1)
    temp_path.reverse()
    return temp_path


def cal_editing_commands(old_content, new_content):
    old_arr = np.array(old_content.split("\n"))
    new_arr = np.array(new_content.split("\n"))

    editing_commands = ''

    # Initialize a matrix to store the minimum edit distance
    dist_matrix = np.zeros((new_arr.size + 1, old_arr.size + 1))
    path_matrix = np.empty((new_arr.size + 1, old_arr.size + 1), dtype='str')
    for i in range(0, old_arr.size + 1):
        dist_matrix[0][i] = i
        path_matrix[0][i] = 'L'
    for i in range(0, new_arr.size + 1):
        dist_matrix[i][0] = i
        path_matrix[i][0] = 'U'
    path_matrix[0][0] = 'O'

    # Find and stroe the min distances in the matrix
    for col in range(1, old_arr.size + 1):
        for row in range(1, new_arr.size + 1):
            if old_arr[col - 1] == new_arr[row - 1]:
                cost = 0
            else:
                cost = 1
            min_cost = min(dist_matrix[row - 1][col] + 1,
                           dist_matrix[row][col - 1] + 1,
                           dist_matrix[row - 1][col - 1] + cost)
            dist_matrix[row][col] = min_cost

            # Find out which operation should be done
            if min_cost == dist_matrix[row - 1][col] + 1:
                path_matrix[row][col] = 'U'  # delete
            elif min_cost == dist_matrix[row][col - 1] + 1:
                path_matrix[row][col] = 'L'  # add
            else:
                path_matrix[row][col] = 'D'  # update

    path = get_path(path_matrix)
    delete_count = 0
    for pair in path:
        if path_matrix[pair[0]][pair[1]] == 'U':
            editing_commands += 'delete ' + str(pair[0] - 1) + ';'
            delete_count += 1
        elif path_matrix[pair[0]][pair[1]] == 'L':
            editing_commands += 'add ' + str(pair[0] - 1) + ' ' + str(old_arr[pair[0] - delete_count]) + ';'
        elif (path_matrix[pair[0]][pair[1]] == 'D'
              and dist_matrix[pair[0]][pair[1]] > dist_matrix[pair[0] - 1][pair[1] - 1]):
            editing_commands += 'update ' + str(pair[0] - 1) + ' ' + str(old_arr[pair[0] - delete_count - 1]) + ';'

    print(dist_matrix)
    print(path_matrix)
    print(path)
    print(editing_commands)
    return editing_commands


def editing_commands_to_content(editing_commands, based_on_content):
    commands = editing_commands.split(';')
    new_arr = based_on_content.split('\n')
    # new_arr = based_on_content
    old_arr = new_arr[:]
    # split the commands into lists
    for i in range(0, len(commands)):
        commands[i] = commands[i].split()
    print(commands)

    for command in commands:
        if command:
            if command[0] == 'delete':
                old_arr[int(command[1])] = '*'
            elif command[0] == 'update':
                old_arr[int(command[1])] = command[2]
            elif command[0] == 'add':
                old_arr.insert(int(command[1]), command[2])

    print(old_arr)
    return old_arr

