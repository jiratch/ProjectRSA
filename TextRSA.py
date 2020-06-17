import base64
import random
import sympy.ntheory as nt 

from tkinter import Tk
from tkinter.filedialog import askopenfilename

from tkinter.filedialog import asksaveasfilename
import filetype
import pathlib
from PIL import Image

import numpy as np


#----------------------------------------------------------------------

def generateKeys(keysize=1024):
    e = d = N = 0

    # get prime nums, p & q
    p = generateLargePrime(keysize)
    q = generateLargePrime(keysize)

   

    N = p * q 
    phiN = (p - 1) * (q - 1) # totient

    # choose e
    # e is coprime with phiN & 1 < e <= phiN
    while True:
        e = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
        if (isCoPrime(e, phiN)):
            break

    # choose d
    # d is mod inv of e with respect to phiN, e * d (mod phiN) = 1
    d = modinv(e, phiN)

    return p,q,e, d, N,phiN
#-----------------------------------------------------------------
def generateLargePrime(keysize):
    """
        return random large prime number of keysize bits in size
    """
    return nt.randprime(2 ** (keysize - 1),2 ** keysize - 1)

#-----------------------------------------------------------------
def isCoPrime(p, q):
    """
        return True if gcd(p, q) is 1
        relatively prime
    """

    return gcd(p, q) == 1
#-----------------------------------------------------------------
def gcd(p, q):
    """
        euclidean algorithm to find gcd of p and q
    """

    while q:
        p, q = q, p % q
    return p

#-----------------------------------------------------------------
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
#----------------------------------------------------------------------------------------------------------------------------------------------
def modinv(a, m):
    g,x,y = egcd(a, m)
  

    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
#-----------------------------------------------------------------------------------------------------------------------------------------------
def encrypt(msg):
    print("Please choose your key")
    fileName = askopenfilename() # show an "Open" dialog box and return the path to the selected file
 
    
    with open(fileName, 'r') as infile:
       string = infile.read()
       n,e = string.split()
       #pub_key has attributes: n: int, e: int
       n = int(n)
       e = int(e)
       infile.close()
       
       
    cipher = ""

    for c in msg:
           m = ord(c)
           cipher += str(pow(m, e, n)) + " "

          
    message = cipher
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')       
        

    return base64_message


#--------------------------------------------------------------------------------------------------------------------------------------------------
def decrypt(cipher):
    msg = ""
    print("Please choose your key")
    fileName = askopenfilename() # show an "Open" dialog box and return the path to the selected file

    with open(fileName, 'r') as infile:
       string = infile.read()
       n,e,d,p,q = string.split()
       n,e,d,p,q  = int(n),int(e),int(d),int(p),int(q) 
       infile.close()


    base64_message = cipher
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

   # print(message)
    
    parts = message.split()
    for part in parts:
       if part:
           c = int(part)
           msg += chr(pow(c, d, n))
    
    return msg
#--------------------------------------------------------------------------------------------------------------------------------------------------
def SavePublicKey(e,n):
    E = str(e)
    N = str(n)
  
    print("Please save your PublicKey")
    file_name = asksaveasfilename(initialfile='PublicKey.txt',defaultextension=".txt",filetypes=[("Text Documents","*.txt"),("All Files","*.*")])

    if file_name:
       f = open(file_name, 'a')      
       f.write(N)    
       f.write("      ") # seperating n and e
       f.write(E)
       f.close()
#--------------------------------------------------------------------------------------------------------------------------------------------------
def SavePrivateKey(e,n,d,p,q):
    E = str(e)
    N = str(n)
    D = str(d)
    P = str(p)
    Q = str(q)
  
    print("Please save your PrivateKey")
    file_name = asksaveasfilename(initialfile='PrivateKey.txt',defaultextension=".txt",filetypes=[("Text Documents","*.txt"),("All Files","*.*")])

    if file_name:
       f = open(file_name, 'a')      
       f.write(N)
       f.write("      ") # seperating n and e
       f.write(E)
       f.write("      ") # seperating e and d
       f.write(D)
       f.write("      ") # seperating d and p
       f.write(P)
       f.write("      ") # seperating p and q
       f.write(Q)
       f.close()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
def main():
 
 
    choice=int(input("Do you want to 1)encryption 2)decryption : "))
    if(choice == 1):

             
              keysize = int(input("Press input a keysize:"))
              print("Generating Key, please wait....")
              p,q ,e, d, n ,phiN = generateKeys(keysize)
           
            
              SavePublicKey(e,n)
              SavePrivateKey(e,n,d,p,q)
              
              print("Please choose your text message..")
              fileName = askopenfilename() # show an "Open" dialog box and return the path to the selected file
              Type = pathlib.Path(fileName).suffix
            
          
              with open(fileName, 'r') as infile:
                         string = infile.read()
                         infile.close()

              enc = encrypt(string)
 
              file_name = asksaveasfilename(initialfile='CipherText.txt',defaultextension=".txt",filetypes=[("Text Documents","*.txt"),("All Files","*.*")])

              if file_name:
                f = open(file_name, 'a')      
                f.write(enc)    
                f.close()
              
           
         
    #decryption     
    else:
        print("Please choose your CipherText..")
        fileName = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        with open(fileName, 'r') as infile:
                string = infile.read()
                infile.close()

     #   print(string)

        dec = decrypt(string)
        file_name = asksaveasfilename(initialfile='PlainText.txt',defaultextension=".txt",filetypes=[("Text Documents","*.txt"),("All Files","*.*")])

        if file_name:
             f = open(file_name, 'a')      
             f.write(dec)    
             f.close()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

main()
