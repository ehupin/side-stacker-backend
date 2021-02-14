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
