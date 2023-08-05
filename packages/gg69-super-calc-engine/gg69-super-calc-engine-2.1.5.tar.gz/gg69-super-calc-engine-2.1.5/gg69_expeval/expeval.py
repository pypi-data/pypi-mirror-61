from queue import Queue
from colorama import Fore
from typing import Dict, Tuple
from .expeval_std import std_names, std_specific_operators, CharOperator, Namespace, Operator
from .ulib.killable_thread import KillableThread


class CalculationTimeoutExpired(Exception):
    pass


class ExpEval:
    names: Namespace
    specific_operators: Dict[str, CharOperator]

    def __init__(self, names=None, specific_operators=None):
        # config
        if names is None:
            self.names = std_names
        else:
            self.names = names
        if specific_operators is None:
            self.specific_operators = std_specific_operators
        else:
            self.specific_operators = specific_operators
        self.other_symbols = list("()[]{},;.")  # They all 1 char length
        # {"second": "first"}
        self.pares = {">": "<", "\\": "/"}
        self.brackets = {"(": ")", "[": "]", "{": "}"}
        self.sep = ","

        # execution levels
        self.execution_levels_pre_set = set()

        def manage_namespace_for_operators_e_l(ns: Namespace):
            for ns_name in ns.cont.values():
                if isinstance(ns_name, Namespace):
                    manage_namespace_for_operators_e_l(ns_name)
                elif isinstance(ns_name, Operator):
                    self.execution_levels_pre_set.add(ns_name.level)
        manage_namespace_for_operators_e_l(self.names)
        self.execution_levels = sorted(list(self.execution_levels_pre_set), reverse=True)

        # operator_symbols
        self.operator_symbols = set()
        for name in list(self.specific_operators) + list(self.pares):
            for ch in name:
                self.operator_symbols.add(ch)

        # max operator size
        self.mx_op_size = max(map(lambda n: len(n), self.specific_operators.keys()))

    def comp_exp(self, query) -> Tuple[str, bool]:
        """
        :param query: calculation query text
        :return: result, pretty_result, success
        """
        try:
            q = Queue()
            thread = KillableThread(target=lambda config, query, queue: queue.put(ExpEvalProcedure(config, query)()),
                                    args=(self, query, q))
            thread.start()
            thread.join(1)
            if thread.is_alive():
                thread.kill()
                raise CalculationTimeoutExpired()
            res = q.get()
            return res, True
        except Exception as err:
            return err.__class__.__name__ + " " + str(err), False


class ExpEvalProcedure:
    def __init__(self, config: ExpEval, query):
        self.config = config
        self.query = query

    def __call__(self):
        tokenizer = Tokenizer(self, self.query)
        tokens = tokenizer()
        executor = Executor(self, tokens)
        return executor()


from .tokenizer import Tokenizer
from .executor import Executor
