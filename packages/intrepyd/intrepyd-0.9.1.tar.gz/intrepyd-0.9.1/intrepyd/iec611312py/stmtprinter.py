"""
Copyright (C) 2018 Roberto Bruttomesso <roberto.bruttomesso@gmail.com>

This file is distributed under the terms of the 3-clause BSD License.
A copy of the license can be found in the root directory or at
https://opensource.org/licenses/BSD-3-Clause.

Author: Roberto Bruttomesso <roberto.bruttomesso@gmail.com>
  Date: 02/11/2018

This module implements a printer for the parsed AST
"""

from intrepyd.iec611312py.visitor import Visitor
from intrepyd.iec611312py.statement import Assignment
from intrepyd.iec611312py.expression import VariableOcc, Expression

def termAsString(term):
    printer = StmtPrinter()
    printer.visit(term)
    return printer.result

class StmtPrinter(Visitor):
    """
    Visitor for printing Statements on a string
    """
    def __init__(self):
        self._result = ''

    @property
    def result(self):
        return self._result

    def processStatements(self, statements):
        for statement in statements:
            statement.accept(self)

    def _visit_assignment(self, obj):
        obj.lhs.accept(self)
        self._result += ' := '
        obj.rhs.accept(self)
        self._result += ';'

    def _visit_ifthenelse(self, obj):
        first = True
        if len(obj.conditions) != len(obj.stmt_blocks):
            raise RuntimeError('Wrong number of conditions and statements in if then else')
        for i in range(len(obj.conditions)):
            if first:
                self._result += 'IF '
                first = False
            else:
                self._result += 'ELSIF '
            obj.conditions[i].accept(self)
            self._result += ' THEN '
            for statement in obj.stmt_blocks[i]:
                statement.accept(self)
                self._result += ' '
        self._result += 'END_IF;'
    
    def _visit_case(self, obj):
        selections = obj.selections
        statements = obj.stmt_blocks
        if len(selections) != len(statements):
            raise RuntimeError('Wrong number of selections and statements in case')
        self._result += 'CASE '
        obj.expression.accept(self)
        self._result += ' OF '
        for i in range(len(selections)):
            for selection in selections[i]:
                selection.accept(self)
            self._result += ': '
            for statement in statements[i]:
                statement.accept(self)
                self._result += ' '
        self._result += 'END_CASE;'

    def _visit_expression(self, expression):
        args = expression.arguments
        nargs = len(args)
        if nargs == 1:
            self._result += expression.operator + '('
            expression.arguments[0].accept(self)
            self._result += ')'
            return
        elif nargs == 2:
            self._result += '('
            args[0].accept(self)
            self._result += ' ' + expression.operator + ' '
            args[1].accept(self)
            self._result += ')'

    def _visit_ite(self, ite):
        self._result += 'ite('
        ite.condition.accept(self)
        self._result += ', '
        ite.then_term.accept(self)
        self._result += ', '
        ite.else_term.accept(self)
        self._result += ')'

    def _visit_variable_occ(self, variableOcc):
        self._result += variableOcc.var.name

    def _visit_constant_occ(self, constantOcc):
        self._result += constantOcc.cst
