# Number Functions

A Python Package of various Number(Integer) Functions for computations

## Various Functions and their Description
You can call directly these functions by importing this package

1.quotient(a,b) //It takes two arguments and returns quotient i.e a/b

2.remainder(a,b) //It takes two arguments and returns remainder i.e a%b

3.floordiv(a,b) //It takes two arguments and returns quotient along with specific floor and ceil i.e a//b

4.product(a,b) //It takes two arguments and returns product i.e a * b

5.power(a,b) //It takes two arguments and returns a power b


6.sum(a,b) //It takes two arguments and returns sum i.e a+b

7.subtract(a,b) //It takes two arguments and returns subtraction i.e a-b

8.iseven(n) //It takes one argument and returns true if passed argument is even otherwise false

9.isodd(n) //It takes one argument and returns true if passed argument is odd otherwise false

10.prteven(n) //It takes one argument and prints even digits of that number

11.prtodd(n) //It takes one argument and prints odd digits of that number

12.digcount(n) //It takes one argument and returns the count of digits of given number

13.prtevencount(n) //It takes one argument and prints the count of even digits of given number

14.prtoddcount(n) //It takes one argument and prints the count of odd digits of given number

15.evensum(n) //It takes one argument and returns the sum of even digits of given number

16.oddsum(n) //It takes one argument and returns the sum of odd digits of given number

17.digitsum(n) //It takes one argument and returns the sum of all digits of given number

18.isprime(n) //It takes one argument and returns true if passed argument is prime number otherwise false

19.primedigitcount(n) //It takes one argument and returns count of prime digits in given number

20.prtprime(n) //It takes one argument and prints the prime digits of given number

21.primedigitsum(n) //It takes one argument and returns sum of prime digits  of given number

22.digreverse(n) //It takes one argument and returns the number which is reverse of given number

23.ispalindrome(n) //It takes one argument and returns true if passed argument is palindrome otherwise false

24.factorial(n) //It takes one argument and returns factorial of given number

25.factor(n) //It takes one argument and returns factors of given number

26.factorcount(n) //It takes one argument and returns count of factors of given number

27.factorsum(n) //It takes one argument and returns sum of factors of given number

28.isstrong(n) //It takes one argument and returns true if passed argument is strong otherwise false

STRONG:
-----------
If sum of individual digits factorial is equal to given number then it is called Strong number
Ex:-
====
145


29.isperfect(n) //It takes one argument and return true if passed argument is perfect otherwise false

PERFECT:
------------------
If sum of factors of given number except that one which is equal to given number is called Perfect number
Ex:-
====
28

30.isarmstrong(n) //It takes one argument and return true if passed argument is armstrong otherwise false 

ARMSTRONG:
-------------------------
An armstrong number is a number which equal to the sum of the cubes of its individual digits
Ex:
====
153

31.digitproduct(n) //It returns product of digits of given number(number should not contains zeroes(0))




###  Usage

Following query on terminal will provide the following

```
INPUT:
-----------------------------------------------
import Numfunctions
a=Num-functions.isprime(407)
print (a)

b=Numfunctions.isodd(51432)
print(b)

c=Numfunctions.digreverse(995186)
print(c)

Numfunctions.prteven(123456789)

Numfunctions.prtprime(123456789123456789)

OUTPUT:
----------------------------------------------
False
False
681599
2 4 6 8
2 3 5 7 2 3 5 7

```