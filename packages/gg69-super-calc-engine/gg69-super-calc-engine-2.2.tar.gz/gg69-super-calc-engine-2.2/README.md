# gg69-calc-engine
One line calculator engine with example of wrapping his functional
<!-- TODO: fix grammar-->
## Syntax
Numbers can be float
```
4.5
```
Function attributes should be given in circle brackets
```
sqrt(69)
```
To get name from namespace, you should use comma too
```
comb.comb_c
```
Sets should be declared in figure brackets and tuples in square brackets
```
{2, 4, 6, 8}
[1, 1, 2 ,3]
```
gg69 calculator engine is using concept of operators.

They could be writen of letters or from specific chars like +-/*=.

If chars in operator were reversed (like using \ instead of /), the notion of
left and right will be changed to *opposite*.
```
a / b
b \ a
a <= b
b => a
```
Unfortunately, constructions like ```1 < 2 < 3``` are not supported

Some operators could take the third parameter, that called *dop*. Syntax is same 
for functions
```
69 mod(5) 179
```
If you put two *char-made* operator near, each one of them will count his own value
and than gg69-super-calc-engine will *merge* them all to one set
```
(0-b+-sqrt(D))/a
``` 
All chars after ; token will be ignored
```
2+2;bla-bla-bla
```