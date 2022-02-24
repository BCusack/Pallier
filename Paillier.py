import os

from time import sleep
from math import lcm, gcd,sqrt
os.system('cls' if os.name == 'nt' else 'clear')

"""
Server client communication with Paillier algorithm
@author Brian Cusack
"""
def loading():
    for i in range(3):
        sleep(0.5)
        print('.', end=" ")

def checkGCD(p,q):
    return gcd(p*q,(p-1)*(q-1)) == 1


def isprime(num):
    a=2
    while a <= sqrt(num):
        if num % a < 1:
            return False
        a += a
    return num > 1

def gcdInputValidation():
    while True:
        while True:
            p = int(input("Enter the value for p or press Enter for default value:") or 7)
            if isprime(p):
                print(f"p = {p}")
                break
            else:
                print(f'{p} is not a prime number')
        while True:
            q = int(input("Enter the value for q or press Enter for default value:") or 11)
            if isprime(q):
                print(f"q = {q}")
                break
            else:
                print(f'{q} is not a prime number')
        if checkGCD(p,q):
            break
        else:
            print(f'\n😝 The value of gcd(pq,(p-1)(q-1)) ≠  1')
    n = p * q
    return p,q,n


def getServerInputs():
    """Get values of n and g from server"""
    print("Select two random primes p and q such that the gcd(pq,(p-1)(q-1)) = 1")
    p, q, n = gcdInputValidation()
    while True:
           g = int(input(f"Enter the value for g such that g is relatively prime to n^2 {pow(n,2)}: or press Enter for default value:") or 5652)
           if gcd(g,pow(n,2)) == 1:
               print(f'g = {g}')
               break
           else:
               print(f'\n😝 The value of g {g} is not relatively prime to n^2: {pow(n,2)}')
    return p,q,n, g

# server has private key
def getPrivateKey(p,q,g):
     lmda = lcm(p-1, q-1)
     n = p * q
     u1 = pow(g, lmda, pow(n, 2))
     L_of_u1 = int((u1-1)/n)
     mu = pow(L_of_u1, -1, n)
     print(f'\n🔑 Generate private key'),sleep(1)
     print(f'Calculate λ = lcm(p - 1,q - 1)'),sleep(1)
     print(f'Calculate mu = (L(g^λ mod n2))^-1 mod n'),sleep(1)
     print(f'Server has private key (λ,mu) = ({lmda},{mu})'),sleep(1)
     return lmda,mu

# client encrypts message
def clientEncrytion(n, g, M, r):
    C = pow((g**M)*(r**n),1,n**2)
    print(f'\n🔐 Encrypting message with public key (n,g) and random r: ({n},{g}) and {r}'),sleep(1)
    print(f'Calculate n = pq'),sleep(1)
    print(f'Calculate Ciphertext = (g^M)*(r^n) mod n^2'),sleep(1)
    print(f'Sending Ciphertext: {C} to the server'),loading()
    return C

def decrypt(C,n,Lambda,meu):
    u1 = pow(C,Lambda,n*n)
    L_of_u1 = int((u1-1)/n)
    print(f'\n🔓 Decrypting message with private key (λ,u): {Lambda},{meu}'),sleep(1)
    print(f'Calculate u = C^λ mod n^2 = {u1}'),sleep(1)
    print(f'Calculate L(u) = (u-1)/n = {L_of_u1}'),sleep(1)
    print(f'Calculate M = L(c^λ mod n^2) * (u mod n)'),sleep(1)
    loading()
    return int(pow(L_of_u1 * meu ,1, n))

def getMessage(n):
    """ Get message from user safely"""
    while True:
        # Input Message
        m = int(input(f"\n💌 Enter the value of Message 'm' (as Integer and less than n: {n}): "))
        if m < n:
            break
        else:
            print(f"\n😝 The value of the message {m} must be less than n' {n}"), sleep(1)
    r = int(input("Enter the value of Random 'r' (as Integer): "))
    return m, r


def main():
    # get server public key
    p,q,n, g = getServerInputs()
    M, r = getMessage(n)
    C = clientEncrytion(n, g, M, r)
    # send message to server
    lmbda, mu = getPrivateKey(p,q,g)
    M = decrypt(C,n,lmbda,mu)
    print(f'\n🔓 Decrypted message M = {M}')

if __name__ == "__main__":
    main()