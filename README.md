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
Creating a Variable:
```
alc 1
$var1 *0
```
