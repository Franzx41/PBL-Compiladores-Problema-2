class TabelaIdentificadores():
    def __init__(self, nome, tipo, valor=None, tipoRetorno=None, parametros=None, tamanho=0):
        self.nome = nome
        self.tipo = tipo
        self.valor = valor
        self.tipoRetorno = tipoRetorno
        self.parametros = parametros
        self.tamanho = tamanho
    
    def __repr__(self):
        pass

class TabelaPares():
    def __init__(self):
         self.tabela = []
         
    def adicionarPar(self, pai, tabelaIdentificadores):
        novoPar = {
            "pai": pai,
            "tabela": tabelaIdentificadores 
        }
        
        self.tabela.append(novoPar)
    
    def __repr__(self):
            pass
        