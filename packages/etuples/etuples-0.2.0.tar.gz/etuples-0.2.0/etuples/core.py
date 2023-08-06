import inspect
import reprlib

import toolz

from collections.abc import Sequence


etuple_repr = reprlib.Repr()
etuple_repr.maxstring = 100
etuple_repr.maxother = 100


class InvalidExpression(Exception):
    """An exception indicating that an `ExpressionTuple` is not a valid [S-]expression.

    This exception is raised when an attempt is made to evaluate an
    `ExpressionTuple` that does not have a valid operator (e.g. not a
    `callable`).

    """


class KwdPair(object):
    """A class used to indicate a keyword + value mapping.

    TODO: Could subclass `ast.keyword`.

    """

    __slots__ = ("arg", "value")

    def __init__(self, arg, value):
        assert isinstance(arg, str)
        self.arg = arg
        self.value = value

    @property
    def eval_obj(self):
        return KwdPair(self.arg, getattr(self.value, "eval_obj", self.value))

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.arg)}, {repr(self.value)})"

    def __str__(self):
        return f"{self.arg}={self.value}"

    def _repr_pretty_(self, p, cycle):
        p.text(str(self))

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self.arg == other.arg
            and self.value == other.value
        )

    def __hash__(self):
        return hash((type(self), self.arg, self.value))


class ExpressionTuple(Sequence):
    """A tuple-like object that represents an expression.

    This object caches the return value resulting from evaluation of the
    expression it represents.  Likewise, it holds onto the "parent" expression
    from which it was derived (e.g. as a slice), if any, so that it can
    preserve the return value through limited forms of concatenation/cons-ing
    that would reproduce the parent expression.

    TODO: Should probably use weakrefs for that.
    """

    __slots__ = ("_eval_obj", "_tuple", "_parent")
    null = object()

    def __new__(cls, seq=None, **kwargs):

        # XXX: This doesn't actually remove the entry from the kwargs
        # passed to __init__!
        # It does, however, remove it for the check below.
        kwargs.pop("eval_obj", None)

        if seq is not None and not kwargs and type(seq) == cls:
            return seq

        res = super().__new__(cls)

        return res

    def __init__(self, seq=None, **kwargs):
        """Create an expression tuple.

        If the keyword 'eval_obj' is given, the `ExpressionTuple`'s
        evaluated object is set to the corresponding value.
        XXX: There is no verification/check that the arguments evaluate to the
        user-specified 'eval_obj', so be careful.
        """

        _eval_obj = kwargs.pop("eval_obj", self.null)
        etuple_kwargs = tuple(KwdPair(k, v) for k, v in kwargs.items())

        if seq:
            self._tuple = tuple(seq) + etuple_kwargs
        else:
            self._tuple = etuple_kwargs

        # TODO: Consider making these a weakrefs.
        self._eval_obj = _eval_obj
        self._parent = None

    @property
    def eval_obj(self):
        """Return the evaluation of this expression tuple.

        Warning: If the evaluation value isn't cached, it will be evaluated
        recursively.

        """
        if len(self._tuple) == 0:
            raise InvalidExpression()

        if self._eval_obj is not self.null:
            return self._eval_obj
        else:
            op = self._tuple[0]
            op = getattr(op, "eval_obj", op)

            if not callable(op):
                raise InvalidExpression()

            evaled_args = [getattr(i, "eval_obj", i) for i in self._tuple[1:]]
            arg_grps = toolz.groupby(lambda x: isinstance(x, KwdPair), evaled_args)
            evaled_args = arg_grps.get(False, [])
            evaled_kwargs = arg_grps.get(True, [])

            try:
                op_sig = inspect.signature(op)
            except ValueError:
                # This handles some builtin function types
                _eval_obj = op(*(evaled_args + [kw.value for kw in evaled_kwargs]))
            else:
                op_args = op_sig.bind(
                    *evaled_args, **{kw.arg: kw.value for kw in evaled_kwargs}
                )
                op_args.apply_defaults()

                _eval_obj = op(*op_args.args, **op_args.kwargs)

            # assert not isinstance(_eval_obj, ExpressionTuple)

            self._eval_obj = _eval_obj
            return self._eval_obj

    @eval_obj.setter
    def eval_obj(self, obj):
        raise ValueError("Value of evaluated expression cannot be set!")

    def __add__(self, x):
        res = self._tuple + x
        if self._parent is not None and res == self._parent._tuple:
            return self._parent
        return type(self)(res)

    def __contains__(self, *args):
        return self._tuple.__contains__(*args)

    def __ge__(self, *args):
        return self._tuple.__ge__(*args)

    def __getitem__(self, key):
        tuple_res = self._tuple[key]
        if isinstance(key, slice) and isinstance(tuple_res, tuple):
            tuple_res = type(self)(tuple_res)
            tuple_res._parent = self
        return tuple_res

    def __gt__(self, *args):
        return self._tuple.__gt__(*args)

    def __iter__(self, *args):
        return self._tuple.__iter__(*args)

    def __le__(self, *args):
        return self._tuple.__le__(*args)

    def __len__(self, *args):
        return self._tuple.__len__(*args)

    def __lt__(self, *args):
        return self._tuple.__lt__(*args)

    def __mul__(self, *args):
        return type(self)(self._tuple.__mul__(*args))

    def __rmul__(self, *args):
        return type(self)(self._tuple.__rmul__(*args))

    def __radd__(self, x):
        res = x + self._tuple  # type(self)(x + self._tuple)
        if self._parent is not None and res == self._parent._tuple:
            return self._parent
        return type(self)(res)

    def __str__(self):
        return f"e({', '.join(tuple(str(i) for i in self._tuple))})"

    def __repr__(self):
        return f"ExpressionTuple({etuple_repr.repr(self._tuple)})"

    def _repr_pretty_(self, p, cycle):
        if cycle:
            p.text(f"e(...)")  # pragma: no cover
        else:
            with p.group(2, "e(", ")"):
                p.breakable(sep="")
                for idx, item in enumerate(self._tuple):
                    if idx:
                        p.text(",")
                        p.breakable()
                    p.pretty(item)

    def __eq__(self, other):
        return self._tuple == other

    def __hash__(self):
        return hash(self._tuple)


def etuple(*args, **kwargs):
    """Create an ExpressionTuple from the argument list.

    In other words:
        etuple(1, 2, 3) == ExpressionTuple((1, 2, 3))

    """
    return ExpressionTuple(args, **kwargs)
