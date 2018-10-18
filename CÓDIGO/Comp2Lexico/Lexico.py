palavraReservada = ('var', 'integer', 'real', 'if', 'then', 'while', 'do', 'write', 'read', 'else', 'begin', 'end', 'program')
simbolo = ('+', '-', '=', '<', '>', '(', ')', '.', ',', ':', ';', '$', ':=', '<>', '<=', '>=', '/')
comentario = ('/', '*', '{', '}')


class Token:
    def __init__(self, _value, _type, _index):
        self._type = _type
        self._value = _value
        self._index = _index

    ind = property(lambda self: self._index)
    value = property(lambda self: self._value)
    type = property(lambda  self: self._type)

    def __str__(self):
        return "{} {} => {}".format(self._value, self._type, self._index)

    __repr__ = __str__


def peek(l, ch):
    if len(l) - 1 > l.index(ch):
        return l[l.index(ch) + 1]
    return ch


def isreal(num):
    if '.' not in num:
        return False
    i = num.index('.')
    return num[:i].isnumeric() and num[i + 1:].isnumeric()


def tokenizer(l, i):
    isComentario = False
    s = ''
    tokens = []
    for ch in l + ' ':
        if ch == '{' or (ch == '/' and peek(l, ch) == '*'):
            isComentario = True

        if ch == '}' or (ch == '*' and peek(l, ch) == '/'):
            isComentario = False
            continue

        if isComentario:
            continue

        if ch in simbolo or ch in (' ', '\n', '\t'):

            if s in simbolo:
                tokens.append(Token(s, "Símbolo composto", i))
                s = ''
                continue
            if s in palavraReservada:
                tokens.append(Token(s, "Palavra reservada", i))
            elif s.isalpha():
                tokens.append(Token(s, "Identificador", i))
            elif s.isnumeric():
                tokens.append(Token(s, "Identificador numérico inteiro", i))
            elif isreal(s):
                tokens.append(Token(s, "Identificador numérico real", i))
            s = ''

            if ch == ':' and peek(l, ch) == '=':
                s = ':='
            elif ch == '<' and peek(l, ch) == '>':
                s = '<>'
            elif ch == '<' and peek(l, ch) == '=':
                s = '<='
            elif ch == '>' and peek(l, ch) == '=':
                s = '>='
            elif ch in simbolo:

                tokens.append(Token(ch, "Símbolo simples", i))
        else:
            s += ch

    return tokens


if __name__ == '__main__':
    from Sintatico import sintatico
    with open('arquivo.txt', 'r') as arq:
        tokens = []
        for i, l in enumerate(arq):
            tokens += tokenizer(l, i)
        print(tokens)
        CompSintatico = sintatico(tokens)
        CompSintatico.S()

        print('Cadeia aceita')
