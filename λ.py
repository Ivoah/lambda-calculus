import sys

class Lambda:
    def __init__(self, arg, body):
        self.arg = arg
        self.body = body

    def __str__(self):
        #return f'(λ{self.arg}.{self.body})'
        return f'(lambda {self.arg}: {self.body})'

    def eval(self):
        return eval(str(self), {'PRINT_BYTE': lambda f: print(f(lambda x: x + 1)(0))})

class Application:
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __str__(self):
        #return f'({self.func} {self.arg})'
        return f'{self.func}' + ''.join(f'({arg})' for arg in self.args)

    def eval(self):
        return eval(str(self), {'PRINT_BYTE': lambda f: print(f(lambda x: x + 1)(0))})

class Var:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

def pull(s):
    parens = 0
    for i, c in enumerate(s):
        if c == '(': parens += 1
        elif c == ')': parens -= 1
        if parens == -1 or (c == ' ' and parens <= 0): return s[:i]
    return s

def tokenize(string):
    res = []
    cur = ''
    for c in string:
        if c in '(λ. )':
            if cur:
                res.append(cur)
                cur = ''
            res.append(c)
        else:
            cur += c
    if cur:
        res.append(cur)
    return res

def parse(expr):
    if expr[0] == '(':
        if expr[1] == 'λ':
            return Lambda(expr[2], parse(pull(expr[4:-1])))
        else:
            func = pull(expr[1:])
            l = len(func)
            args = []
            while l < len(expr) - 2:
                arg = pull(expr[l + 2:])
                l += len(arg) + 1
                args.append(parse(arg))
            return Application(parse(func), args)
    elif expr[0] == 'λ':
        return Lambda(expr[1], parse(pull(expr[3:])))
    else:
        return Var(expr[0])

with open(sys.argv[1]) as f:
    lines = f.read().strip().split('\n')
    lines = [l for l in lines if len(l) > 0 and l[0] != '#']
    expr = lines[-1]
    for var in lines[-2::-1]:
        var = list(map(str.strip, var.split('=')))
        expr = expr.replace(var[0], f'({var[1]})')

    parse(tokenize(expr)).eval()
