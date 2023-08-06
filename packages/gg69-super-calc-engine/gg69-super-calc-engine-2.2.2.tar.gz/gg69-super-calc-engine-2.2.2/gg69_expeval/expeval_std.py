from typing import Tuple, Callable, List
from .ulib import UsefulObj
from .gg69_shell.signal import Signal
from .miscellanea import *


class Operator(UsefulObj):
    level: int
    sides: Tuple[bool, bool, bool]
    func: Callable


class CompSingCopyOperator(Operator):
    def __init__(self, op: Operator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.import_from_parent(op, ("level", "sides", "func"))

    rev: bool = False
    from_heaven = []


class CharOperator(UsefulObj):
    replace: str
    allow_shuffle = False
    from_heaven = []
    branching = True


class CompOperator(UsefulObj):
    branches: List[CompSingCopyOperator]
    args_trick = ["branches"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = self.branches[0]

    def get_level(self):
        return min(map(lambda op: op.level, self.branches))


class Namespace(UsefulObj):
    cont: dict

    def apply_path(self, path: str, op_converting: bool = False):
        sp_res = path.split(".", 1)
        in_me = self.cont[sp_res[0]]
        if len(sp_res) == 1:
            return in_me if not op_converting else self.try_std_op_to_this(in_me)
        return in_me.apply_path(sp_res[1], op_converting)

    @staticmethod
    def try_std_op_to_this(maybe_op):
        if isinstance(maybe_op, Operator):
            return CompOperator(branches=[CompSingCopyOperator(maybe_op)])
        else:
            return maybe_op

    def __iter__(self):
        return self.cont.__iter__()

    def __getitem__(self, item: str):
        return self.apply_path(item)


def send_exit_signal_to_testing_shell():
    raise Signal("exit", "exiting from testing shell")


std_names = Namespace(cont={
    "comb": Namespace(cont={
        "comb_c": cnpk
    }),
    "pi": math.pi,
    "mod": Operator(level=1, sides=(True, True, True), func=lambda a, bl, c: a % bl[0] == c % bl[0]),
    "sqrt": math.sqrt,
    "exit": Operator(level=0, sides=(False, False, False), func=send_exit_signal_to_testing_shell),
    "__operators__": Namespace(cont={
        "__addition__": Operator(level=1, sides=(True, False, True), func=addition),
        "__fact__": Operator(level=3, sides=(True, False, False), func=math.factorial),
        "__multiplication__": Operator(level=2, sides=(True, False, True), func=lambda a, b: a * b),
        "__division__": Operator(level=2, sides=(True, False, True), func=lambda a, b: a / b),
        "__power__": Operator(level=3, sides=(True, False, True), func=lambda a, b: a ** b),
        "__less__": Operator(level=4, sides=(True, False, True), func=is_less),
        "__equals__": Operator(level=4, sides=(True, False, True), func=lambda a, b: a == b)
    })
})

# All keys should be False orientated and sorted
std_specific_operators = {
    "+": CharOperator(replace="__operators__.__addition__", from_heaven=[1]),
    "-": CharOperator(replace="__operators__.__addition__", from_heaven=[-1]),
    "!": CharOperator(replace="__operators__.__fact__", branching=False),
    "*": CharOperator(replace="__operators__.__multiplication__"),
    "/": CharOperator(replace="__operators__.__division__"),
    "**": CharOperator(replace="__operators__.__power__", branching=False),
    "<": CharOperator(replace="__operators__.__less__", from_heaven=[False], branching=False),
    "<=": CharOperator(replace="__operators__.__less__", from_heaven=[True], branching=False, allow_shuffle=True),
    "=": CharOperator(replace="__operators__.__less__", branching=False)
}
