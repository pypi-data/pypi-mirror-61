import operator
from typing import Any, Callable, Dict, Optional

from ratus.parse import BinaryOp, Expression, Function, Literal, UnaryOp


class ExecutorError(Exception):
    """Exception raised if there is an error executing an expression."""


class Executor:
    """Executor of expressions."""

    def __init__(
        self,
        functions: Optional[Dict[str, Callable[..., Any]]] = None,
        binary_ops: Optional[Dict[str, Callable[[Any, Any], Any]]] = None,
        unary_ops: Optional[Dict[str, Callable[[Any], Any]]] = None,
    ) -> None:
        """
        Instantiate an Executor object.

        This constructor provides three arguments to control behavior.

        `functions` allows us to extend the callable functions in expression. By default
        only `if` is provided but more can be added and the default definition of `if`
        (`lambda c, s, f: s if c else f`) can be overridden simple by having an "if" key
        in the `functions` dictionary.

        `binary_ops` allows us to extend the binary operations available. It is a
        dictionary mapping variants of `ratus.parse.BinaryOpTypes` to a function with
        two parameters and a single output.

        `unary_ops` allows us to extend the unary operations available. It is a
        dictionary mapping variants of `ratus.parse.UnaryOpTypes` to a function with one
        parameter and one outputs.
        """
        self.binary_ops: Dict[str, Callable[[Any, Any], Any]] = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            ">": operator.gt,
            ">=": operator.ge,
            "<": operator.lt,
            "<=": operator.le,
            "and": operator.and_,
            "or": operator.or_,
            "=": operator.eq,
            "!=": operator.ne,
        }
        if binary_ops is not None:
            self.binary_ops.update(binary_ops)

        self.unary_ops: Dict[str, Callable[[Any], Any]] = {
            "!": operator.not_,
            "-": operator.neg,
        }
        if unary_ops is not None:
            self.unary_ops.update(unary_ops)

        self.functions = {"if": lambda c, s, f: s if c else f}
        if functions is not None:
            self.functions.update(functions)

    def execute(self, expression: Expression) -> Any:
        """Execute an expression and return the result."""
        if isinstance(expression, Literal):
            return expression.value
        if isinstance(expression, BinaryOp):
            left = self.execute(expression.left)
            right = self.execute(expression.right)
            binary_op = self.binary_ops[expression.op_type.value]
            return binary_op(left, right)
        if isinstance(expression, UnaryOp):
            operand = self.execute(expression.operand)
            unary_op = self.unary_ops[expression.op_type.value]
            return unary_op(operand)
        if isinstance(expression, Function):
            function = self.functions.get(expression.name)
            if function is None:
                raise ExecutorError(f"Function '{expression.name}' is not defined")
            args = [self.execute(arg) for arg in expression.args]
            return function(*args)
