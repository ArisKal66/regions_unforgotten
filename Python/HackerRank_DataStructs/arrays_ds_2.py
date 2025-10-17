#!/bin/python3

import math
import os
import random
import re
import sys
import random
#
# Complete the 'hourglassSum' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY arr as parameter.
#
# practice

def array2dgen():
    return [[random.randint(-9, 9) for _ in range(6)] for _ in range(6)]

arr = array2dgen()
for row in arr:
    print(row)


def hourglassSum_simple(arr):
    max_sum = None  # initial
    
    for i in range(4):
        for j in range(4):
            top = arr[i][j] + arr[i][j+1] + arr[i][j+2]
            middle = arr[i+1][j+1]
            bottom = arr[i+2][j] + arr[i+2][j+1] + arr[i+2][j+2]
            hourglass = top + middle + bottom

            if max_sum is None or hourglass > max_sum:
                max_sum = hourglass

    return max_sum

print(hourglassSum_simple(arr))

def hourglassSum(arr): # final version
    max_sum = -math.inf # initial
    for i in range(len(arr)-2):
        for j in range(len(arr[0])-2):
            top = arr[i][j] + arr[i][j+1] + arr[i][j+2]
            middle = arr[i+1][j+1]
            bottom = arr[i+2][j] + arr[i+2][j+1] + arr[i+2][j+2]
            hourglass = top + middle + bottom
            max_sum = max(max_sum, hourglass)

    return max_sum

print(hourglassSum(arr))

# if __name__ == '__main__':
#     fptr = open(os.environ['OUTPUT_PATH'], 'w')

#     arr = []

#     for _ in range(6):
#         arr.append(list(map(int, input().rstrip().split())))

#     result = hourglassSum(arr)

#     fptr.write(str(result) + '\n')

#     fptr.close()