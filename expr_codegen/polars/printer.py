from sympy import Basic, Function, StrPrinter
from sympy.printing.precedence import precedence


# TODO: 如有新添加函数，需要在此补充对应的打印代码

class PolarsStrPrinter(StrPrinter):
    def _print(self, expr, **kwargs) -> str:
        """Internal dispatcher

        Tries the following concepts to print an expression:
            1. Let the object print itself if it knows how.
            2. Take the best fitting method defined in the printer.
            3. As fall-back use the emptyPrinter method for the printer.
        """
        self._print_level += 1
        try:
            # If the printer defines a name for a printing method
            # (Printer.printmethod) and the object knows for itself how it
            # should be printed, use that method.
            if self.printmethod and hasattr(expr, self.printmethod):
                if not (isinstance(expr, type) and issubclass(expr, Basic)):
                    return getattr(expr, self.printmethod)(self, **kwargs)

            # See if the class of expr is known, or if one of its super
            # classes is known, and use that print function
            # Exception: ignore the subclasses of Undefined, so that, e.g.,
            # Function('gamma') does not get dispatched to _print_gamma
            classes = type(expr).__mro__
            # if AppliedUndef in classes:
            #     classes = classes[classes.index(AppliedUndef):]
            # if UndefinedFunction in classes:
            #     classes = classes[classes.index(UndefinedFunction):]
            # Another exception: if someone subclasses a known function, e.g.,
            # gamma, and changes the name, then ignore _print_gamma
            if Function in classes:
                i = classes.index(Function)
                classes = tuple(c for c in classes[:i] if \
                                c.__name__ == classes[0].__name__ or \
                                c.__name__.endswith("Base")) + classes[i:]
            for cls in classes:
                printmethodname = '_print_' + cls.__name__
                printmethod = getattr(self, printmethodname, None)
                if printmethod is not None:
                    return printmethod(expr, **kwargs)
            # Unknown object, fall back to the emptyPrinter.
            return self.emptyPrinter(expr)
        finally:
            self._print_level -= 1

    def _print_Symbol(self, expr):
        # return f"pl.col('{expr.name}')"
        return expr.name

    # 此处代码保留做为二次开发的示例
    # def _print_Equality(self, expr):
    #     PREC = precedence(expr)
    #     return "%s==%s" % (self.parenthesize(expr.args[0], PREC), self.parenthesize(expr.args[1], PREC))

    def _print_Equality(self, expr):
        PREC = precedence(expr)
        return "%s==%s" % (self.parenthesize(expr.args[0], PREC), self.parenthesize(expr.args[1], PREC))

    def _print_if_else(self, expr):
        return "if_else(%s, %s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]), self._print(expr.args[2]))

    def _print_ts_mean(self, expr):
        return "ts_mean(%s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]))

    def _print_ts_std_dev(self, expr):
        return "ts_std_dev(%s, %s, ddof=0)" % (self._print(expr.args[0]), self._print(expr.args[1]))

    def _print_ts_arg_max(self, expr):
        return "ts_arg_max(%s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]))

    def _print_ts_arg_min(self, expr):
        return "ts_arg_min(%s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]))

    def _print_ts_product(self, expr):
        return "ts_product(%s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]))

    def _print_ts_max(self, expr):
        return "ts_max(%s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]))

    def _print_ts_min(self, expr):
        return "ts_min(%s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]))

    def _print_ts_delta(self, expr):
        return "ts_delta(%s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]))

    def _print_ts_delay(self, expr):
        return "ts_delay(%s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]))

    def _print_ts_corr(self, expr):
        return "ts_corr(%s, %s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]), self._print(expr.args[2]))

    def _print_ts_covariance(self, expr):
        return "ts_covariance(%s, %s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]), self._print(expr.args[2]))

    def _print_ts_rank(self, expr):
        return "ts_rank(%s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]))

    def _print_ts_sum(self, expr):
        return "ts_sum(%s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]))

    def _print_ts_decay_linear(self, expr):
        return "ts_decay_linear(%s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]))

    def _print_cs_rank(self, expr):
        return "cs_rank(%s)" % self._print(expr.args[0])

    def _print_cs_scale(self, expr):
        return "cs_scale(%s)" % self._print(expr.args[0])

    def _print_log(self, expr):
        if expr.args[0].is_Number:
            return "np.log(%s)" % expr.args[0]
        else:
            return "log(%s)" % self._print(expr.args[0])

    def _print_Abs(self, expr):
        if expr.args[0].is_Number:
            return "np.abs(%s)" % expr.args[0]
        else:
            return "abs_(%s)" % self._print(expr.args[0])

    def _print_Max(self, expr):
        return "max_(%s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]))

    def _print_Min(self, expr):
        return "min_(%s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]))

    def _print_sign(self, expr):
        if expr.args[0].is_Number:
            return "np.sign(%s)" % expr.args[0]
        else:
            return "sign(%s)" % self._print(expr.args[0])

    def _print_signed_power(self, expr):
        return "signed_power(%s, %s)" % (self._print(expr.args[0]), self._print(expr.args[1]))

    def _print_gp_rank(self, expr):
        return "cs_rank(%s)" % self._print(expr.args[1])

    def _print_gp_demean(self, expr):
        return "neutralize_demean(%s)" % self._print(expr.args[1])
