print(1+32/4*4)

counter = 0

def Fibonacci(n):
    global counter
    if (n <= 2):
        return 1
    #print ("Fibonacci", n)
    counter += 1
    return Fibonacci(n-1) + Fibonacci(n-2)

counter = 0
print (Fibonacci(5), counter)

counter = 0
print (Fibonacci(10), counter)

counter = 0
print (Fibonacci(30), counter)

def FibonacciNR(n):
    fib = [1,1]
    x = 2
    while x<n:
        fib.append(fib[-1] + fib[-2])
        x += 1
    return fib[-1]

print (FibonacciNR(101))

import json

with open("../News_Category_Dataset_v2.json", "r") as ifile:
    categorySet = set()
    lines = ifile.readlines()
    for line in lines:
        d = json.loads(line)
        #print (d)
        if "category" in d:
            categorySet.add(d["category"])
print (len(categorySet), categorySet)