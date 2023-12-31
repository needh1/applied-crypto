from sympy import randprime
import math
from decimal import *
from Crypto.Util.number import getPrime



def gcd(a,b): 
    if a == 0: 
        return b 
    return gcd(b % a, a)

def modInverse(a, m) : 
    m0 = m 
    y = 0
    x = 1
  
    if (m == 1) : 
        return 0
  
    while (a > 1) : 
  
        # q is quotient 
        q = a // m 
  
        t = m 
  
        # m is remainder now, process 
        # same as Euclid's algo 
        m = a % m 
        a = t 
        t = y 
  
        # Update x and y 
        y = x - q * y 
        x = t 
  
  
    # Make x positive 
    if (x < 0) : 
        x = x + m0 
  
    return int(x) 
  
def randomPrime(bits):
	min = math.sqrt(2)*(2**(bits - 1))
	max = 2**(bits)- 1
	p = randprime(min, max)
	return p

def rsa_generate(keysize):
	#accessing the global varialbes
	while True:
		p = randomPrime(keysize/2);
		q = randomPrime(keysize/2);
		phi= (p-1)*(q-1)
		if p<q:
			if q>2*p:
				continue
		if q<p:
			if p>2*q:
				continue
		
		n = p*q
		d=2
		e = None
		while(d<((n**(1/4))/3)):
			if(gcd(d, phi)==1):
				e = modInverse(d, phi)
				break
			d = d + 1
		if e == None:
			continue
		if (gcd(e, phi) == 1 and abs(p-q) >= 2**(keysize/2 - 100) ):
			break
		
	phi = (p-1)*(q-1)
	lambda_= (p-1)*(q-1)/gcd(p-1, q-1)
	print(p)
	print(q)
	print(phi)
	return n, e, d


def rsa_encrypt(m, n ,e):
	return (m**e)%n
	
def rsa_decrypt(c, d ,n):
	return (c**d)%(n)