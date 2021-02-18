import matrix_utils
import pytest
import pprint

def test_get_series_in_list():
    series = [0, 0, 0, 1, 1, 0, 0]
    series_indexes = matrix_utils.get_series_indexes_in_list(series, 1)
    assert len(series_indexes) == 1
    assert series_indexes[0][0] == 3
    assert series_indexes[0][1] == 4

    series = [1, 1, 0, 1, 1, 0, 0]
    series_indexes = matrix_utils.get_series_indexes_in_list(series, 1)
    assert len(series_indexes) == 2
    assert series_indexes[0][0] == 0
    assert series_indexes[0][1] == 1
    assert series_indexes[1][0] == 3
    assert series_indexes[1][1] == 4

    series = [0, 0, 0, 0, 0, 0, 0]
    series_indexes = matrix_utils.get_series_indexes_in_list(series, 1)
    assert len(series_indexes) == 0

    series = [1, 1, 1, 1, 1, 1, 1]
    series_indexes = matrix_utils.get_series_indexes_in_list(series, 1)
    assert len(series_indexes) == 1
    assert series_indexes[0][0] == 0
    assert series_indexes[0][1] == 6


    series = [0, 0, 0, 0, 1, 1, 1]
    series_indexes = matrix_utils.get_series_indexes_in_list(series, 1)
    assert len(series_indexes) == 1
    assert series_indexes[0][0] == 4
    assert series_indexes[0][1] == 6


def test_get_longest_series_neighbor_empty_index_in_list():
    index = matrix_utils.get_longest_series_neighbor_empty_index_in_list([0, 0, 0, 1, 1, 0, 0], 1, 2, neighbor_value=0)
    assert index == 2

    index = matrix_utils.get_longest_series_neighbor_empty_index_in_list([1, 1, 1, 0, 0, 0, 0], 1, 3, neighbor_value=0)
    assert index == 3


def test_blocking_compute_move():
    tested_matrix = [
        [0, 0, 0, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None]]
    row, side = matrix_utils.compute_move(tested_matrix, 1)
    assert row == 0
    assert side == 0

    tested_matrix = [
        [None, None, None, None, 0, 0, 0],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None]]
    row, side = matrix_utils.compute_move(tested_matrix, 1)
    assert row == 0
    assert side == 1


    tested_matrix = [
        [0, None, None, None, None, None, None],
        [0, None, None, None, None, None, None],
        [0, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None]]
    row, side = matrix_utils.compute_move(tested_matrix, 1)
    assert row == 3
    assert side == 0

    tested_matrix = [
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [0, None, None, None, None, None, None],
        [0, None, None, None, None, None, None],
        [0, None, None, None, None, None, None]]
    row, side = matrix_utils.compute_move(tested_matrix, 1)
    assert row == 3
    assert side == 0

    tested_matrix = [
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, 0],
        [None, None, None, None, None, None, 0],
        [None, None, None, None, None, None, 0]]
    row, side = matrix_utils.compute_move(tested_matrix, 1)
    assert row == 3
    assert side == 1

    tested_matrix = [
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, 1, 1],
        [None, None, None, None, 0, 1, 0],
        [None, None, None, None, 0, 1, 0],
        [None, None, None, None, 0, 1, 0]]
    row, side = matrix_utils.compute_move(tested_matrix, 1)
    assert row == 3
    assert side == 1



