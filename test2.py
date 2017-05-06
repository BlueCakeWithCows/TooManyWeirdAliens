UP, DOWN, LEFT, RIGHT = 'up', 'down', 'left', 'right'

def shift(direction, number, matrix):
    ''' shift given 2D matrix in-place the given number of rows or columns
        in the specified (UP, DOWN, LEFT, RIGHT) direction and return it
    '''
    if direction in (UP, DOWN):
        n =  (number % len(matrix) if direction == UP else
            -(number % len(matrix)))
        h = matrix[:n]
        del matrix[:n]
        matrix.extend(h)
        return matrix
    elif direction in (LEFT, RIGHT):
        n =  (number % len(matrix[0]) if direction == LEFT else
            -(number % len(matrix[0])))
        temp = list(zip(*matrix))
        h = temp[:n]
        del temp[:n]
        temp.extend(h)
        matrix[:] = map(list, zip(*temp))
        return matrix
    else:
        return matrix

if __name__ == '__main__':
    def print_shifted_matrix(direction, number, matrix):
        print(direction + ': ' + (10-2-len(direction))*' ' +
              ('\n' + 10*' ').join(str(row)
                                  for row in shift(direction, number, matrix)))
        print

    matrix1 = [[1, 2, 3, 4],
               [5, 6, 7, 8],
               [9, 10, 11, 12]]

    matrix2 = [[1, 2, 3],
               [4, 5, 6],
               [7, 8, 9],
               [10, 11, 12]]

    for matrix in matrix1, matrix2:
        print_shifted_matrix('original', 0, matrix)
        print_shifted_matrix(UP, 1, matrix)
        print_shifted_matrix(DOWN, 1, matrix)
        print_shifted_matrix(LEFT, 1, matrix)
        print_shifted_matrix(RIGHT, 1, matrix)