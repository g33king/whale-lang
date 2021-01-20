# region constants
DIGITS = "0123456789"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet = "abcdefghijklmnopqrstuvwxyz"
operators = "^*/%+-"
quotes = '"' + "'"

TTSTR = "STRING"
TTINT = "INT"
TTFLOAT = "FLOAT"
TTBOOL = "BOOL"
TTVAR = "VAR"
TTCRVAR = "CREATE VAR"
TTCOM = "COMMENT"
TTOP = "OPERATOR"
TTBOOLOP = "BOOL OP"
TTPRINT = "PRINT"
TTIF = "IF"
TTELIF = "ELIF"
TTELSE = "ELSE"
TTENDLINE = "END LINE"

VAR_VALUES = [TTSTR, TTINT, TTFLOAT]
# endregion

vars = []


def get_type(value):
    if str(value)[0] in DIGITS + "-":
        for digit in str(value):
            if digit == '.':
                return TTFLOAT
        return TTINT
    elif str(value) in ["True", "False"]:
        return TTBOOL
    else:
        return TTSTR


class Var:
    def __init__(self, name, value=None, type_=None):
        self.name = name
        self.value = value
        self.type = type_
        if type_ is None and value is not None:
            self.type = get_type(self.value)

    def __repr__(self):
        return f'{self.value}'


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Type: {self.type} Value: {self.value}'


# expression, and can calculate itself
class Exp:
    def __init__(self, tokens, type_):
        self.type = type_
        self.tokens = tokens

    def calc(self):
        if self.type == "^":
            return self.tokens[0].value ** self.tokens[1].value
        elif self.type == "*":
            return self.tokens[0].value * self.tokens[1].value
        elif self.type == "/":
            return self.tokens[0].value / self.tokens[1].value
        elif self.type == "+":
            return self.tokens[0].value + self.tokens[1].value
        elif self.type == "-":
            return self.tokens[0].value - self.tokens[1].value


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

            # region comment
            if line[0] == "#" and type_ == "":
                type_ = TTCOM
            if type_ == TTCOM:
                type_ = ""
                continue
            # endregion

            for word in line.split():
                # region string
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
                    str_out = str_out[:len(str_out) - 1]
                    str_token = ""
                    type_ = ""
                if type_ == TTSTR:
                    str_out += " "
                if not type_ == TTSTR and str_out != "":
                    self.tokens.append(Token(TTSTR, str_out))
                    str_out = ""
                    continue
                # endregion

                # region int
                if type_ == "" and word[0] in DIGITS + "-":
                    type_ = TTINT
                if type_ == TTINT:
                    dec = 0
                    num_out = 0
                    for digit in word:
                        if digit == ".":
                            type_ = TTFLOAT
                            dec = 0.1
                        elif digit == "-":
                            continue
                        elif type_ == TTINT:
                            num_out *= 10
                            num_out += int(digit)

                        if type_ == TTFLOAT and digit != ".":
                            num_out += int(digit) * dec
                            dec /= 10
                    if word[0] == "-":
                        num_out *= -1
                    self.tokens.append(Token(type_, num_out))
                    type_ = ""
                    continue
                # endregion

                # region var
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
                    type_ = ""
                # endregion

                # region operators
                if type_ == "" and ((len(word) == 1 and word in operators + '=') or (len(word) == 2 and word[1] == '=' and word[0] in operators)):
                    self.tokens.append(Token(TTOP, word))
                # endregion

                # region bool operators
                if type_ == "" and len(word) == 2 and word[1] == "=" and not word[0] in operators:
                    self.tokens.append(Token(TTBOOLOP, word))
                #endregion

                # region saved words
                if type_ == "":
                    if word == "print":
                        self.tokens.append(Token(TTPRINT))
                    elif word == "if":
                        self.tokens.append(Token(TTIF))
                #endregion
            self.tokens.append(Token(TTENDLINE))
        print(self.tokens)

class Executioner:
    def __init__(self, tokens):
        self.tokens = tokens
        self.execute()

    def expression(self, token_array):
        todo = []
        for t in token_array:
            if t.type == TTVAR:
                var = self.find_var(t.value.name)
                if var is not None:
                    todo.append(Token(var.type, var.value))
                else:
                    print(f'Error! There is no var named {t.value}')
            else:
                todo.append(t)

        for op in operators:
            for t in todo:
                if t.type == TTOP and t.value == op:
                    operands = [todo[todo.index(t) - 1], todo[todo.index(t) + 1]]
                    del todo[todo.index(operands[0])+1:todo.index(operands[1])+1]
                    express = Exp(operands, op).calc()
                    todo[todo.index(operands[0])] = Token(get_type(express), express)
        return todo[0]

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

            for t in self.tokens[i:endline]:
                if t.type == TTCRVAR:
                    if self.tokens[i + 1].value == "=":
                        value = self.expression(self.tokens[i + 2:endline]).value
                        vars.append(Var(t.value, value, get_type(value)))
                    elif self.tokens[i + 1].type == TTENDLINE:
                        vars.append(Var(t.value))

                elif t.type == TTVAR:
                    if self.tokens[i+1].value == "=":
                        vars[vars.index(self.find_var(t.value.name))] = Var(t.value.name, self.expression(self.tokens[i+2:endline]).value, get_type(self.expression(self.tokens[i+2:endline]).value))
                    elif self.tokens[i+1].type == TTOP and len(self.tokens[i+1].value) == 2:
                        vars[vars.index(self.find_var(t.value.name))] = Var(t.value.name, Exp([vars[vars.index(self.find_var(t.value.name))], self.expression(self.tokens[i+2:endline])], self.tokens[i+1].value[0]).calc())

                elif t.type == TTPRINT:
                    print(self.expression(self.tokens[i + 1:endline]))
            i = endline + 1


def comp(code):
    exec = Executioner(Lexer(code).tokens)


while True:
    text = input("whale >>")
    comp(text)
