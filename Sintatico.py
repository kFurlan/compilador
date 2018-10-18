tabela_TS = {}
lista_token=[]
cat = ""
global 
def inserir_TS(token, cat):
    global tabela_TS
    insert_ts = {token._value: {"Token": token._type, "Categoria": cat,"Index": token._index}}
    busca_ts = get_ts(token)
    if busca_ts == None:
        tabela_TS.update(insert_ts)
    else:
        print("Variável já declarada: ", (token._value))
        return False
    return True


def get_ts(token):
    global tabela_TS
    get_dict = tabela_TS.get(token._value)
    return get_dict

def erro(token, esperado):
    print("Erro de sintaxe: linha {} | esperado: {} | entrada: {}"
          "".format(token.ind,esperado, token.value))
    exit()

class sintatico:
    def __init__(self, tokens):
         self.tokens = tokens

    def S(self):
        self.program()
        print("oi")
        print(tabela_TS)


    def program(self):
        if self.tokens.pop(0).value != "program":
            exit("Erro1: esperava program")
        if self.tokens.pop(0).type not in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            exit("Erro2: esperava um identificador")
        self.corpo()
        if self.tokens.pop(0).value != ".":
            exit("Erro3: esperava um ponto final")
        print("ponto")

    def corpo(self):
        self.dc()
        if self.tokens.pop(0).value != "begin":
            exit("Erro4: esperava um begin")
        self.comandos()
        token = self.tokens.pop(0)
        if token.value != "end":
            exit("Erro5: esperava um end")

    def dc(self):
        global cat
        if self.tokens[0].value == "var":
            cat = "var"
            self.dc_v()
            self.mais_dc()
        elif self.tokens[0].value == "procedure":
            cat = "proc"
            self.dc_p()
            self.mais_dc()

    def comandos(self):
        self.comando()
        self.mais_comandos()

    def comando(self):
        if self.tokens[0].value == "while":
            self.tokens.pop(0)
            self.condicao()
            if self.tokens.pop(0).value == "do":
                self.comandos()
                if self.tokens.pop(0).value != "$":
                    exit("Erro7: esperava $")

        elif self.tokens[0].value == "write":
            self.tokens.pop(0)
            if self.tokens.pop(0).value == "(":
                self.variaveis()
                if self.tokens.pop(0).value != ")":
                    exit("Erro8")

        elif self.tokens[0].value == "if":
            self.tokens.pop(0)
            self.condicao()
            if self.tokens.pop(0).value == "then":
                self.comandos()
                self.pfalsa()
                if self.tokens.pop(0).value != "$":
                    exit("Erro9: esperava um $")

        elif self.tokens[0].value == "read":
            self.tokens.pop(0)
            if self.tokens.pop(0).value == "(":
                self.variaveis()
                if self.tokens.pop(0).value != ")":
                    exit("ErroNOVO")

        elif self.tokens[0].type in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            self.tokens.pop(0)
            self.restoIdent()
        else:
            exit("Erro10")


    def dc_v(self):
        if self.tokens.pop(0).value != "var":
            exit("Erro11: esperava um var")
        self.variaveis()
        if self.tokens.pop(0).value != ":":
            exit("Erro12: esperava um :")
        self.tipo_var()

    def dc_p(self):
        token = self.tokens.pop(0)
        if token.value != "procedure":
            exit("Erro13: esperava um procedure")
        if token.type not in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            exit("Erro14: esperava um identificador")
        inserir_TS(token,cat)
        self.parametros()
        self.corpo_p()

    def mais_dc(self):
        if self.tokens[0].value == ";":
            self.tokens.pop(0)
            self.dc()


    def variaveis(self):
        token = self.tokens.pop(0)
        if token.type not in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            exit("Erro15: esperava um identificador")
        inserir_TS(token,cat)
        self.mais_var()

    def mais_var(self):
        if self.tokens[0].value == ",":
            self.tokens.pop(0)
            self.variaveis()

    def restoIdent(self):
        if self.tokens[0].value == ":=":
            self.tokens.pop(0)
            self.expressao()
        else:
            self.list_arg()


    def condicao(self):
        self.expressao()
        self.relacao()
        self.expressao()

    def tipo_var(self):
        token = self.tokens.pop(0)
        if token.value not in ("real", "integer"):
            exit("Erro16: esperava um tipo real ou integer")
        inserir_TS(token,cat)


    def parametros(self):
        global cat
        if self.tokens.pop(0).value == "(":
            cat = "param"
            self.lista_par()
            if self.tokens.pop(0).value != ")":
                exit("Erro16")

    def lista_par(self):
        self.variaveis()
        if self.tokens.pop(0).value != ":":
            exit("Erro17: esperava ':'")
        self.tipo_var()
        self.mais_par()

    def mais_par(self):
        if self.tokens[0].value == ";":
            self.tokens.pop(0)
            self.lista_par()

    def corpo_p(self):
        self.dc_loc()
        global cat
        cat = "var"
        if self.tokens.pop(0).value != "begin":
            exit("Erro18: esperava um begin")
        self.comandos()
        if self.tokens.pop(0).value != "end":
            exit("Erro19: esperava um end")

    def dc_loc(self):
        if self.tokens[0].value != "var":
            self.dc_v()
            self.mais_dcloc()

    def mais_dcloc(self):
        if self.tokens[0].value == ";":
            self.tokens.pop(0)
            self.dc_loc()

    def list_arg(self):
        if self.tokens[0].value == "(":
            self.tokens.pop(0)
            self.argumentos()
            if self.tokens.pop(0).value != ")":
                exit("Erro20")

    def argumentos(self):
        if self.tokens.pop(0).type not in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            exit("Erro21: esperava um identificador")
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
        if self.tokens.pop(0).value not in ("=", "<>", ">=", "<=", ">", "<"):
            exit("Erro22: esperava um operado relacional")

    def expressao(self):
        self.termo()
        self.outros_termos()

    def op_un(self):
        if self.tokens[0].value in ("+", "-"):
            self.tokens.pop(0)

    def outros_termos(self):
        if self.tokens[0].value in ("+", "-"):
            self.op_ad()
            self.termo()
            self.outros_termos()

    def op_ad(self):
        if self.tokens.pop(0).value not in ("+", "-"):
            exit("Erro23: esperava um operador de mais ou menos")

    def termo(self):
        self.op_un()
        self.fator()
        self.mais_fatores()

    def mais_fatores(self):
        if self.tokens[0].value in ("*", "/"):
            self.op_mul()
            self.fator()
            self.mais_fatores()

    def op_mul(self):
        if self.tokens.pop(0).value not in ("*", "/"):
            exit("Erro24: esperava um operador * ou  /")

    def fator(self):
        if self.tokens[0].type not in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            exit("Erro25: esperava um identificador")
        else:
            if self.tokens[0].type in ("Identificador numérico inteiro", "Identificador numérico real"):
                inserir_TS(self.tokens[0], cat)
            if self.tokens.pop(0).value == "(":
                self.expressao()
                if self.tokens.pop(0).value != ")":
                    print("Erro26")
                    exit()










