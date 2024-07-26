import base64 

def b64e(s): 
    return base64.b64encode(s.encode()).decode() 
def b64d(s): 
    return base64.b64decode(s).decode()

