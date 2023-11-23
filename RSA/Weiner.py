from fractions import Fraction
from RSA import gcd, modInverse
import math
def convergent(a, b, i):
	#print("inside convergent of {}th iteration:".format(i))
	if (a%b == 0 or i == 1):
		return Fraction(int(a/b), 1)
	return (Fraction(int(a/b), 1) + Fraction(1, convergent(b, int(a%b), i-1)))

def weiner_attack(e, N):
	con = Fraction(e, N)
	#print(type(con))
	i = 0
	d  = None
	while(True):
		#print("{}th iteration:".format(i+1))
		i = i + 1
		con = convergent(e, N, i)
		if(con == Fraction(e, N)):
			break

		#print("printing convergent: ", con)
		k = con.numerator
		d = con.denominator
		#print("d: ",d)
		#d must be even
		if(d%2 !=0 and d!=1):
			#print("passed 1st test of {}th iteration".format(i + 1))
			phi = (e*d - 1)/k 
			#phi must be a whole number
			if phi.is_integer():
				#print("passed 2nd test of {}th iteration, value of phi is {}".format(i+1, phi))
				b = -(N - int(phi) + 1)
				c = N
				a = 1
				#print("b {}, c {}".format(b,c))
				p = (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)
				q = (-b - math.sqrt(b**2 - 4*a*c)) / (2*a)
				#print("p: ",p,"q: ",q,"p*q: ", p*q)
				
				#N = p*q
				if N == p*q:
					#print("passed 3rd test of {}th iteration... breaking loop".format(i+1))
					break
		
		
	
	return d
