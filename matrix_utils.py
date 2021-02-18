import random

def matrix_has_value(matrix, value):
    """ Return True if value if found in given matrix

    :param matrix: the 2d matrix in which to lookup
    :type matrix: `list' of `list`

    :param value: the value to search
    :type value: any

    :return: True if value if foundm else False
    :type: `bool`
    """
    for row in matrix:
        if value in row:
            return True
    return False


def get_matrix_column(matrix, column_index):
    """Return given matrix column as a list

    :param matrix: the 2d matrix to process
    :type matrix: `list' of `list`

    :param column_index: the index of the column to get from matrix
    :type column_index: `int`

    :return: the column as a list
    :rtype: `list`
    """
    column = []
    for row in matrix:
        column.append(row[column_index])
    return column


def get_matrix_diagonal(matrix, cell_row_index, cell_column_index, direction=1):
    """Return given matrix diagonal as a list

    The returned diagonal is based on a targeted cell, and a direction
    (from top-left to bottom-right or top-right to bottom-left)

    :param matrix: the 2d matrix to process
    :type matrix: `list' of `list`

    :param cell_row_index: the row index of the targeted cell in matrix
    :type cell_row_index: `int`

    :param cell_column_index: the column index of the targeted cell in matrix
    :type cell_column_index: `int`

    :param direction: the direction of the diagonal to return,
                      either 1(default) for TL-BR diagonal or -1 for TR-BL diagonal
    :type direction: `int`

    :return: the diagonal as a list
    :rtype: `list`
    """
    diagonal = []
    for row_index, row in enumerate(matrix):
        column_offset = (row_index - cell_row_index) * direction
        column_index = cell_column_index + column_offset
        if 0 <= column_index < len(row):
            diagonal.append(row[column_index])
    return diagonal


def list_has_series(list_, value, length):
    """ Return True if given value is found n time (length) in given list

    :param list_: the list in which to lookup
    :type list_: `list'

    :param value: the value to search
    :type value: any

    :param length: the length of the series to search
    :type length: `int`

    :return: True if value if found else False
    :type: `bool`
    """
    count = 0
    for i in list_:
        if i != value:
            count = 0
            continue
        count += 1
        if count == length:
            return True
    return False


def matrix_has_line(matrix, value, row_index, column_index, length):
    """ Return True if a line of given value and given length is found in given matrix.

    This function is supposed to be run after a matrix cell update, hence cell coordinates are provided to
    optimise the lookup in the matrix (i.e. only line passing through this cell are analysed)

    :param matrix: the 2d matrix in which to lookup
    :type matrix: `list' of `list`

    :param value: the value to search
    :type value: any

    :param row_index: the row index of the targeted cell in matrix
    :type row_index: `int`

    :param column_index: the column index of the targeted cell in matrix
    :type column_index: `int`

    :param length: the length of the line to search
    :type length: `int`

    :return: True if value if found else False
    :type: `bool`
    """
    row = matrix[row_index]
    if list_has_series(row, value, length):
        return True

    column = get_matrix_column(matrix, column_index)
    if list_has_series(column, value, length):
        return True

    diag_1 = get_matrix_diagonal(matrix, row_index, column_index)
    if list_has_series(diag_1, value, length):
        return True

    diag_2 = get_matrix_diagonal(matrix, row_index, column_index, direction=-1)
    if list_has_series(diag_2, value, length):
        return True

    return False


def get_series_indexes_in_list(list_, value):
    """ Return 2 int tuple with first and last index for each serie of given value in list_

    E.g.
    >>> get_series_indexes_in_list([1, 1, 0, 1, 1, 0, 0], 1)
    [[0,1],[3,4]]

    :param list_: the list to inspect
    :type list_: `list`

    :param value: the value to search
    :type value: any

    :return: list of tuples with first and last index for each serie
    :type: `list` of `tuple` of `int`
    """
    series_indexes = []
    for i in range(len(list_)):
        if series_indexes and len(series_indexes[-1]) < 2:
            current_series = series_indexes[-1]
        else:
            current_series = []


        if list_[i] == value:
            if not current_series:
                current_series.append(i)
                series_indexes.append(current_series)
            if i == len(list_)-1:
                current_series.append(i)
        else:
            if len(current_series) == 1:
                current_series.append(i-1)
    return [tuple(i) for i in series_indexes]


def get_longest_series_indexes_in_list(list_, value):
    """ Return first and last index for longest serie of given value in given list

    :param list_: the list to inspect
    :type list_: `list`

    :param value: the value to search
    :type value: any

    :return: tuple with first and last index for each serie
    :type: `tuple` of `int`
    """
    series_indexes = get_series_indexes_in_list(list_, value)

    if not series_indexes:
        return

    max_length = 0
    longest_series_indexes = None
    for indexes in series_indexes:
        length = indexes[1] - indexes[0] + 1
        if length > max_length:
            max_length = length
            longest_series_indexes = indexes

    return longest_series_indexes


def get_longest_series_neighbor_empty_index_in_list(list_, value, series_length_threshold, neighbor_value=None):
    """ Return first neighbour index with value None for longest serie of given value in given list

        E.g.
    >>> get_longest_series_neighbor_empty_index_in_list([0, 0, 0, 1, 1, 0, 0], 1, 2, neighbor_value=0)
    2
    >>> get_longest_series_neighbor_empty_index_in_list([1, 1, 1, 0, 0, 0, 0], 1, 3, neighbor_value=0)
    3

    :param list_: the list to inspect
    :type list_: `list`

    :param value: the value to search
    :type value: any

    :param series_length_threshold: the minimal length for a serie to be considered valid
    :type series_length_threshold: `int`

    :param neighbor_value: the value the neighbor index must match to be considered valid
    :type neighbor_value: any

    :return: None or neighbor index
    :rtype: `None` or `int`
    """
    series_indexes = get_longest_series_indexes_in_list(list_, value)

    if not series_indexes:
        return
    length = series_indexes[1] - series_indexes[0] + 1

    if length < series_length_threshold:
        return

    indexes = []
    if series_indexes[0] != 0:
        indexes.append(series_indexes[0] - 1)
    if series_indexes[1] != len(list_) - 1:
        indexes.append(series_indexes[1] + 1)

    for index in indexes:
        if list_[index] == neighbor_value:
            return index

def get_playable_side_for_index_in_list(list_, index):
    """ Return the side to play as int so next move on given list will fill given index

    :param list_: the list to inspect
    :type list_: `list`

    :param index: the index to reach
    :type index: `int`

    :return: the side to play, 0 for the left, 1 for the right
    :rtype: `int`
    """
    first_none_index_from_left = None
    for i, value in enumerate(list_):
        if value is None:
            first_none_index_from_left = i
            break

    return 1 if first_none_index_from_left < index else 0



def compute_move(matrix, player_id):
    """ Return a tuple for the next move to play for given matrix and player id

    So far, this function will only attempt to block series of 3 similar values,
    on vertical and horizontal lines.

    :param matrix: the matrix to inspect
    :type matrix: `list` or `list`

    :param index: the of of the player that is about to move
    :type index: `int`

    :return:
    """
    opponent_player_id = 0 if player_id == 1 else 1

    series_length_threshold = 3

    for row_index, row in enumerate(matrix):
        column_index = get_longest_series_neighbor_empty_index_in_list(row, opponent_player_id, series_length_threshold)
        if column_index:
            side = get_playable_side_for_index_in_list(row, column_index)
            return row_index, side

    for column_index in range(len(matrix)):
        column = get_matrix_column(matrix, column_index)
        row_index = get_longest_series_neighbor_empty_index_in_list(column, opponent_player_id, series_length_threshold)
        if row_index:
            row = matrix[row_index]
            side = get_playable_side_for_index_in_list(row, column_index)
            return row_index, side

    row_indexes = list(range(len(matrix)))
    random.shuffle(row_indexes)
    for row_index in row_indexes:
        if None in matrix[row_index]:
            side = random.randint(0, 1)
            return row_index, side

