class Model:

    def __init__(self):
        pass

    def exec_expr(self, expr):
        try:
            result = str(eval(expr, {}, {}))
        except Exception:
            result = "OP NOT SUPPORTED"

        return result