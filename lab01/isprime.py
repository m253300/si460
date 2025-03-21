import sys
import math

def isPrime(num):
    bound = math.sqrt(num)
    bound = round(bound+1)
    for i in range(2, bound):
        if num%i==0:
            return False
    return True

if(len(sys.argv) <= 1):
    print("usage: isprime.py ###")
    sys.exit(1)

if(int(sys.argv[1]) > 512):
    print("Choose a number less than 512")
    sys.exit(1)

if(isPrime(int(sys.argv[1]))):
    print("Prime!")
else:
    print("Not Prime!")