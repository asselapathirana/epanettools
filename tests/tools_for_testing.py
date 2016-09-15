import difflib

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def compareFiles( first, second):
    with open(first, 'r') as myfile:
        f=myfile.readlines()
    with open(second, 'r') as myfile:
        s=myfile.readlines()
        
    diff = difflib.ndiff(f,s)    
    d1=""
    d2=""
    for line in diff:
        if(len(d1)>5000):
            break
        if line.startswith('-'):
            d1=d1+" "+(line[1:])
        elif line.startswith('+'):
            d2=d2+" "+(line[1:])     
    d1=d1.split()
    d2=d2.split()
    dif=""
    for i in range(min(len(d1),len(d2))):
        
        s=d1[i].strip("\n\t ")
        if(is_number(s)): s=format(float(s),'.3g')
        r=d2[i].strip("\n\t ")
        if(is_number(r)): r=format(float(r),'.3g')        
        if(s!=r):
            dif=dif+s+">"+r+"; "

                
        
    return dif