import time
import math

def task1():
    ans = 1
    start = time.time()
    for i in range(1,50000):
        ans*=i
    print(time.time()-start)

def task2():
    start = time.time()
    ans = math.factorial(50000)
    print(time.time()-start)

task1()