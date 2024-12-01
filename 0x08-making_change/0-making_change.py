#!/usr/bin/python3
"""
0-making_change
"""


def makeChange(coins, total):
    """
    makeChange
    """
    if total <= 0:
        return 0

    stop = 0
    tmp = 0
    coins.sort(reverse=True)
    for coin in coins:
        while stop < total:
            stop += coin
            tmp += 1
        if stop == total:
            return tmp
        stop -= coin
        tmp -= 1
    return -1
