"""
+=========================   
|   A new language designed by Ben Greene in spring 2018
|   
|
+=========================
"""
import sys
"""
a basic token class for
organizational purposes only...
a struct...
"""
class Token:
    def __init__(self, t, v):
        self.ty = t
        self.v = v
    def __str__(self):
        return "{}\t{}".format(self.ty, self.v)

# acc = [0,0]
# # pointer stack
# ptr = [0]
# mem = []


def setMem(l,mem,used):
# size of memory!! to be adjustable LATER
    while len(mem)< l:
        mem.append(0)
        used.append(0)
    while len(mem) > l:
        mem.pop()
        used.pop()





"""
Tokenize the input text...
Very simple lexer because
the language is simple...
"""
def tkns(text):
    words = text.split()
    tokens = []
    comment = False
    for word in words:
        if word == "::":
            comment = not comment
        if comment:
                continue
        if word[0] == "*":
            tokens.append(Token("ADD", word[1:]))
        elif word[0] == "@":
            tokens.append(Token("ATT", word[1:]))
        elif word.isdigit():
            tokens.append(Token("NUM", word))
        elif word == "\n":
            tokens.append(Token("RET", word))
        elif word in ["a", "m", "s","j","f","o","d","r","e","w","l",
         "inc", "mem", "alc", "rel", "ali"]:#"asmjfodrew":
            tokens.append(Token("KEY", word))
        elif "--" in word[:2]:
            tokens.append(Token("LBF", word[2:]))
        elif "->" in word[:2]:
            tokens.append(Token("LBT", word[2:]))
        elif word[0] == "$":
            tokens.append(Token("VAR", word[1:]))
            #print tokens[-1]
        elif word.replace("/","").isalpha():
            tokens.append(Token("IDT", word))


    return tokens

"""
Check to see if address is valid
ps not sure why I had to make this method so fucking kooky
"""
def validMem(n):
    lN = len(mem)
    if n < lN:
        pass
    else:
        print "invalid memory access attempt:", n
        sys.exit(1)


"""
gets the value of a pointed token
recursively capable of multiple layers
of pointing
ACCESS MEMORY
"""
def fnd(token):
    if token.ty == "NUM":
        return int(token.v)
    elif token.ty == "VAR":
        return var[token.v]
    elif token.ty == "ADD":
        newToken = tkns(token.v)[0]
        if newToken.ty == "ADD":
            validMem(fnd(newToken))
        return mem[int(fnd(newToken))]
"""
combined steps of parsing and 
executing.
"""
def prs(tk, ptr, exp):
    # if at end, return
    if ptr[-1] >= len(tk):
        return
    # error check the expected token type
    if exp != [] and tk[ptr[-1]].ty not in exp:
        print "error:", tk[ptr[-1]-1], "wanted", str(exp) 
        sys.exit(1)
    # return a number
    if tk[ptr[-1]].ty == "NUM":
        n = int(tk[ptr[-1]].v)
        ptr[-1] = ptr[-1] + 1
        return n
    if tk[ptr[-1]].ty == "IDT":
        m = tk[ptr[-1]].v
        ptr[-1] = ptr[-1] + 1
        return m
    # recursively returns a pointed number
    elif tk[ptr[-1]].ty == "ADD":
        n = fnd(tk[ptr[-1]])
        ptr[-1] = ptr[-1] + 1
        return n
    # work with labels either as functions
    # or simple gotos for loops
    # "to"
    elif tk[ptr[-1]].ty == "LBT":
        l = tk[ptr[-1]].v
        ptr[-1] = ptr[-1] + 1
        return l
    # labels more
    # "from"
    elif tk[ptr[-1]].ty == "LBF":
        ptr[-1] = ptr[-1] + 1
        prs(tk, ptr, [])
    # simple set an address in memory a value
    elif tk[ptr[-1]].ty == "ATT":
        val1 = fnd(tkns(tk[ptr[-1]].v)[0])
        ptr[-1] = ptr[-1] + 1
        val2 = prs(tk, ptr, ["NUM", "ADD", "VAR"])
        #validMem(add)
        mem[val1] = int(val2)
        used[val1] = 1
        prs(tk, ptr, [])
    # add two values
    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "a":
        ptr[-1] = ptr[-1] + 1
        v1 = prs(tk, ptr, ["NUM", "ADD", "VAR"])
        v2 = prs(tk, ptr, ["NUM", "ADD","VAR"])
        acc[0] = v1 + v2
        prs(tk, ptr, [])
    # subtract two values
    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "s":
        ptr[-1] = ptr[-1] + 1
        v1 = prs(tk, ptr, ["NUM", "ADD", "VAR"])
        v2 = prs(tk, ptr, ["NUM", "ADD", "VAR"])
        acc[0] = v1 - v2
        prs(tk, ptr,[])
    # move the accumulator to an address in memory ACCESS MEMORY
    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "m":
        ptr[-1] = ptr[-1] + 1
        add = prs(tk, ptr, ["NUM", "ADD", "VAR"])
        validMem(add)
        mem[add] = acc[0]
        used[add] = 1
        acc[0] = 0
        prs(tk, ptr,[])
    # output value in address
    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "o":
        ptr[-1] = ptr[-1] + 1
        val = prs(tk, ptr, ["NUM","ADD", "VAR"])
        if acc[1] == 1:
            sys.stdout.write(chr(val))
        else:
            sys.stdout.write(str(val))
        sys.stdout.flush()
        prs(tk, ptr,[])
    # conditional if x == y pass, else skip to next command
    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "f":
        ptr[-1] = ptr[-1] + 1
        v1 = prs(tk, ptr, ["NUM", "ADD", "VAR"])
        v2 = prs(tk, ptr, ["NUM", "ADD", "VAR"])
        if int(v1) != int(v2):
            ptr[-1] = ptr[-1] + 1
            if ptr[-1] >= len(tk):
                return
            # interesting issue here because var can also be a command...
            # it will be skipped... (workaround: use a jump)
            while (tk[ptr[-1]].ty != "KEY" and tk[ptr[-1]].ty != "ATT"):
                ptr[-1] = ptr[-1] + 1
                if ptr[-1] >= len(tk):
                    return
        prs(tk, ptr,[])
    # condition if x < y pass, else skip to next command
    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "l":
        ptr[-1] = ptr[-1] + 1
        v1 = prs(tk, ptr, ["NUM", "ADD", "VAR"])
        v2 = prs(tk, ptr, ["NUM", "ADD", "VAR"])
        if int(v1) >= int(v2):
            ptr[-1] = ptr[-1] + 1
            if ptr[-1] >= len(tk):
                return
            # interesting issue here because var can also be a command...
            # it will be skipped... (workaround: use a jump)
            while (tk[ptr[-1]].ty != "KEY" and tk[ptr[-1]].ty != "ATT"):
                ptr[-1] = ptr[-1] + 1
                if ptr[-1] >= len(tk):
                    return
        prs(tk, ptr,[])
    # jump to label
    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "j":
        ptr[-1] = ptr[-1] + 1
        lbl = prs(tk, ptr, ["LBT"])
        #print "JUMP:",lbl
        ptr[-1] = 0
        while tk[ptr[-1]].ty != "LBF" or tk[ptr[-1]].v != lbl:
            ptr[-1] = ptr[-1] + 1
            if ptr[-1] >= len(tk):
                return
        prs(tk, ptr, [])
    # define label as function
    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "d":
        ptr[-1] = ptr[-1] + 1
        lbl = prs(tk, ptr, ["LBF"])
    # run function by pushing current location to pointer stack
    # and moving new pointer to label 
    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "r":
        ptr[-1] = ptr[-1] + 1
        lbl = prs(tk, ptr, ["LBT"])
        #print "ENTER:",lbl
        ptr.append(0)

        while tk[ptr[-1]].ty != "LBF" or tk[ptr[-1]].v != lbl:
            ptr[-1] = ptr[-1] + 1
            if ptr[-1] >= len(tk):
                print "Error: function: {} not found".format(lbl)
                sys.exit(1)
        prs(tk, ptr, [])
    # exit function: pop off pointer stack and resume at new 
    # location: allows for nested function execution
    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "e":
        #print "EXIT"
        if len(ptr) > 1:
            ptr.pop()
        else:
            print "error:", tk[ptr[-1]], "illegal function exit"
        prs(tk, ptr, [])
    # set output mode to ascii or numerical
    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "w":
        ptr[-1] = ptr[-1] + 1
        if acc[1] == 0:
            acc[1] = 1
        else:
            acc[1] = 0
        prs(tk, ptr, [])
    # include a file
    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "inc":
        ptr[-1] = ptr[-1] + 1
        fname = prs(tk, ptr, ["IDT"])
        text = run(fname+".ptr")
        tk += tkns(text)
        prs(tk,ptr,[])
    # set the memory size for a program
    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "mem":
        ptr[-1] = ptr[-1] + 1
        val = prs(tk, ptr, ["NUM"])
        setMem(val,mem,used)
        prs(tk, ptr, [])
    
    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "alc":
        ptr[-1] = ptr[-1] + 1
        amount = prs(tk, ptr, ["NUM", "ADD"]) + 1
        freeCount = 0
        ind = 20
        while freeCount < amount:
            if used[ind] == 1:
                freeCount = 0
            else:
                freeCount += 1
            ind += 1
            if ind == len(used):
                print "Error: not enough memory to allocate"
                sys.exit(1)
        mem[0] = ind-amount+1
        #print ind-amount
        for i in range(ind-amount+1, ind):
            used[i] = 1
        prs(tk, ptr, [])
    
    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "ali":
        ptr[-1] = ptr[-1] + 1
        addr = prs(tk, ptr, ["NUM", "ADD"])
        if addr >= len(used):
            print "No such memory exists!"
            sys.exit(1)
        if used[addr] == 1:
            #print used
            #print mem
            #print addr
            print "Memory already allocated"
            sys.exit(1)
        else:
            used[addr] = 1
        prs(tk, ptr, [])

    elif tk[ptr[-1]].ty == "KEY" and tk[ptr[-1]].v == "rel":
        ptr[-1] = ptr[-1] + 1
        addr = prs(tk, ptr, ["NUM", "ADD"])
        amount = prs(tk, ptr, ["NUM", "ADD"])
        for i in range(addr, addr+amount):
            mem[i] = 0
            used[i] = 0
        prs(tk, ptr, [])

    # set or access a variable
    elif tk[ptr[-1]].ty == "VAR":
        if not var.get(tk[ptr[-1]].v, False):
            name = tk[ptr[-1]].v
            ptr[-1] = ptr[-1] + 1
            val = prs(tk, ptr, ["NUM","ADD"])
            var[name] = val
            prs(tk, ptr, [])
        else:
            n = var[tk[ptr[-1]].v]
            ptr[-1] = ptr[-1] + 1
            return n


"""
run a file
"""
def run(fname):
    try:
        with open(fname) as f:
            text = f.read()
    except:
        print "Error: {}: No such lib exists".format(fname)
        sys.exit(1)
    return text

if __name__ == '__main__':
    # accumulator and write mode
    acc = [0,0]
    # pointer stack
    ptr = [0]
    mem = []
    used = []
    var = {}
    setMem(10,mem, used)
    if len(sys.argv) == 1:
        text = ""
    else:
        text = run(sys.argv[1])
    t = tkns(text)

    prs(t, ptr, [])
    if len(sys.argv) == 3:
        if sys.argv[2] == "-d":
            #slots = [i for i in range(len(mem))]
            #print slots
            print used
            print mem
            #print acc
            #print var
