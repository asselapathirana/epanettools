import difflib
import os
import sys


def redirect_stdout():
    print ("Redirecting stdout")
    sys.stdout.flush()  # <--- important when redirecting to files

    # Duplicate stdout (file descriptor 1)
    # to a different file descriptor number
    newstdout = os.dup(1)

    # /dev/null is used just to discard what is being printed
    devnull = os.open('/dev/null', os.O_WRONLY)

    # Duplicate the file descriptor for /dev/null
    # and overwrite the value for stdout (file descriptor 1)
    os.dup2(devnull, 1)

    # Close devnull after duplication (no longer needed)
    os.close(devnull)

    # Use the original stdout to still be able
    # to print to stdout within python
    sys.stdout = os.fdopen(newstdout, 'w')


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def compareFiles(first, second):
    with open(first, 'r') as myfile:
        f = myfile.readlines()
    with open(second, 'r') as myfile:
        s = myfile.readlines()

    diff = difflib.ndiff(f, s)
    d1 = ""
    d2 = ""
    for line in diff:
        if(len(d1) > 5000):
            break
        if line.startswith('-'):
            d1 = d1 + " " + (line[1:])
        elif line.startswith('+'):
            d2 = d2 + " " + (line[1:])
    d1 = d1.split()
    d2 = d2.split()
    dif = ""
    for i in range(min(len(d1), len(d2))):

        s = d1[i].strip("\n\t ")
        if(is_number(s)):
            s = format(float(s), '.3g')
        r = d2[i].strip("\n\t ")
        if(is_number(r)):
            r = format(float(r), '.3g')
        if(s != r):
            dif = dif + s + ">" + r + "; "

    return dif
