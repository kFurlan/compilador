class sintatico:
    def __init__(self, tokens):
         self.tokens = tokens

    def S(self):
        self.program()

    def program(self):
        if self.tokens.pop(0).value != "program":
            exit("Erro: esperava program")
        if self.tokens.pop(0).type not in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            exit("Erro: esperava um identificador")
        self.corpo()
        if self.tokens.pop(0).value != ".":
            exit("Erro: esperava um ponto final")
    def corpo(self):
        self.dc()
        if self.tokens.pop(0).value != "begin":
            exit("Erro: esperava um begin")
        self.comandos()
        if self.tokens.pop(0).value != "end":
            exit("Erro: esperava um end")

    def dc(self):
        if self.tokens[0].value == "var":
            self.dc_v()
            self.mais_dc()

        elif self.tokens[0].value == "procedure":
            self.dc_p()
            self.mais_dc()


    def comandos(self):
        self.comando()
        self.mais_comandos()

    def comando(self):
        if self.tokens[0].valeu == "read":
            if self.tokens.pop(0).value == "(":
                self.variaveis()
                if self.tokens.pop(0).value != ")":
                    exit("Erro")
            else:
                self.condicao()
                if self.tokens.pop(0).value == "do":
                    self.comandos()
                    if self.tokens.pop(0).value != "$":
                        exit("Erro: esperava $")

        elif self.tokens[0].value == "write":
            if self.tokens.pop(0).value == "(":
                self.variaveis()
                if self.tokens.pop(0).value != ")":
                    exit("Erro")
        elif self.tokens[0].value == "if":
            self.condicao()
            if self.tokens.pop(0).value == "then":
                self.comandos()
                self.pfalsa()
                if self.tokens.pop(0).value != "$":
                    exit("Erro: esperava um $")
        elif self.tokens[0].type not in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            self.restoIdent()
        else:
            exit("Erro")


    def dc_v(self):
        if self.tokens.pop(0).value != "var":
            exit("Erro: esperava um var")
        self.variaveis()
        if self.tokens.pop(0).value != ":":
            exit("Erro: esperava um :")
        self.tipo_var()

    def dc_p(self):
        if self.tokens.pop(0).value != "procedure":
            exit("Erro: esperava um procedure")
        if self.tokens.pop(0).type not in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            exit("Erro: esperava um identificador")
        self.parametros()
        self.corpo_p()

    def mais_dc(self):
        if self.tokens[0].value == ";":
            self.tokens.pop(0)
            self.dc()


    def variaveis(self):
        if self.tokens.pop(0).type not in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            exit("Erro: esperava um identificador")
        self.mais_var()

    def tipo_var(self):
        pass

    def mais_var(self):
        if self.tokens[0].value == ",":
            self.tokens.pop(0)
            self.variaveis()

    def restoIdent(self):
        if self.tokens[0].value != ":=":
            self.tokens.pop(0)
            self.expressao()
        else:
            self.list_arg()


    def condicao(self):
        self.expressao()
        self.relacao()
        self.expressao()

    def tipo_var(self):
        if self.tokens.pop(0) not in ("real", "integer"):
            exit("Erro: esperava um tipo real ou integer")

    def parametros(self):
        if self.tokens[0].value == "(":
            self.lista_par()
            if self.tokens.pop(0).value != ")":
                exit("Erro")

    def lista_par(self):
        self.variaveis()
        if self.tokens.pop(0).value != ":":
            exit("Erro: esperava ':'")
        self.tipo_var()
        self.mais_par()

    def mais_par(self):
        if self.tokens[0].value == ";":
            self.tokens.pop(0)
            self.lista_par()

    def corpo_p(self):
        self.dc_loc()
        if self.tokens.pop(0).value != "begin":
            exit("Erro: esperava um begin")
        self.comandos()
        if self.tokens.pop(0).value != "end":
            exit("Erro: esperava um end")

    def dc_loc(self):
        self.dc_v()
        self.mais_dcloc()

    def mais_dcloc(self):
        if self.tokens[0].value == ";":
            self.tokens.pop(0)
            self.dc_loc()

    def list_arg(self):
        if self.tokens[0].value == "(":
            self.argumentos()
            if self.tokens.pop(0).value != ")":
                exit("Erro")

    def argumentos(self):
        if self.tokens.pop(0).value not in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            exit("Erro: esperava um identificador")
        self.mais_ident()

    def mais_ident(self):
        if self.tokens[0].value == ";":
            self.tokens.pop(0)
            self.argumentos()

    def pfalsa(self):
        if self.tokens[0].value == "else":
            self.tokens.pop(0)
            self.comandos()

    def mais_comandos(self):
        if self.tokens[0].value == ";":
            self.tokens.pop(0)
            self.comandos()

    def relacao(self):
        if self.tokens.pop(0) not in ("=", "<>", ">=", "<=", ">", "<"):
            exit("Erro: esperava um operado relacional")

    def expressao(self):
        self.termo()
        self.outros_termos()

    def op_un(self):
        if self.tokens[0].value in ("+", "-"):
            self.tokens.pop(0)

    def outros_termos(self):
        self.op_ad()
        self.termo()
        self.outros_termos()

    def op_ad(self):
        if self.tokens.pop(0).value not in ("+", "-"):
            exit("Erro: esperava um operador de mais ou menos")
    def termo(self):
        self.op_un()
        self.fator()
        self.mais_fatores()

    def mais_fatores(self):
        self.op_mul()
        self.fator()
        self.mais_fatores()

    def op_mul(self):
        if self.tokens.pop(0).value not in ("*", "/"):
            exit("Erro: esperava um operador * ou  /")

    def fator(self):
        if  self.tokens[0].type not in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            exit("Erro: esperava um identificador")
        else:
            if self.tokens.pop(0).value == "(":
                self.expressao()
                if self.tokens.pop(0).value != ")":
                    print("Erro")
                    exit()










