import re

from grako import exceptions

from django.db.models import constants

from . import expression_parser


class LookupExpression(object):
    """
    Describes a registry lookup expression.
    """

    registration_point = None
    registry_id = None
    constraints = None
    field = None

    def __init__(self, registration_point=None, registry_id=None, field=None, constraints=None):
        self.registration_point = registration_point
        self.registry_id = registry_id
        self.field = field
        self.constraints = constraints

    def apply_constraints(self, queryset):
        """
        Applies all constraints contained in the lookup expression.

        :param queryset: Queryset to apply the constraints to
        :return: Queryset with all constraints applied
        """

        for constraint in self.constraints:
            queryset = constraint.apply(queryset)

        return queryset

    @property
    def name(self):
        """
        Returns an identifier suitable for representing this lookup expression
        in an attribute.
        """

        return '%s%s%s' % (
            self.registration_point.replace('.', '_') if self.registration_point else '',
            self.registry_id.replace('.', '_') if self.registry_id else '',
            '_'.join(self.field or []),
        )

    def __repr__(self):
        return '<LookupExpression registration_point=\'%s\' registry_id=\'%s\' constraints=\'%s\' field=\'%s\'>' % (
            self.registration_point,
            self.registry_id,
            self.constraints,
            '.'.join(self.field) if self.field else ''
        )


class Lookup(object):
    def __init__(self, operator, field, value):
        self.operator = operator
        self.field = constants.LOOKUP_SEP.join(field)
        self.value = value

    def apply(self, queryset):
        return queryset.filter(**{self.field: self.value})

    def __repr__(self):
        return '%s %s %s' % (self.field, self.operator, self.value)


class LookupExpressionSemantics(expression_parser.LookupExpressionSemantics):
    def constraint(self, ast):
        return Lookup(ast.operator, ast.field, ast.value)

    def INTEGER(self, ast):
        return int(ast)

    def STRING(self, ast):
        return ''.join(ast)


class LookupExpressionParser(object):
    """
    A parser for registry lookup expressions.
    """

    def __init__(self):
        self._parser = expression_parser.LookupExpressionParser()
        self._semantics = LookupExpressionSemantics()

    def parse(self, expression):
        try:
            ast = self._parser.parse(expression, rule_name='lookup', semantics=self._semantics)
        except exceptions.FailedParse:
            raise ValueError('Invalid registry lookup expression: %s' % expression)

        # Construct a lookup expression from the AST.
        return LookupExpression(
            registration_point=ast.registration_point,
            registry_id='.'.join(ast.registry_id),
            field=ast.field,
            constraints=ast.constraints,
        )
