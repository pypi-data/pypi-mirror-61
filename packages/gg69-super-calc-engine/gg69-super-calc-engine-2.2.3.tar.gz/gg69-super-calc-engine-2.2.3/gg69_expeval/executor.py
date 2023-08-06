from typing import List, Tuple
from .expeval import ExpEvalProcedure
from .tokenizer import Token
from .expeval_std import Namespace, Operator, CompOperator, CompSingCopyOperator
from useless_lib.useful import UsefulSet


class Executor:
    def __init__(self, procedure: ExpEvalProcedure, tokens):
        self.procedure = procedure
        self.env: List = tokens.copy()

    def replace_range(self, start, length, value):
        self.env[start] = value
        before = self.env[:start + 1]
        after = self.env[start + length:]
        self.env = before + after

    @staticmethod
    def execute_single_operator(single_operator: CompSingCopyOperator, left_n_right, dop):
        if single_operator.rev:
            left_n_right = left_n_right[::-1]
        op_func_result = single_operator.func(*(left_n_right + dop + single_operator.from_heaven))
        return op_func_result

    @staticmethod
    def get_token_val_for_operator(token):
        return None if isinstance(token, (Token, CompOperator)) else token

    def brackets(self, sti, bracket, mode):
        """
        :param sti:
        :param bracket:
        :param mode:
        0 - prosto skobki
        1 - called
        2 - (,  or  ,,  or  ,)
        :return: something if mode = 2 and nothing in other case
        """
        end_bracket = self.procedure.config.brackets[bracket]
        if mode == 1:
            p = sti
            res = UsefulSet() if bracket == "{" else []
            sectors_count = 0
            while True:
                elem = self.brackets(p, bracket, 2)
                # Crutch
                if bracket == "{":
                    res.add(elem)
                else:
                    res.append(elem)
                sectors_count += 1
                p += 2
                if self.env[p].token == end_bracket:
                    break
            self.replace_range(sti, 2 * sectors_count + 1, res)
        else:
            p = sti + 1
            while True:
                if isinstance(self.env[p], Token):
                    tk: Token = self.env[p]
                    if tk.token == end_bracket:
                        break
                    elif tk.token == self.procedure.config.sep:
                        if mode == 2:
                            break
                        else:
                            raise Exception("Are you stupid? Wtf a separator doing here (%d)" % tk.st)
                    elif tk.op:
                        br = self.env.pop(p).token
                        transformed: List[CompSingCopyOperator] = []
                        for op_writing, rev in br:
                            char_op = self.procedure.config.specific_operators[op_writing]
                            new_transformed_sing_op = CompSingCopyOperator(self.procedure.config.names[char_op.replace])
                            transformed.append(new_transformed_sing_op)
                            transformed[-1].rev = rev
                            transformed[-1].from_heaven = char_op.from_heaven
                        self.env.insert(p, CompOperator(branches=transformed))
                    elif tk.val:
                        self.env[p] = float(self.env[p].token)
                    elif tk.token == "(":
                        # Bracket for functions
                        called_by_func = callable(self.env[p - 1])
                        called_by_operator = isinstance(self.env[p - 1], CompOperator) and self.env[p - 1].model.sides[1]
                        self.brackets(p, tk.token, 1 if called_by_func or called_by_operator else 0)
                        if called_by_func:
                            p -= 1
                            func_res = self.env[p](*(self.env[p + 1]))
                            self.replace_range(p, 2, func_res)
                    elif tk.token in self.procedure.config.brackets:
                        # Other brackets
                        self.brackets(p, tk.token, 1)
                    elif tk.word:
                        from_root_val = self.procedure.config.names.apply_path(self.env.pop(p).token, True)
                        self.env.insert(p, from_root_val)
                    elif tk.token == ".":
                        # At this place, point is using only to use "namespaces".
                        ns = self.env[p - 1]
                        wrd_tok = self.env[p + 1]
                        if not (isinstance(ns, Namespace) and wrd_tok.word):
                            raise Exception("Point that doesn't bind namespace and link at place % d (It proves, that you are down)" % tk.st)
                        next_val = ns.apply_path(wrd_tok.token, True)
                        p -= 1
                        self.replace_range(p, 3, next_val)
                p += 1

            for cur_level in self.procedure.config.execution_levels:
                p = sti + 1
                while True:
                    if isinstance(self.env[p], Token):
                        if self.env[p].token in (end_bracket, self.procedure.config.sep):
                            break
                    elif isinstance(self.env[p], CompOperator):
                        operator: CompOperator = self.env[p]
                        if operator.get_level() == cur_level:
                            # left, right, dop, from_heaven
                            dop_information = []
                            left_n_right = []
                            if operator.model.sides[1]:
                                # Нам не мешает никак
                                dop_information = self.env.pop(p + 1)
                            if operator.model.sides[0]:
                                # TODO: remove crutches
                                val_for_op = self.get_token_val_for_operator(self.env[p - 1])
                                if val_for_op is None:
                                    left_n_right.append(None)
                                else:
                                    self.env.pop(p - 1)
                                    left_n_right.append(val_for_op)
                                    p -= 1
                            if operator.model.sides[2]:
                                val_for_op = self.get_token_val_for_operator(self.env[p + 1])
                                if val_for_op is None:
                                    left_n_right.append(None)
                                else:
                                    self.env.pop(p + 1)
                                    left_n_right.append(val_for_op)

                            if len(operator.branches) == 1:
                                op_res = self.execute_single_operator(operator.model, left_n_right.copy(), dop_information)
                            else:
                                op_res = UsefulSet()
                                for single_operator in operator.branches:
                                    op_res.add(self.execute_single_operator(single_operator, left_n_right.copy(), dop_information))
                            self.replace_range(p, 1, op_res)
                    p += 1

            res = self.env[sti + 1]
            if mode == 0:
                self.replace_range(sti, 3, res)
            else:
                return res

    def error_when_you_dont_know_anything_about_error(self):
        raise Exception("Something went wrong\n{}".format(str(self.env)))

    def __call__(self):
        self.env.insert(0, Token("("))
        self.env.append(Token(")"))
        self.brackets(0, "(", 0)
        # crutch, but it works
        if len(self.env) != 1:
            self.error_when_you_dont_know_anything_about_error()
        res = self.env[0]
        if isinstance(res, (Token, CompOperator)):
            self.error_when_you_dont_know_anything_about_error()
        return res
