#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

from grako.parsing import graken, Parser
from grako.util import re, RE_FLAGS, generic_main  # noqa


__version__ = (2016, 4, 16, 20, 9, 18, 5)

__all__ = [
    'LookupExpressionParser',
    'LookupExpressionSemantics',
    'main'
]

KEYWORDS = set([])


class LookupExpressionParser(Parser):
    def __init__(self,
                 whitespace=None,
                 nameguard=None,
                 comments_re=None,
                 eol_comments_re=None,
                 ignorecase=None,
                 left_recursion=True,
                 keywords=KEYWORDS,
                 **kwargs):
        super(LookupExpressionParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            keywords=keywords,
            **kwargs
        )

    @graken()
    def _lookup_(self):
        with self._optional():
            self._registration_point_()
            self.name_last_node('registration_point')
        self._registry_id_()
        self.name_last_node('registry_id')
        with self._optional():
            self._constraint_specifier_()
            self.name_last_node('constraints')
        with self._optional():
            self._field_specifier_()
            self.name_last_node('field')
        self._check_eof()

        self.ast._define(
            ['registration_point', 'registry_id', 'constraints', 'field'],
            []
        )

    @graken()
    def _registration_point_(self):
        self._FIELD_()
        self.name_last_node('@')
        self._token(':')

    @graken()
    def _registry_id_(self):

        def sep0():
            self._token('.')

        def block0():
            self._REGISTRY_ID_ATOM_()
        self._positive_closure(block0, prefix=sep0)

    @graken()
    def _REGISTRY_ID_ATOM_(self):
        self._pattern(r'[a-zA-Z0-9]+')

    @graken()
    def _field_specifier_(self):
        self._token('__')
        self._fields_()
        self.name_last_node('@')

    @graken()
    def _fields_(self):

        def sep0():
            self._token('__')

        def block0():
            self._FIELD_()
        self._positive_closure(block0, prefix=sep0)

    @graken()
    def _FIELD_(self):
        self._pattern(r'([a-zA-Z0-9]|_(?!_))+')

    @graken()
    def _constraint_specifier_(self):
        self._token('[')
        self._constraints_()
        self.name_last_node('@')
        self._token(']')

    @graken()
    def _constraints_(self):

        def sep0():
            with self._group():
                self._CONSTRAINT_SEPARATOR_()

        def block0():
            self._constraint_()
        self._positive_closure(block0, prefix=sep0)

    @graken()
    def _constraint_(self):
        self._fields_()
        self.name_last_node('field')
        self._operator_()
        self.name_last_node('operator')
        self._CONSTANT_()
        self.name_last_node('value')

        self.ast._define(
            ['field', 'operator', 'value'],
            []
        )

    @graken()
    def _operator_(self):
        self._token('=')

    @graken()
    def _CONSTRAINT_SEPARATOR_(self):
        self._token(',')

    @graken()
    def _CONSTANT_(self):
        with self._choice():
            with self._option():
                self._INTEGER_()
            with self._option():
                self._STRING_()
            self._error('no available options')

    @graken()
    def _INTEGER_(self):
        self._pattern(r'[0-9]+')

    @graken()
    def _STRING_(self):
        self._token('"')

        def block1():
            with self._choice():
                with self._option():
                    self._pattern(r'[^"\n\\]')
                with self._option():
                    self._ESC_()
                self._error('expecting one of: [^"\\n\\\\]')
        self._closure(block1)
        self.name_last_node('@')
        self._token('"')

    @graken()
    def _ESC_(self):
        self._pattern(r'\\["\\]')


class LookupExpressionSemantics(object):
    def lookup(self, ast):
        return ast

    def registration_point(self, ast):
        return ast

    def registry_id(self, ast):
        return ast

    def REGISTRY_ID_ATOM(self, ast):
        return ast

    def field_specifier(self, ast):
        return ast

    def fields(self, ast):
        return ast

    def FIELD(self, ast):
        return ast

    def constraint_specifier(self, ast):
        return ast

    def constraints(self, ast):
        return ast

    def constraint(self, ast):
        return ast

    def operator(self, ast):
        return ast

    def CONSTRAINT_SEPARATOR(self, ast):
        return ast

    def CONSTANT(self, ast):
        return ast

    def INTEGER(self, ast):
        return ast

    def STRING(self, ast):
        return ast

    def ESC(self, ast):
        return ast


def main(
        filename,
        startrule,
        trace=False,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        left_recursion=True,
        **kwargs):

    with open(filename) as f:
        text = f.read()
    parser = LookupExpressionParser(parseinfo=False)
    ast = parser.parse(
        text,
        startrule,
        filename=filename,
        trace=trace,
        whitespace=whitespace,
        nameguard=nameguard,
        ignorecase=ignorecase,
        **kwargs)
    return ast

if __name__ == '__main__':
    import json
    ast = generic_main(main, LookupExpressionParser, name='LookupExpression')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()
