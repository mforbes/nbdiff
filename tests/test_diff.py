from nose.tools import eq_
import itertools as it
from nbdiff.diff import (
    add_results,
    find_candidates,
    find_matches,
    process_col,
    check_match,
)


def test_find_candidates():
    A = "abcabba"
    B = "cbabac"
    grid = [
        [False, False, True, False, True, False],
        [False, True, False, True, False, False],
        [True, False, False, False, False, True],
        [False, False, True, False, True, False],
        [False, True, False, True, False, False],
        [False, True, False, True, False, False],
        [False, False, True, False, True, False]
    ]
    print zip(*grid)
    print "\n".join(str(" ".join(c and "X" or "+" for c in row)) for row in zip(*[reversed(col) for col in grid]))
    result = find_candidates(grid)
    expected = {1:[(0,2),(1,1),(2,0)],
                2:[(1,3),(3,2),(4,1)],
                3:[(2,5),(3,4),(4,3),(6,2)],
                4:[(6,4)]}
    eq_(result, expected)


def test_add_results():
    k = {1:[(0,2)]}
    newk = {1:[(1,1)],2:[(1,3)]}
    result = add_results(k, newk)
    expected = {1:[(0,2),(1,1)],2:[(1,3)]}
    eq_(result, expected)


def test_find_matches():
    A = "abcabba"
    B = "cbabac"
    grid = [[a == b for (a, b) in list(it.product(A, B))][i * len(B):i * len(B) + len(B)] for i in range(len(A))]
    k = [[(len(A), len(B))] for x in range(min(len(A), len(B)) + 1)]
    colNum = 0
    result = find_matches(grid[colNum], colNum)
    expected = [(0, 2),(0,4)]
    eq_(result, expected)


def test_process_col():
    d = {1:[(0, 2)]}
    a = [False, True, False, True, False, False]
    col = 1
    expected = {1:[(1,1)], 2:[(1,3)]}
    result = process_col(d, a, col)
    eq_(result, expected)

    d = {}
    a = [False, True, False, True, False, False]
    col = 1
    expected = {1:[(1,1)]}
    result = process_col(d, a, col)
    eq_(result, expected)

    d = {1:[(0,2)]}
    a = [False, True, False, True, False, True]
    col = 1
    expected = {1:[(1,1)], 2:[(1,3)]}
    result = process_col(d, a, col)
    eq_(result, expected)

    d = {1:[(0,2),(1,1),(2,0)], 2:[(1,3)],3:[(2,5)]}
    a = [False, False, False, False, True, False]
    col = 3
    expected = {3:[(3,4)]}
    result = process_col(d, a, col)
    eq_(result, expected)


def test_check_match():
    point = (1,3)
    k = {1:[(0,2)]}
    expected = 2
    result = check_match(point, k)
    eq_(result, expected)

    point = (1,1)
    k = {1:[(0,2)]}
    expected = 1
    result = check_match(point, k)
    eq_(result, expected)

    point = (1,2)
    k = {1:[(0,2)]}
    expected = None
    result = check_match(point, k)
    eq_(result, expected)

    point = (3,4)
    k = {1:[(0,2),(1,1),(2,0)], 2:[(1,3)],3:[(2,5)]}
    expected = 3
    result = check_match(point, k)
    eq_(result, expected)

    point = (2, 0)
    k = {1:[(0,2),(1,1)], 2:[(1,3)]}
    expected = 1
    result = check_match(point, k)
    eq_(result, expected)

    point = (5, 1)
    k = {1: [(0, 2), (1, 1), (2, 0)], 2: [(1, 3), (3, 2), (4, 1)], 3: [(2, 5), (3, 4), (4, 3)]}
    expected = None
    result = check_match(point, k)
    eq_(result, expected)
