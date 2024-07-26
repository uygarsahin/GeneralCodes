import base64 

#Encryption of String
def b64e(string): 
    return base64.b64encode(string.encode()).decode() 
#Decryption of String 
def b64d(string): 
    return base64.b64decode(string).decode()

##MAIN##

WordOfChange ='Hello World'

OutPutofEncWord=b64e(WordOfChange)
print(OutPutofEncWord)
print('='*10)
OutPutofDencWord=b64d(OutPutofEncWord)
print(OutPutofDencWord)

