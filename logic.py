#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Cameron White
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the project nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE PROJECT AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE PROJECT OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

class Atom(object):
    """ A Atom is an object for doing logical operations.
        
        A Atom instance represents an atomic object
        in logic. These instances may proform logical 
        operations(NOT/¬, AND/∧, OR/∨, XOR/⊻, IMPLIES/→, 
        IFF/↔). The only conveat is that operations do
        not evaluate (i.e the solution is not returned)
        instead an Expression object is returned. These
        Expression objects may then be used to evaluate
        atoms with different values as well as 
        other usefull things.
    """ 
    def __init__(self, symbol, value=None):
        """
            Any object which str(symbol) is valid is
            a valid object. A string object is the most
            logical type to use.

            Keyword arguments:
            symbol -- Object to represent the Atom.
        """
        self.symbol = symbol
        if value is None:
            self.value = False
        else:
            self.value = value
    def __str__(self):
        """ Return the str of the symbol representing the Atom. """
        return str(self.symbol)
    def __repr__(self):
        """ Return the repr of the symbol representing the Atom.  """
        return repr(self.symbol)
    def __call__(self):
        """ Return the """
        return self.value
    def true(self):
        self.value = True
    def false(self):
        self.value = False
    def __invert__(self):
        left,right = self.get_atoms(None)
        return Expression(NotOperation(left))
    def __and__(self, other):
        """ Return the Expression containing the AndOperation. """
        left, right =  self.get_atoms(other)
        return Expression(AndOperation(left, right)) 
    def __or__(self, other):
        """ Return the Expression containing the OrOperation. """
        left, right = self.get_atoms(other)
        return Expression(OrOperation(left, right)) 
    def __xor__(self, other):
        """ Return the Expression containing the XorOperation. """
        left, right = self.get_atoms(other)
        return Expression(XorOperation(left, right))
    def implies(self, other):
        """ Return the Expression containing the ImpliesOperation. """
        left, right = self.get_atoms(other)
        return Expression(ImpliesOperation(left, right))
    def iff(self, other):
        """ Return the Expression containing the IffOperation. """
        left, right = self.get_atoms(other)
        return Expression(IffOperation(left, right))
    def get_atoms(self, other=None):
        """ Return the left atom and right atoms.

            A atom can proform operations with other Atom
            or Expression ojects. However the atom needs to get
            access to the atoms of expressions inorder to 
            create an operation instance.
            
            Keyword Arguments:
            other -- Second object to test.
        """
        P, Q = None, None
        if isinstance(self, (Expression, Operation)):
            P = self.expression
        else:
            P = self
        if other is not None:
            if isinstance(other, Expression):
                Q = other.expression
            else:
                Q = other
        return P, Q

class Expression(Atom):
    """ An Expression is the High level object which represents a 
        """
    def __init__(self, expression):
        """ """
        if not isinstance(expression, (Atom,Operation)):
            raise TypeError
        self.expression = expression
    def __str__(self):
        """ """
        return str(self.expression)
    def __repr__(self):
        """ """
        return repr(self.expression)
    def __call__(self):
        """ """
        return self.expression()
    def truthTable(self, *atom_list):
        """ """
        # Create a header line
        output_line = " "
        for atom in atom_list:
            output_line += str(atom) + ' | '
        output_line += str(self)
        print(output_line)
        # Determine all possible inputs. 
        possible_input = permutations((False, True), len(atom_list))
        # Evaluate the expression for each possible input.
        for input_line in possible_input:
            output_line = " "
            for i in range(len(input_line)):
                if input_line[i] == True:
                    atom_list[i].true()
                    output_line += 'T | '
                else:
                    atom_list[i].false()
                    output_line += 'F | '
            if self() == True:
                output_line += 'T '
            else:
                output_line += 'F '
            print(output_line)
    def truthTableExtended(self, *atom_list):
        """ """
        return NotImplemented
    def vennDiagram(self):
        """ """
        return NotImplemented
    def nand(self):
        """ """
        self.expression = self.expression.nand()
    def nor(self):
        """ """
        self.expression = self.expression.nor()

class Operation(object):
    """ An Operation is used to represent an operation one or more
        Atom objects.  """
    def __init__(self, *atom_list):
        """ Create an Operation instance. 
            
            Keyword Arguments:
            *atom_list -- tuple or list of Atom objects.  """
        for atom in atom_list:
            if not isinstance(atom, (Atom, Operation)):
                raise TypeError
    
class UnaryOperation(Operation):
    """ An UnaryOperation is used to represent an operation on one
        Atom object.  """
    def __init__(self, P):
        """ Create an UnaryOperation instance. """
        super().__init__(P)
        self.P = P
    def nand(self):
        """ """
        try:
            self.P = self.P.nand()
        except(AttributeError):
            pass
    def nor(self):
        """ """
        try:
            self.P = self.P.nor()
        except(AttributeError):
            pass

class BinaryOperation(UnaryOperation):
    """ An BinaryOperation is used to represent an operation on two
        Atom objects.  """
    def __init__(self, P, Q):
        """ """
        super(BinaryOperation, self).__init__(P)
        super(UnaryOperation, self).__init__(Q)
        self.Q = Q
    def nand(self):
        """ """
        super().nand()
        try:
            self.Q = self.Q.nand()
        except(AttributeError):
            pass
    def nor(self):
        """ """
        super().nor()
        try:
            self.Q = self.Q.nor()
        except(AttributeError):
            pass

class NotOperation(UnaryOperation):
    """ An NotOperation is used to represent a NOT operation on a
        Atom object. """
    def __init__(self, atom):
        """ """
        super().__init__(atom)
    def __str__(self):
        """ """
        string = '¬'
        if isinstance(self.P, Operation):
            string += '(' + str(self.P) + ')'
        else:
            string += str(self.P)
        return string
    def __repr__(self):
        return "'" + str(self) + "'"
    def __call__(self):
        """ """
        return logical_not(self.P())
    def nand(self):
        """ """
        super().nand()
        return NandOperation(self.P, self.P)
    def nor(self):
        """ """
        super().nor()
        return NorOperation(self.P, self.P)

class AndOperation(BinaryOperation):
    """ An AndOperation is used to represent an AND operation on two
        Atom objects. """
    def __init__(self, P, Q):
        """ """
        super().__init__(P, Q)
    def __str__(self):
        """ """
        string = '' 
        if isinstance(self.P, Operation):
            string += '(' + str(self.P) + ')'
        else:
            string += str(self.P)
        string += ' ∧ '
        if isinstance(self.Q, Operation):
            string += '(' + str(self.Q) + ')'
        else:
            string += str(self.Q)
        return string
    def __repr__(self):
        return "'" + str(self) + "'"
    def __call__(self):
        """ """
        return logical_and(self.P(), self.Q())
    def nand(self):
        """ """
        super().nand()
        return NandOperation(NandOperation(self.P, self.Q),\
                             NandOperation(self.P, self.Q))
    def nor(self):
        """ """
        super().nor()
        return NorOperation(NorOperation(self.P, self.P),\
                            NorOperation(self.Q, self.Q))

class OrOperation(BinaryOperation):
    """ An OrOperation is used to represent an OR operation on two
        Atom objects. """
    def __init__(self, P, Q):
        """ """
        super().__init__(P, Q)
    def __str__(self):
        """ """
        string = ""
        if isinstance(self.P, Operation):
            string += '(' + str(self.P) + ')'
        else:
            string += str(self.P)
        string += ' ∨ '
        if isinstance(self.Q, Operation):
            string += '(' + str(self.Q) + ')'
        else:
            string += str(self.Q)
        return string
    def __repr__(self):
        return "'" + str(self) + "'"
    def __call__(self):
        """ """
        return logical_or(self.P(), self.Q())
    def nand(self):
        """ """
        super().nand()
        return NandOperation(NandOperation(self.P, self.P),\
                             NandOperation(self.Q, self.Q))
    def nor(self):
        """ """
        super().nor()
        return NorOperation(NorOperation(self.P, self.Q),\
                            NorOperation(self.P, self.Q))

class XorOperation(BinaryOperation):
    """ An XorOperation is used to represent an ⊻(XOR) operation on two
        arguments (ie. P ⊻ Q). 

        The arguments may be of type Atom or Operation. The
        simplest case is when the arguments are both Atoms,
        the operation can be solved by lookup in the xor logic 
        table. If an argument is a Expression the expression has
        to be evaluated before the final xor operation will be
        proformed.
    """
    def __init__(self, P, Q):
        """ """
        super().__init__(P, Q)
    def __str__(self):
        """ Return the string representation of the XorOperation 
            Object. """
        string = ""
        if isinstance(self.P, Operation):
            string += '(' + str(self.P) + ')'
        else:
            string += str(self.P)
        string += ' ⊻ '
        if isinstance(self.Q, Operation):
            string += '(' + str(self.Q) + ')'
        else:
            string += str(self.Q)
        return string
    def __repr__(self):
        """ Return the representation of the XorOperation Object. """
        return "'" + str(self) + "'"
    def __call__(self):
        """ Return the value of the evaluated XorOperation Object. """
        return logical_xor(self.P(), self.Q())
    def nand(self):
        """ """
        return NotImplemented
    def nor(self):
        """ """
        return NotImplemented

class ImpliesOperation(BinaryOperation):
    """ An ImpliesOperation is used to represent an IMPLIES 
        operation on two Atom objects. 
    """
    def __init__(self, P, Q):
        """ """
        super(ImpliesOperation, self).__init__(P, Q)
    def __str__(self):
        """ """
        string = ""
        if isinstance(self.P, Operation):
            string += '(' + str(self.P) + ')'
        else:
            string += str(self.P)
        string += ' → '
        if isinstance(self.Q, Operation):
            string += '(' + str(self.Q) + ')'
        else:
            string += str(self.Q)
        return string
    def __repr__(self):
        return "'" + str(self) + "'"
    def __call__(self):
        """ """
        return logical_implies(self.P(), self.Q())
    def nand(self):
        """ """
        return NotImplemented
    def nor(self):
        """ """
        return NotImplemented

class IffOperation(BinaryOperation):
    """ An IffOperation is used to represent an Iff operation on two
        Atom objects. """
    def __init__(self, P, Q):
        """ """
        super().__init__(P, Q)
    def __str__(self):
        """ """
        string = ""
        if isinstance(self.P, Operation):
            string += '(' + str(self.P) + ')'
        else:
            string += str(self.P)
        string += ' ↔ '
        if isinstance(self.Q, Operation):
            string += '(' + str(self.Q) + ')'
        else:
            string += str(self.Q)
        return string
    def __repr__(self):
        return "'" + str(self) + "'"
    def __call__(self):
        """ """
        return logical_iff(self.P(), self.Q())
    def nand(self):
        """ """
        return NotImplemented
    def nor(self):
        """ """
        return NotImplemented

class NandOperation(BinaryOperation):
    """ An NandOperation is used to represent an NAND operation on two
        Atom objects. """
    def __init__(self, P, Q):
        """ """
        super().__init__(P, Q)
    def __str__(self):
        """ """
        string = ""
        if isinstance(self.P, Operation):
            string += '(' + str(self.P) + ')'
        else:
            string += str(self.P)
        string += ' | '
        if isinstance(self.Q, Operation):
            string += '(' + str(self.Q) + ')'
        else:
            string += str(self.Q)
        return string
    def __repr__(self):
        return "'" + str(self) + "'"
    def __call__(self):
        """ """
        return logical_nand(self.P(), self.Q())
    def nand(self):
        """ """
        super().nand()
        return self
    def nor(self):
        """ """
        super().nor()
        if type(self.P) is NandOperation and type(self.Q) is NandOperation: 
            if self.P.P is self.P.Q and self.Q.P is self.P.Q:
                return NorOperation(NorOperation(self.P.P, self.Q.P),
                                    NorOperation(self.P.Q, self.Q.Q))
            elif self.P.P is self.Q.P and self.P.Q is self.Q.Q:
                return NorOperation(NorOperation(self.P.P, self.Q.P),
                                    NorOperation(self.P.Q, self.Q.Q))
            elif self.P.P is self.Q.Q and self.P.Q is self.Q.P:
                return NorOperation(NorOperation(self.P.P, self.Q.Q),
                                    NorOperation(self.P.Q, self.Q.P))
        return NorOperation(NorOperation(
                                NorOperation(self.P, self.P), 
                                NorOperation(self.Q, self.Q)),
                            NorOperation(
                                NorOperation(self.P, self.P), 
                                NorOperation(self.Q, self.Q))) 

class NorOperation(BinaryOperation):
    """ An NorOperation is used to represent an NOR operation on two
        Atom objects. """
    def __init__(self, P, Q):
        """ """
        super().__init__(P, Q)
    def __str__(self):
        """ """
        string = ""
        if isinstance(self.P, Operation):
            string += '(' + str(self.P) + ')'
        else:
            string += str(self.P)
        string += ' ↓ '
        if isinstance(self.Q, Operation):
            string += '(' + str(self.Q) + ')'
        else:
            string += str(self.Q)
        return string
    def __repr__(self):
        return "'" + str(self) + "'"
    def __call__(self):
        """ """
        return logical_nor(self.P(), self.Q())
    def nand(self):
        """ """
        super().nand()
        return NandOperation(NandOperation(
                                NandOperation(self.P, self.P), 
                                NandOperation(self.Q, self.Q)),
                            NandOperation(
                                NandOperation(self.P, self.P), 
                                NandOperation(self.Q, self.Q))) 
    def nor(self):
        """ """
        super().nor()
        return self

def logical_not(P):
    return {
        False:True,
        True:False,
    }[P]

def logical_and(P, Q):
    return {
        False:
            {False:False,
             True:False},
        True:
            {False:False,
             True:True},
    }[P][Q]

def logical_or(P, Q):
    return {
        False:
            {False:False,
            True:True},
        True:
            {False:True,
            True:True},
    }[P][Q]

def logical_xor(P, Q):
    return {
        False:
            {False:False,
             True:True},
        True:
            {False:True,
             True:False},
    }[P][Q]

def logical_implies(P, Q):
    return {
        False:
            {False:True,
             True:True},
        True:
            {False:False,
             True:True},
    }[P][Q]

def logical_iff(P, Q):
    return {
        False:
            {False:True,
             True:False},
        True:
            {False:False,
             True:True},
    }[P][Q]

def logical_nand(P, Q):
    return {
        False:
            {False:True,
             True:True},
        True:
            {False:True,
             True:False},
    }[P][Q]

def logical_nor(P, Q):
    return {
        False:
            {False:True,
             True:False},
        True:
            {False:False,
             True:False},
    }[P][Q]

def permutations(sequence, length, permutation=None, permutation_set=None):
    if permutation is None or permutation_set is None:
        permutation = []
        permutation_set = []
    if len(permutation) == length:
        permutation_set.append(permutation)
        return permutation_set
    else:
        for item in sequence:
            permutations(sequence, length, permutation + [item], permutation_set)
    return permutation_set

