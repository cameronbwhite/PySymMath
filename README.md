PySymMath
=========

Interactive mathematical languages written in Python

```python
>>> A,B,C = Atom('A'), Atom('B'), Atom('C')
>>> ~A
'¬A'
>>> A & B
'A ∧ B'
>>> A | B
'A ∨ B'
>>> A & (B | C) & ~B
'(A ∧ (B ∨ C)) ∧ (¬B)'
```

```python
>>> A,B,C = Atom('A'), Atom('B'), Atom('C')
>>> e = ~A 
>>> e.truthTable(A)
 A | ¬A
 F | T 
 T | F 

>>> e = A & B
>>> e.truthTable(A)
 A | B | A ∧ B
 F | F | F 
 F | T | F 
 T | F | F 
 T | T | T 

>>> e = A | B
>>> e.truthTable(A,B,C)
 A | B | A ∨ B
 F | F | F 
 F | T | T 
 T | F | T 
 T | T | T 

>>> e = A & (B | C) & ~B
>>> e.truthTable(A,B,C)
 A | B | C | (A ∧ (B ∨ C)) ∧ (¬B)
 F | F | F | F 
 F | F | T | F 
 F | T | F | F 
 F | T | T | F 
 T | F | F | F 
 T | F | T | T 
 T | T | F | F 
 T | T | T | F 
```
