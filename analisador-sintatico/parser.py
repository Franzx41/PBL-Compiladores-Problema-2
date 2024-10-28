class Parser():
    def __init__(self, token_list):
        self.token_list = token_list
        self.error_list = []
        self.index = 0

    # Função match para verificar categoria
    def match_category(self, expected_token_category):
        current_token = self.lookahead()
        if current_token['category'] != None and current_token['category'] in expected_token_category:
            self.index += 1 # Move to the next token
            return current_token
        else:
            self.error_list.append({"position":current_token["line"], "expected":expected_token_category, "received":current_token["category"]})
            
    # Função match para verificar o lexema
    def match_lexeme(self, expected_token_lexeme):
        current_token = self.lookahead()
        if current_token['lexeme'] != None and current_token['lexeme'] in expected_token_lexeme:
            self.index += 1 # Move to the next token
            return current_token
        else:
            self.error_list.append({"position":current_token["line"], "expected":expected_token_lexeme, "received":current_token["lexeme"]})
    
    # Acessa o token atual ou examina os proximos
    def lookahead(self, K = 0):
        if self.index + K < len(self.token_list):
            return self.token_list[self.index + K]
        return {"lexeme": None,"category": None,"line": None}
    
    # Executa o algorítimo
    def run(self):
        self.start()

        if self.index < len(self.token_list):
            self.error_list.append({"position":"Parsing Erro", "expected":"No tokens", "received":"Remaining tokens"})

        return len(self.error_list) == 0
    
    ### Produções ###
    def start(self):
        self.logic_expression()
    
    def logic_expression(self):
        current_token = self.lookahead()

        # Caso: '(' <logic expression> ')' ou '(' <logic expression> ')' <logic terminal> <logic expression>
        if current_token["lexeme"] == "(":
            self.match_lexeme(["("]) 
            self.logic_expression() 
            self.match_lexeme([")"]) 
            
            # Check for the optional <logic terminal> and further <logic expression>
            if self.lookahead()["lexeme"] in ['&&', '||']:
                self.logic_terminal() 
                self.logic_expression()

        # Caso: <logic value> ou <logic value> <logic terminal> <logic expression>
        else:
            self.logic_value()

            if self.lookahead()["lexeme"] in ['&&', '||']:
                self.logic_terminal()
                self.logic_expression()
                            
    def logic_value(self):
        current_token = self.lookahead()
        
        if current_token["lexeme"] in ['true', 'false']: 
            self.match_lexeme(['true', 'false'])
        else:
            self.relational_expression()  

    def logic_terminal(self):
        self.match_lexeme(['&&', '||']) 

    def relational_expression(self):
        current_token = self.lookahead()

        # Caso: '(' <relational expression> ')' ou '(' <relational expression> ')' <relational terminal> <relational expression>
        if current_token["lexeme"] == "(":
            self.match_lexeme(["("])
            self.relational_expression()
            self.match_lexeme([")"]) 
            
            # Verify <relational terminal> and further <relational expression>
            if self.lookahead()["lexeme"] in ['>', '<', '!=', '>=', '<=', '==']:
                self.relational_terminal()
                self.relational_expression()

        # Caso: <arithmetic expression> ou <arithmetic expression> <relational terminal> <relational expression>
        else:
            self.arithmetic_expression()
            
            if self.lookahead()["lexeme"] in ['>', '<', '!=', '>=', '<=', '==']:
                self.relational_terminal()
                self.relational_expression()

    def relational_terminal(self):
        self.match_lexeme(['>', '<', '!=', '>=', '<=', '=='])

    def arithmetic_expression(self):
        self.arithmetic_operating()
        if self.lookahead()["lexeme"] in ['+', '-']:
            self.arithmetic_sum()
    
    def arithmetic_operating(self):
        self.arithmetic_value()
        if self.lookahead()["lexeme"] in ['*', '/']:
            self.arithmetic_multiplication()

    def arithmetic_value(self):
        if self.lookahead()["category"] == "number":
            self.match_category("number")
        elif self.lookahead()["lexeme"] == "(":
            self.match_lexeme("(")
            self.arithmetic_expression()
            self.match_lexeme(")")
        elif self.lookahead()["category"] == "identifier":
            if self.lookahead(1)["category"] == "(":
                #self.function_call()
                pass
            else:
                #self.attribute
                pass

    def arithmetic_sum(self):
        self.match_lexeme(['+', '-'])
        self.arithmetic_operating()
        if self.lookahead()["lexeme"] in ['+', '-']:
            self.arithmetic_sum()
      
    def arithmetic_multiplication(self):
        self.match_lexeme(['*', '/'])
        self.arithmetic_value()
        if self.lookahead()["lexeme"] in ['*', '/']:
            self.arithmetic_multiplication()

    # <vector position>::= identifier <vector index>
    def vector_position(self):
        self.match_category(["identifier"])
        self.vector_index()

    # <vector index>::= 
    #         '[' number ']' 
    #       | '[' number ']' <vector index> 
    #       | '[' identifier ']' 
    #       | '[' identifier ']' <vector index> 
    #       | '[' <arithmetic expression>']' 
    #       | '[' <arithmetic expression>']' <vector index>
    def vector_index(self):
        self.match_lexeme(["["])

        # Caso: '[' number ']' ...
        if self.lookahead()["category"] == "number" and self.lookahead(1)["lexeme"] == "]":
            self.match_category("number")

        # Caso: Identifier
        elif self.lookahead()["category"] == "identifier" and self.lookahead(1)["lexeme"] == "]":
            self.match_category("identifier")

        # Caso: Arithmetic expression
        else:
            self.arithmetic_expression()

        self.match_lexeme(["]"])

        # Olha se o proximo token é [ e depois se é algo que caracterize <vector index> (parte opcional)
        if self.lookahead()["lexeme"] == "[" and (self.lookahead(1)["category"] in ["number", "identifier"] or self.lookahead(1)["lexeme"] == "("):
            self.vector_index()
            
    # <register position>::= identifier <register access>
    def register_position(self):
        self.match_category(["identifier"])
        self.register_access()
    
    # <register access>::= '.' identifier <register access> | ε
    def register_access(self):
        if self.lookahead()["lexeme"] == ".":
            self.match_lexeme(["."])
            self.match_category(["identifier"])
            self.register_access()

# Testando a classe
token_list = []
token_list.append({"lexeme": "(", "category": "OPEN_PARENTHESIS", "line": 1})
token_list.append({"lexeme": "2", "category": "number","line": 1})
token_list.append({"lexeme": ">", "category": "operator","line": 1})
token_list.append({"lexeme": "1", "category": "number","line": 1})
token_list.append({"lexeme": ")", "category": "CLOSE_PARENTHESIS", "line": 1})
token_list.append({"lexeme": "||", "category": "operator","line": 1})
token_list.append({"lexeme": "variavel", "category": "IDENTIFIER","line": 1})
token_list.append({"lexeme": "==", "category": "operator","line": 1})
token_list.append({"lexeme": "3", "category": "number","line": 1})

for item in token_list:
    print(item["lexeme"], end=" ")
print('')

p = Parser(token_list)

if p.run():
    print("Passou sem erros")
else:
    print("Falhou, erros:")
    for erro in p.error_list:
        print(erro)