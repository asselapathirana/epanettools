import difflib

def compareFiles( first, second):
    with open(first, 'r') as myfile:
        f=myfile.readlines()
    with open(second, 'r') as myfile:
        s=myfile.readlines()
        
    diff = difflib.ndiff(f,s)    
    d1=""
    d2=""
    for line in diff:
        if line.startswith('-'):
            d1=d1.join(line[1:])
        elif line.startswith('+'):
            d2=d2.join(line[1:])     
    d1=d1.split()
    d2=d2.split()
    diff=""
    for i,v in enumerate(d1):
        if(d1[i]!=d2[i]):
            diff=diff+d1[i]+">"+d2[i]
        
    return diff