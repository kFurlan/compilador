from copy import deepcopy
from operator import itemgetter

tabela_TS = {"global": {}} #lista de lista da tabela de símbolos
lista_token = [] #lista dos tokens lidos
cat = ""
contador = 0    #contador da tabela escopo global
contador_p = 0  #contador das tabelas escopos locais
list_variaveis = [] #guarda todas as variáveis lidas e depois insere na tabela
list_arg = []
Tresult = None
escopo = "global"
TipoIdent = None
Tipo_aux = None
nomeProcedure = None

def verificaDeclaracao(cadeia):
    variavelDeclarada = busca(cadeia) #primeiro busca por escopo local
    variavelDeclaradaGlobal = buscaPorEscopo(cadeia, "global")  #busca por escopo global
    if variavelDeclarada:
        linhaTabela = obterLinhaTabela(cadeia)  #primeiro verifica no escopo local
        if not (linhaTabela[1] == "var" or linhaTabela[1] == "param"):  #posição 1 que possui a cat
            exit("{} não é uma variável".format(cadeia))
    elif variavelDeclaradaGlobal:
        linhaTabela = obterLinhaTabelaPorEscopo(cadeia, "global") #depois verifica no escopo global
        if not (linhaTabela[1] == "var" or linhaTabela[1] == "param"):
            print(linhaTabela[1])
            exit("{} não é uma variável".format(cadeia))

    else:   #senão tiver em nenhum escopop a variável não foi declarada
        exit("Identificador {} não declarado".format(cadeia))

def inserirTabela(cadeia, token, tipo, valor, cont):
    tabela_TS[escopo][cadeia] = [token, cat, tipo, valor, cont]

def erro(token, esperado):
    print("Erro de sintaxe: linha {} | esperado: {} | entrada: {}"
          "".format(token.ind,esperado, token.value))
    exit()

def novoEscopo():
    tabela_TS[escopo] = {}

def insereVariavelTabela(tipo):
    global contador
    global contador_p
    for variavel in list_variaveis:
        variavelDeclarada = busca(variavel.value)
        if variavelDeclarada:
            exit("Variável {} ja declarada!".format(variavel.value))
        if escopo == "global":
            inserirTabela(variavel.value, variavel.type, tipo.value,None, cont=contador)
            contador += 1
        else:
            inserirTabela(variavel.value, variavel.type, tipo.value, None, cont=contador_p)
            contador_p += 1
    list_variaveis.clear()  # esvazia lista depois q insere

def busca(cadeia):  #busca pela cadeia na tabela daquele escopo
    return cadeia in tabela_TS[escopo]

def buscaPorEscopo(cadeia,_escopo): #busca pela cadeia na tabela de escopo global
    return cadeia in tabela_TS[_escopo]

def obterLinhaTabela(cadeia):
    return tabela_TS[escopo][cadeia]

def obterLinhaTabelaPorEscopo(cadeia, _escopo):
    return tabela_TS[_escopo][cadeia]

def trocaTipo(tipo):
    global Tresult
    if Tresult != tipo:
        Tresult = "real"

class sintatico:
    def __init__(self, tokens):
         self.tokens = tokens

    def S(self):
        self.program()
        for linha in tabela_TS:
            print(linha, tabela_TS[linha])


    def program(self):
        if self.tokens.pop(0).value != "program":
            exit("Erro1: esperava program")
        if self.tokens.pop(0).type not in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            exit("Erro2: esperava um identificador")
        self.corpo()
        if self.tokens.pop(0).value != ".":
            exit("Erro3: esperava um ponto final")

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
        global Tresult
        global Tipo_aux
        global nomeProcedure
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
                for variavel in list_variaveis:
                    verificaDeclaracao(variavel.value)
                list_variaveis.clear()
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
                for variavel in list_variaveis:
                    verificaDeclaracao(variavel.value)
                list_variaveis.clear()
                if self.tokens.pop(0).value != ")":
                    exit("Erro")

        elif self.tokens[0].type in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            token = self.tokens.pop(0)

            variavelDeclarada = busca(token.value)
            variavelDeclaradaGlobal = buscaPorEscopo(token.value, "global")
            if variavelDeclarada:
                linhaTabela = obterLinhaTabela(token.value)
                if not (linhaTabela[1] != "var" or linhaTabela[1] != "param" or linhaTabela[1] != "proc"):
                    print(linhaTabela[1])
                    exit("{} não é uma variável".format(token.value))
            elif variavelDeclaradaGlobal:
                linhaTabela = obterLinhaTabelaPorEscopo(token.value, "global")
                if not (linhaTabela[1] != "var" or linhaTabela[1] != "param" or linhaTabela[1] != "proc"):
                    print(linhaTabela[1])
                    exit("{} não é uma variável".format(token.value))

            else:
                exit("Identificador {} não declarado".format(token.value))

            Tresult = obterLinhaTabela(token.value)[2] if busca(token.value) else obterLinhaTabelaPorEscopo(token.value, "global")[2]
            Tipo_aux = deepcopy(Tresult)
            nomeProcedure = token.value

            self.restoIdent()

        else:
            exit("Erro10")


    def dc_v(self):
        if self.tokens.pop(0).value != "var":
            exit("Erro11: esperava um var")
        self.variaveis()
        if self.tokens.pop(0).value != ":":
            exit("Erro12: esperava um :")
        tipo = self.tipo_var()
        insereVariavelTabela(tipo)



    def dc_p(self):
        global contador
        global escopo
        global cat
        token = self.tokens.pop(0)
        if token.value != "procedure":
            exit("Erro13: esperava um procedure")
        token = self.tokens.pop(0)
        if token.type not in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            exit("Erro14: esperava um identificador")
        inserirTabela(token.value, token.type,None, None, cont=contador)
        escopo = token.value
        novoEscopo()    #quando se tem um procedure um novo escopo é criado com nome da procedure
        self.parametros()
        cat = "var"
        self.corpo_p()

    def mais_dc(self):
        if self.tokens[0].value == ";":
            self.tokens.pop(0)
            self.dc()


    def variaveis(self):
        token = self.tokens.pop(0)


        if token.type not in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            exit("Erro15: esperava um identificador")
        list_variaveis.append(token)
        self.mais_var()



    def mais_var(self):
        if self.tokens[0].value == ",":
            self.tokens.pop(0)
            self.variaveis()

    def restoIdent(self):
        if self.tokens[0].value == ":=":
            self.tokens.pop(0)
            self.expressao()
            if Tipo_aux != Tresult:
                exit("Tipo incompatível. Esperava {} e recebeu {}".format(Tipo_aux, Tresult))
        else:
            self.list_arg()
            tabelaProc = tabela_TS[nomeProcedure]
            parametros = sorted([tabelaProc[p] for p in tabelaProc if tabelaProc[p][1] == "param"],key = itemgetter(-1))
            if len(parametros) != len(list_arg):
                exit("Erro de número nos parâmetros")

            for i in range(len(parametros)):
                arg = obterLinhaTabela(list_arg[i].value)
                if parametros[i][2] != arg[2]:
                    exit("Erro de tipo ou ordem nos parâmetros")

            list_arg.clear()


    def condicao(self):
        self.expressao()
        self.relacao()
        self.expressao()

    def tipo_var(self):
        token = self.tokens.pop(0)
        if token.value not in ("real", "integer"):
            exit("Erro16: esperava um tipo real ou integer")
        return token


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
        tipo = self.tipo_var()
        insereVariavelTabela(tipo)
        self.mais_par()

    def mais_par(self):
        if self.tokens[0].value == ";":
            self.tokens.pop(0)
            self.lista_par()

    def corpo_p(self):
        global contador_p
        global escopo
        contador_p = 0

        self.dc_loc()

        global cat
        cat = "var"
        if self.tokens.pop(0).value != "begin":
            exit("Erro18: esperava um begin")
        self.comandos()
        escopo = "global"
        if self.tokens.pop(0).value != "end":
            exit("Erro19: esperava um end")

    def dc_loc(self):
        if self.tokens[0].value == "var":
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
        token = self.tokens.pop(0)
        if token.type not in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            exit("Erro21: esperava um identificador")
        list_arg.append(token)
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
        global contador
        global contador_p
        if self.tokens[0].type in ("Identificador", "Identificador numérico inteiro", "Identificador numérico real"):
            token = self.tokens.pop(0)
            if token.type in ("Identificador"):
                verificaDeclaracao(token.value)

            if token.type in ("Identificador numérico inteiro", "Identificador numérico real"):
                inserirTabela(token.value, token.type, None, token.value, cont=contador if escopo == "global" else contador_p)
                contador += 1
            Tresult_aux = obterLinhaTabela(token.value)[2] if busca(token.value) else obterLinhaTabelaPorEscopo(token.value, "global")[2]
            trocaTipo(Tresult_aux)

        elif self.tokens.pop(0).value == "(":
            self.expressao()
            if self.tokens.pop(0).value != ")":
                 exit("erro")











