
#region constants
DIGITS = "0123456789"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet = "abcdefghijklmnopqrstuvwxyz"
operators = "^*/%+-="
quotes = '"' + "'"

TTSTR = "STRING"
TTINT = "INT"
TTFLOAT = "FLOAT"
TTCOM = "COMMENT"
TTVAR = "VAR"
TTCRVAR = "CREATE VAR"
TTOP = "OPERATOR"
TTPRINT = "PRINT"
TTIF = "IF"
TTELIF = "ELIF"
TTELSE = "ELSE"
TTENDLINE = "END LINE"

VAR_VALUES = [TTSTR, TTINT, TTFLOAT]
#endregion

vars = []


class Var:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __repr__(self):
        return f'{self.value}'


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Type: {self.type} Value: {self.value}'


# making a list of tokens, for the executioner to recognize and work with
class Lexer:
    def __init__(self, text):
        self.code = text
        self.tokens = []
        self.analyze()

    def analyze(self):

        for line in self.code.split("\n"):
            type_ = ""
            str_out = ""
            str_token = ""

            #region comment
            if line[0] == "#" and type_ == "":
                type_ = TTCOM
            if type_ == TTCOM:
                type_ = ""
                continue
            #endregion

            for word in line.split():
                #region string
                # if still string
                if type_ == TTSTR:
                    str_out += word
                # starting string
                elif not type_ == TTSTR and word[0] in quotes:
                    type_ = TTSTR
                    str_token = word[0]
                    str_out += word[1:]
                # ending the string
                if type_ == TTSTR and word[len(word) - 1] == str_token and not str_out[len(str_out) - 5] == "/":
                    str_out = str_out[:len(str_out)-1]
                    str_token = ""
                    type_ = ""
                if type_ == TTSTR:
                    str_out += " "
                if not type_ == TTSTR and str_out != "":
                    self.tokens.append(Token(TTSTR, str_out))
                    str_out = ""
                    continue
                #endregion

                #region int
                if type_ == "" and word[0] in DIGITS:
                    type_ = TTINT
                if type_ == TTINT:
                    dec = 0
                    num_out = 0
                    for digit in word:
                        if digit == ".":
                            type_ = TTFLOAT
                            dec = 0.1
                        elif type_ == TTINT:
                            num_out *= 10
                            num_out += int(digit)

                        if type_ == TTFLOAT and digit != ".":
                            num_out += int(digit) * dec
                            dec /= 10
                    self.tokens.append(Token(type_, num_out))
                    type_ = ""
                    continue
                #endregion

                #region var
                if type_ == "" and word[0] == "$":
                    # if the var is in the memory
                    for v in vars:
                        if v.name == word[1:]:
                            type_ = TTVAR
                            self.tokens.append(Token(type_, v))
                    # if the var wasn't found in the memory
                    if type_ != TTVAR:
                        type_ = TTCRVAR
                        self.tokens.append(Token(type_, word[1:]))
                        type_ = ""
                #endregion

                #region operators
                if type_ == "" and len(word) == 1 and word in operators:
                    self.tokens.append(Token(TTOP, word))
                #endregion

                if type_ == "" and word == "print":
                    self.tokens.append(Token(TTPRINT))

            self.tokens.append(Token(TTENDLINE))
        print(self.tokens)

class Exp:
    def __init__(self, tokens, type_):
        self.type = type_
        self.tokens = tokens

class Executioner:
    def __init__(self, tokens):
        self.tokens = tokens
        self.execute()

    def expression(self, token_array):
        todo = []
        for t in token_array:
            if t.type == TTVAR:
                todo.append(self.find_var(t.value).value)
            else:
                todo.append(t)

        for t in todo:
            # if the symbol is before in the order of actions in math
            if t.type == TTOP and (type(todo[todo.index(t)-1]) is not Token or operators.index(todo[todo.index(t)-1].value) <= operators.index(t.value)):
                todo[todo.index(t)-1:todo.index(t)+2] = Exp([todo[todo.index(t)-1], todo[todo.index(t)+1]], t.value)
            elif t.type == TTOP:
                todo[todo.index(t):todo.index(t)+2] = Exp([todo[todo.index(t)-1], todo[todo.index(t)+1]], t.value)
                todo[todo.index(t)-1].tokens[1] = todo[todo.index(t)]

        calc_exp(todo)


    def calc_exp(self, todo):
        out = 0
        for t in todo.tokens:
            if type(t) == Exp:
                todo[todo.index(t)] = self.calc_exp(t)
                out = self.calc_exp(t)
            else:
                if t.type in operators:
                    if t.type == "^":
                        out = t.tokens[0].value ** t.tokens[1].value
                    elif t.type == "*":
                        out = t.tokens[0].value * t.tokens[1].value
                    elif t.type == "/":
                        out = t.tokens[0].value / t.tokens[1].value
                    elif t.type == "+":
                        out = t.tokens[0].value + t.tokens[1].value
                    elif t.type == "-":
                        out = t.tokens[0].value - t.tokens[1].value
        return out

    def find_var(self, search, is_value=False):
        for v in vars:
            if (not is_value and v.name == search) or (is_value and v.value == search):
                return v
        return None

    def execute(self):
        i = 0
        t = None

        while i < len(self.tokens):
            j = None
            for j in self.tokens[i:]:
                if j.type == TTENDLINE:
                    break
            endline = self.tokens.index(j)
            with t as self.tokens[i]:
                if t.type == TTCRVAR:
                    if self.tokens[i+1].value == "=":
                        vars.append(Var(t.value, self.expression(self.tokens[i+2:endline])))
                    elif self.tokens[i+1].type == TTENDLINE:
                        vars.append(Var(t.value))
                if t.type == TTPRINT:
                    print(str(self.expression(self.tokens[i+1:endline])))
            i = endline




def comp(code):
    exec = Executioner(Lexer(code).tokens)

while True:
    text = input("whale >> ")
    comp(text)
