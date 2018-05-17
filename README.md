# PTR

PTR is an assembly-like low level esoteric language. Its 
syntax is very simple and requires manual memory management.

## PTR's Structure

PTR makes use of a one-dimensional memory array that the user
configures. In addition there is a single accumulator register
that receives all arithmetic operations.

## Running files

Right now, PTR is implemented in python2.7, but an implementation in
C is in the works. Run PTR files as such:
```
python PTR.py <file.ptr> [-d]
```

## Basics

### Creating a Variable:
```
alc 1
$var1 *0
```

The first line allocates one space in memory and puts that address in memory
slot 0. The second line sets the variable var1 to the value at 0.
```*``` pointers can be stacked up as many times as necessary. A variable
can only be assigned once, and its value is not especially important because
```$var1``` is a pointer. 
```
@$var1 5
```
Sets the value at the address stored in ```$var1``` to 5. 
the command ```o``` outputs whatever is after it. ```o $var1``` will print the
address of ```$var1``` to STDOUT. To print the value of ```$var1```, the command 
```o *$var1``` is used. In addition to ```o```, ```w``` does the same thing, but
it prints the ascii character of the value.

### Arithmetic
The commands ```a, s``` respectively add and subtract the next
two tokens. ```sl, sr``` shift left and shift right the next token.
right the next two tokens. If either of the two arent scalars, pointers, or vars, 
an error is thrown. The result is put into the accumulator register. The command ```m```
moves the value of the accumulator to the value in memory of the following token.

### Functions and Convention.
PTR has some basic flow commands. ```f``` skips the following command if the two
tokens directly following it are not equal. ```l``` does the same except for less 
than.

There are two types of labels in PTR. The first is a destination label, indicated
by ```--<name>```, the second is a departure label, indicated by ```-><name```.
These labels are used both as flow commands and function calls. The command ```j ->LABEL```
sends the instruction pointer to the destination of said label. The command ```r ->LABEL```
pushes a new instruction pointer onto the call stack and goes to the corresponding label.
The command ```d --LABEL``` indicates the definition of a function, and the command
```e``` pops the call stack and resumes running at the new instruction pointer, exiting
the function. An error is returned on empty call stack.

### Memory Management
As seen earlier, memory is manually managed in PTR. The whole language is an excercise
in layered pointers and respectful memory use, and while there is no error penalty for memory
leaks, overwriting data and leaving memory allocated is sad.

By convention, the first 10 slots of memory are swap memory. If there is data you want to keep
persistent between function calls, it's best to allocate space. The next
ten are used as function arguments. std.ptr has a function that automatically assigns variables
to slots 10-15 called ```$arg1``` etc. This makes code easier to visualize. The rest of memory
is up for grabs.

The command ```alc <VALUE>``` returns the smallest continuous space in memory that is <VALUE> + 1 slots
in size. Functions by convention return values to the 0 slot. The command ```rel <VAL1> <VAL2>```
releases VAL2 slots in memory staring with VAR1. The final memory command is ```ali```, which 
allocates a specific spot in memory. This is helpful for allocating data structures larger than
one slot in memory, like arrays, but should really only be used in lower level functions.

### Other files
Including a file is fairly simple. ```inc folder/fileName``` **without** the '.ptr'. The file is tokenized
and added to the end of the tokens to be parsed and executed, so any and all code will be 
executed. Jump statements can form simple ifguards.

## Examples
One example included in the ```lib``` folder is an implementation of a classic array. These
functions allow the user to create and edit an array without *as* manually manipulating memory.
Here is an excerpt:
```
j ->endArray
d --makeArray
m 0 :: first arg: length ::
@0 **0 
@2 *0
:: now, find a chunk of memory big enough ::
a *0 1 :: length of array + 1 ::
m 1
alc *1
@*0 *2
rel 1 8 :: skip 0th slot bc of return values ::
e

...
--endArray
```
The jump statement at the top forms a rudimentary ifguard as mentioned above. The reason why
the first command is a move statement is that I've loaded the address of the first argument
into the accumulator. The first thing I do is get its value to work with. Then I allocate space
I've coded arrays as an integer value for length followed by that many empty slots. The address
of the array is returned, but not before slots 1-9 are released from working memory.
