import random
import os,sys
import random
import numpy 
from PIL import Image
from tkinter.filedialog import askopenfilename
import sympy.ntheory as nt
from tkinter.filedialog import asksaveasfilename
import pathlib


#isCoprime--------------------------------------------------

def isCoPrime(p, q):
    """
        return True if gcd(p, q) is 1
        relatively prime
    """

    return gcd(p, q) == 1
#--------------------------------------------------------------
def gcd(p, q):
    """
        euclidean algorithm to find gcd of p and q
    """

    while q:
        p, q = q, p % q
    return p

#invmod+egcd----------------------------------------------

def egcd(a, b):  
    # Base Case  
    if a == 0 :   
        return b,0,1
             
    gcd,x1,y1 = egcd(b%a, a)  
     
    # Update x and y using results of recursive  
    # call  
    x = y1 - (b//a) * x1  
    y = x1

    
     
    return gcd,x,y 
#----------------------------------------------------------------------
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
#-------------------------------------------------------------------
   
def generateKey(size):
   
     p = nt.randprime(2 ** (size - 1),2 **  size  - 1)
     q = nt.randprime(2 ** (size - 1),2 ** size - 1)
     n = p*q

     phiN = (p - 1) * (q - 1) # totient

     # choose e
     # e is coprime with phiN & 1 < e <= phiN
     while True:
          e = random.randrange(2 ** (size - 1), 2 **  size - 1)
          if (isCoPrime(e, phiN)):
              break

     # choose d
     # d is mod inv of e with respect to phiN, e * d (mod phiN) = 1
     d = modinv(e, phiN)
     return p,q,n,phiN,e,d
#-------------------------------------------------------------------------------------------------
def encrypt(m,e,N): 

    return  pow(m, e, N)
#-------------------------------------------------------------------------------------------------

def decrypt(c,d,N): 

    return  pow(c, d, N)
#-------------------------------------------------------------------------------------------------


def main():
    
 
     p,q,n,phiN,e,d = generateKey(12)
 
    # print(f"p: {p}")
    # print(f"q: {q}")
    # print(f"n: {n}")
    # print(f"phiN: {phiN}")
    # print(f"d: {d}")
     pu='('+str(e)+','+str(n)+')'
     pr='('+str(d)+','+str(n)+')'
     print("PublicKey(E,N) is ",pu)
     print("PrivetKey(D,N) is ",pr)


     fileName = askopenfilename()
     jpgfile = Image.open(fileName)
     row,col = jpgfile.size
     pixels = jpgfile.load()
     
     enc = [[0 for x in range(row)] for y in range(col)]
     dec = [[0 for x in range(row)] for y in range(col)]
  
     print("Encrypting...")
     for i in range(col):
             for j in range(row):
                     r,g,b = pixels[j,i]
                     r1 = encrypt(r,e,n)
                     g1 = encrypt(g,e,n)
                     b1 = encrypt(b,e,n)
                     enc[i][j] = [r1,g1,b1]
     
    # print (pixels[row-1,col-1])
    
    
     img = numpy.array(enc,dtype = numpy.uint8)
     img1 = Image.fromarray(img,"RGB")
     img1.save('CipherImage.jpg')
     #pixels2 = img1.load()
     print("Show Cipher image")
     img1.show()
#------------------------DECRYPT--------------------------------------------------------
     

     print("Decrypting...")

     for i in range(col):
	     for j in range(row):
		     r,g,b = enc[i][j]
		     r1 = decrypt(r,d,n)
		     g1 = decrypt(g,d,n)
		     b1 = decrypt(b,d,n)
		     dec[i][j] = [r1,g1,b1]
     img2 = numpy.array(dec,dtype = numpy.uint8)
     img3 = Image.fromarray(img2,"RGB")
     print("show Original image")
     img3.show()
     img3.save('OriginalImage.jpg')
     j = Image.open("OriginalImage.jpg")


     p = j.load()
     print (p[row-1,col-1])
#-----------------------------------------MAIN-----------------------------------------------------
main()
