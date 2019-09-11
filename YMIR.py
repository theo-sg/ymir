import random
import time

ptr = 0
running = True
stack, callbacks = [0] * 64, []
alias, arrays = {}, {}

#creates alias in dict
def addalias(address, aliasname):
    global alias
    alias[aliasname] = address

def clearstack():
    global stack
    stack = [0] * 64
 
#pushes value v into location or alias n
def push(n, v):
    if n in alias:
        stack[int(alias[n][1:])] = v
    else:
        stack[int(n[1:])] = v

#pulls value from location or alias n
def pull(n):
    if n[0] == "$":
        return stack[int(n[1:])]
    elif n in alias:
        return stack[int(alias[n][1:])]
    else:
        return int(n)


#arithmetic engine functions
def add(a):
    try:
        return int(a[0]) + int(a[1])
    except:
        return str(a[0]) + str(a[1])

def subtract(a):
    return a[0] - a[1]

def multiply(a):
    return a[0] * a[1]

def divide(a):
    return a[0] / a[1]

def modulo(a):
    return a[0] % a[1]

def quotient(a):
    return a[0] // a[1]

def exponentiate(a):
    return a[0] ** a[1]

def rand(a):
    return random.randint(int(a[0]), int(a[1]))

def equal(a):
    return str(a[0]).strip() == str(a[1]).strip()

def greater(a):
    return a[0] > a[1]

def less(a):
    return a[0] < a[1]

def greaterequal(a):
    return a[0] >= a[1]

def lessequal(a):
    return a[0] <= a[1]

def notequal(a):
    return str(a[0]).strip() != str(a[1]).strip()


operands = {"+" : add,
                    "-" : subtract,
                    "*" : multiply,
                    "/" : divide,
                    "//" : quotient,
                    "^" : exponentiate,
                    "%" : modulo,
                    "&" : rand,
                    "==" : equal,
                    ">" : greater,
                    "<" : less,
                    ">=" : greaterequal,
                    "<=" : lessequal,
                    "!=" : notequal}

def run(line):
    global file   
    global ptr
    global running
    global operands

    #'error handling' - very basic, should be improved at some time in the future
    try: 
        tokens = line.split(' ')
        tokens[-1] = tokens[-1][:-1]

        #token analysis through selection
        if tokens[0] == "if":
            values = [pull(tokens[1]), pull(tokens[3])]
            #searches for next else between current line and end - fix in future to allow for nestled selection
            parseend = file.index("else," , ptr, len(file) - 1) 
            evaluation = operands[tokens[2]](values)
            #append line number of this if for recursion
            if evaluation:
                callbacks.append(ptr - 1)
            else:
                ptr = parseend
                return
        

        #echo prints value    
        elif tokens[0]  == "echo":
            if tokens[1][0] == '"':
                print(" ".join(tokens[1:]).replace('"', ' ').strip())
            else:
                print(pull(tokens[1]))

        #ask takes input
        elif tokens[0] == "ask":
            push(tokens[3], input(pull(tokens[1])))

        #push sets value in stack
        elif tokens[0] == "push" and tokens[2] == "to":
            push(tokens[3], pull(tokens[1]))

        #string creates string variable
        elif tokens[0] == "string" and tokens[2] == "=":        
            push(tokens[1], " ".join(tokens[3:]).replace('"', ' ').strip())

        #alias allows for variable name
        elif tokens[0] == "alias" and tokens[2] == "as":
            addalias(tokens[1], tokens[3])

        #decrement variable
        elif tokens[0] == "decr":
            push(tokens[1], pull(tokens[1]) - 1)

        #increment variable
        elif tokens[0] == "incr":
            push(tokens[1], pull(tokens[1]) + 1)

        #time delay
        elif tokens[0] == "wait":
            time.sleep(pull(tokens[1])/10)
        

        #arithmetic engine takes up other cases (assignment, etc)
        else:
            try:
                if len(tokens) <= 3:
                    push(tokens[0], pull(tokens[2]))
                else:
                    values = [pull(tokens[2]), pull(tokens[4])]
                    push(tokens[0], operands[tokens[3]](values))
            except:
                pass
        
        #final character and flow control token check

        if tokens[0] == "goto":
            ptr = int(tokens[1]) - 1

        elif tokens[0] == "jump":
            ptr += int(tokens[1])
            
        elif line[-1] == ",":
            ptr += 1

        elif line[-1] == ";":
            running = False

        elif line[-1] == ":":
            ptr = callbacks.pop(-1)
            return
    
    except:
        #cancels execution and displays the problematic line
        running = False
        print("-")
        print("- \nError on line " + str(ptr) + ": " + str(line))
        
    return


#recursively asks user for a file
while True:
    #locationname = input("Please enter the name of the YMIR file which must be opened: ").strip()
    try:
        #creates list of every non-empty element in the file with no whitespace padding
        file = [x.strip() for x in open(input("Please enter the name of the YMIR file which must be opened: ").strip() + ".ymir", "r") if x.strip() != ""]
        break
    except:
        print("No file exists with that name in this folder.")

#a waste of about 1.36 seconds ;)
for i in range(2):
    print(".",end='')
    time.sleep((1/3))
print(".")
print("File loaded successfully.")
time.sleep(.7)

while running:
    run(file[ptr])

for i in range(2):
    print(".",end='')
    time.sleep((1/3))
print(".")
input("Press ENTER to continue.")
