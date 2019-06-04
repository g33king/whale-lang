
DIGITS = "0123456789"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet = "abcdefghijklmnopqrstuvwxyz"

class Token:
    def __init__(self, type_, value=None, posStart=None, posEnd=None):
        self.type = type_
        self.value = value
        self.posStart = posStart
        self.posEnd = posEnd
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

class TokenType:
    def __init__(self,type_):
        self.type = type_
    def __repr__(self):
        return f'{self.type}'

class Var:
    def __init__(self, name, type_, value=None):
        self.name = name
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'{self.value}'

class ErrorClass:
    def __init__(self, error_detailes, pos_start, pos_end):
        self.error_detailes = error_detailes
        self.pos_start = pos_start
        self.pos_end = pos_end
    
    def __repr__():
        return f'ERROR: {self.error_detailes} from: {self.pos_start} to: {self.pos_end)'

TTKeyWord = TokenType("KeyWord")
TTIdentifier = TokenType("Identifier")
TTEq = TokenType("EQ")
TTPlus = TokenType("Plus")
TTMinus = TokenType("Minus")
TTMul = TokenType("Multiply")
TTDiv = TokenType("Divide")
TTLparen = TokenType("(")
TTRparen = TokenType(")")
TTInt = TokenType("Int")
TTFloat = TokenType("Float")
TTStr = TokenType("String")
TTVarCall = TokenType("Called Var")
TTVarDec = TokenType("Declerated Var")

VTypes = [
    "String",
    "Int",
    "Float",
    "Boolean"
]

class Lexer:
    def __init__(self, text):
        self.pos = -1
        self.text = text
        self.current_char = None
        self.advance()
        self.vars = []
    
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t': self.advance()
            if self.current_char == '+':
                tokens.append(Token(TTPlus, None, self.pos, self.pos))
                self.advance()
            if self.current_char == '-':
                tokens.append(Token(TTMinus, None, self.pos, self.pos))
                self.advance()
            if self.current_char == '*':
                tokens.append(Token(TTMul, None, self.pos, self.pos))
                self.advance()
            if self.current_char == '/':
                tokens.append(Token(TTDiv, None, self.pos, self.pos))
                self.advance()
            if self.current_char == '(':
                tokens.append(Token(TTLparen, None, self.pos, self.pos))
                self.advance()
            if self.current_char == ')':
                tokens.append(Token(TTRparen, None, self.pos, self.pos))
                self.advance()
            if self.current_char != None and self.current_char in DIGITS:
                isFloat, num = make_num
                if isFloat: tokens.append(Token(TTFloat, float(num)))
                else: tokens.append(Token(TTInt, int(num)))
            if self.current_char != None and self.current_char in "'" + '"':
                tokens.append(Token(TTStr, self.make_str)
            if self.current_char == '&':
                tokens.append(self.call_var)
            if self.current_char + self.text[self.pos+1] + self.text[self.pos+2] == 'var':
                tokens.append()
        return tokens
    
    def make_num(self):
        num_str = ''
        Float = False
        pos_start = self.pos
        while self.current_char != None and self.current_char in DIGITS + '.' and self.pos < len(self.text):
            if self.current_char == '.': Float = True
            num_str += self.current_char
            self.advance()
        pos_end = self.pos
        return Float, num_str
    
    def make_str(self):
        str_str = ''
        self.advance()
        pos_start = self.pos
        while self.current_char != None and not self.current_char in '"' + "'" and self.pos < len(self.text):
            str_str += self.current_char
            self.advance()
        pos_end = self.pos
        self.advance()
        return str_str
    
    def call_var(self):
        pos_start = self.pos
        self.advance() # because of the $
        var_name = ''
        while self.current_char != None and self.current_char in ALPHABET + alphabet + '_-' + DIGITS and self.pos < len(self.text):
            var_name += self.current_char
            self.advance()
        pos_end = self.pos
        self.advance()
        for t in len(self.vars):
            if var_name == self.vars[t].name:
                var_type = self.vars[t].type_
                return Token(TTVarCall, f'{var_type} {var_name}', pos_start, pos_end)
    
    def declerate_var(self):
        pos_start = self.pos
        var_type = ''
        var_name = ''
        var_value = ''
        for num in range(4): 
            self.advance() # advance after var(
        while self.current_char != None and self.current_char != ')':
            var_type += self.current_char
            self.advance()
        if var_type in VTypes:
            self.advance() # advance after )
            while self.current_char != None and self.current_char in DIGITS + ALPHABET + alphabet + '_-':
                var_name += self.current_char
                self.advance()
            if var_name in self.vars: print(Error(f'There is already var named {var_name}', pos_start, self.pos))
            else:
                if self.current_char == ';':
                    self.vars.append(Var(var_name, var_type))
                    break
                elif self.current_char == '=':
                    self.advance()
                    if self.current_char != None and self.current_char in DIGITS:
                        isFloat, number = self.make_num()
                        if isFloat and var_type == 'Float':
                            var_value = float(number)
                        elif not isFloat and var_type == 'Int': var_value = int(number)
                        else: print(ErrorClass("The type you wrote and the value doesnt match each other", pos_start, self.pos))
                    elif self.current_char != None and self.current_char in '"' + "'": var_value = self.make_str()
                    else: print(ErrorClass("You need to tell what is the value or to remove the equals sign", pos_start, self.pos))
        else: print(ErrorClass(f'There isnt var type as {var_type}', pos_start, self.pos))

def compile(code):
    lex = Lexer(code)
    print(lex.make_tokens())

while True:
    text = input("whale >> ")
    compile(text)