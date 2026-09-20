from ExprVisitor import ExprVisitor
from ExprParser import ExprParser


class EvalVisitor(ExprVisitor):
    """
    Visitor que avalia expressões aritmeticas com suporte a:
    - Parenteses
    - Potenciacao (^)
    - Multiplicacao e divisao (* /)
    - Soma e subtracao (+ -)
    - Valor absoluto: abs(expr)
    - Fatorial: fat(expr)
    """

    def visitRoot(self, ctx: ExprParser.RootContext):
        return self.visit(ctx.expr())

    def visitParent(self, ctx: ExprParser.ParentContext):
        """'(' expr ')' repassa o valor da sub-expressao"""
        return self.visit(ctx.expr(0))

    def visitPot(self, ctx: ExprParser.PotContext):
        """expr '^' expr potenciacao"""
        base = self.visit(ctx.expr(0))
        exp = self.visit(ctx.expr(1))
        return base ** exp

    def visitMultDiv(self, ctx: ExprParser.MultDivContext):
        """expr ('*'|'/') expr  multiplicação ou divisão"""
        esq = self.visit(ctx.expr(0))
        dir = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()
        if op == '*':
            return esq * dir
        if dir == 0:
            raise ZeroDivisionError("Erro: divisão por zero.")
        return esq / dir

    def visitSomaSub(self, ctx: ExprParser.SomaSubContext):
        """expr ('+'|'-') expr  soma ou subtração"""
        esq = self.visit(ctx.expr(0))
        dir = self.visit(ctx.expr(1))
        op  = ctx.getChild(1).getText()
        if op == '+':
            return esq + dir
        else:
            return esq - dir

    def visitFunc(self, ctx: ExprParser.FuncContext):
        """(abs_ | fact) repassa o valor calculado pela função"""
        return self.visit(ctx.getChild(0))

    def visitNumber(self, ctx: ExprParser.NumberContext):
        """('-')? NUM número literal, possivelmente negativo"""
        texto = ctx.getText()
        return float(texto) if '.' in texto else int(texto)

    # funcoes auxiliares aqui embaixo
    
    def visitAbs_(self, ctx: ExprParser.Abs_Context):
        """abs(expr) — valor absoluto."""
        return abs(self.visit(ctx.expr()))

    def visitFact(self, ctx: ExprParser.FactContext):
        """fatorial (somente inteiros positivos)"""
        valor = self.visit(ctx.expr())
        if valor != int(valor) or valor < 0:
            raise ValueError(f"Erro: fatorial indefinido para {valor}.")
        return _fatorial(int(valor))



def _fatorial(n: int) -> int:
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado