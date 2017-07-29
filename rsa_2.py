#!/usr/bin/python

import math
import sympy

"""
wikilink:https://en.wikipedia.org/wiki/RSA_%28cryptosystem%29

1>Select primes p=11, q=3.

2>n = pq = 11.3 = 33
  phi = (p-1)(q-1) = 10.2 = 20 

3>Choose e=3
  Check gcd(e, p-1) = gcd(3, 10) = 1 (i.e. 3 and 10 have no common factors except 1),
  and check gcd(e, q-1) = gcd(3, 2) = 1
  therefore gcd(e, phi) = gcd(e, (p-1)(q-1)) = gcd(3, 20) = 1

4>Compute d such that ed (triple equql sign) 1 (mod phi)
  i.e. compute d = e-1 mod phi = 3-1 mod 20
  i.e. find a value for d such that phi divides (ed-1)
  i.e. find d such that 20 divides 3d-1
  Simple testing (d = 1, 2, ...) gives d = 7
  Check: ed-1 = 3.7 - 1 = 20, which is divisible by phi.

5>Public key = (n, e) = (33, 3)
  Private key = (n, d) = (33, 7)

TODO:
  optimize and remove naive approach with better algos
"""
def rsa_simple_sample():
  p = 0xB
  q = 0x3
  m = p*q
  e = 0x3
  d = 0x7 

  pt = 0x8
  ct = (pow(pt,e)) % m
  pt_obt = (pow(ct,d)) % m

  print ("ct [%d] pt_obt[%d] == original [%d]" % (ct,pt_obt,pt))


def is_odd(i): return bool(i & 1)

def check_mod0(n,num):
   return bool(n%num)


def egcd(a,b):
  if a == 0:
    return(b,0,1)
  else:
    g,y,x = egcd(b%a, a)
    return (g, x - (b // a)*y, y)


def modinv(a,m):
  g, x, y = egcd(a,m)
  if g != 1:
    print("modular inverse doesnot exist")
  else:
    return x % m



def decrypt_using_private_key(c,e,d,n):
    m = (c**d)%n            #remove this approach
    print "original_data:" + str(m)


def rsa_crack_known_primes_small(p,q,e,n,c):
  print("For known primes p[%d] q[%d] e[%d] n[%d]" % (p, q, e, n))
  print("Highest factor of any number sqrt(N) [%d]"% (math.sqrt(n))) 
  h_factor = int(math.sqrt(n))
  obt_p = p
  obt_q = q
# print("prime numbers are p[%d] and q[%d]" % (obt_p,obt_q))  
  phi_p = (obt_p - 1)
  phi_q = (obt_q - 1)
  obt_phi = phi_p * phi_q
  obt_d = modinv(e,obt_phi) #getting private key component d
  decrypt_using_private_key(c, e, obt_d, n)

    
def rsa_crack_with_unknown_primes(c,e,n):
  print("Highest factor of any number sqrt(N) [%d]"% (math.sqrt(n))) 
  h_factor = int(math.sqrt(n))
   
  if (not is_odd(h_factor)):
    h_factor = h_factor - 1
  
  for i in range(h_factor,1,-2):
    if sympy.isprime(i):
       if(not check_mod0(n,i)):
         print ("prime is [%d]" %(i))
         obt_p = i
           
  obt_q = n/obt_p
  print("prime numbers are p[%d] and q[%d]" % (obt_p,obt_q))  
  phi_p = (obt_p - 1)
  phi_q = (obt_q - 1)
  obt_phi = phi_p * phi_q
  obt_d = modinv(e,obt_phi) #getting private key component d
  decrypt_using_private_key(c, e, obt_d, n)
  

def main():
  #rsa_simple_sample()
  #rsa_crack_known_primes_small(0xB, 0x3, 0x3, 0x21,0x11) #(p,q,e,n,c)
  #rsa_crack_known_primes_small(0x101, 0x151, 0x11, 0x15251,0x30A0) #(c,e,n)
  #rsa_crack_with_unknown_primes(0x30A0, 0x11, 0x15251)
  print " My first python project"
  print " 1>Crack RSA with known primes(p,q) and public key (e,n)"
  print " 2>Crack RSA with unknown small primes and public key (e,n)" 

  choice = int(raw_input("Enter Choice: "))
  print choice

  if choice == 1:
    print "cracking rsa with known primes(p,q) and public (e,n)"
    p = int(raw_input("Prime Factor in hex (p): "))
    q = int(raw_input("Prime Factor in hex (q): "))
    e = int(raw_input("Public key exponent in hex (e): "))
    n = int(raw_input("Modulus in hex (n): "))
    c = int(raw_input("Cipher value in hex (c): "))
    rsa_crack_known_primes_small(p,q,e,n,c)
  elif choice == 2:
    print "cracking rsa with unknown primes and known public key (e,n)"
    e = int(raw_input("Public key exponent in hex (e): "),16)
    n = int(raw_input("Modulus in hex (n): "),16)
    c = int(raw_input("Cipher value in hex (c): "),16)
    rsa_crack_with_unknown_primes(c,e,n)
  else:
    print "No choice"


main();
