
#define variables
tokens = []
vars = []

# change this after
_code = "var x = 5;\nxgg print 'hello world ' + x;"

def tokeIt(code):
	var = 0
	end = False
	string = ''
	isString = False
	code = code.split()
	num = 0
	for num in range(len(code)):
		if var == 2:
			var = 0
			tokens.append(';')
			continue
		if var > 0:
			var +=1
			continue
		if code[num][len(code[num]) - 1] == ';':
			end = True
			code[num] = code[num][:len(code[num])-1]
		if isString == True:
			if code[num][len(code[num]) - 1] == "'" or code[num][len(code[num]) - 1] == '"':
				code[num] = code[num][:len(code[num])-1]
				string = string + ' ' + code[num]
				tokens.append(['string:', string])
				isString = False
			else:
				string = string + ' ' + code[num]
		else:
			if code[num] == 'var':
				continue
			elif code[num] == 'print':
				tokens.append('print')
			elif code[num][0] == "'" or code[num][0] == '"':
				code[num] = code[num][1:]
				string = code[num]
				isString = True
			elif code[num-1] == 'var' and code[num+1] == '=':
				tokens.append('var')
				tokens.append(code[num])
				tokens.append(code[num+2][:len(code[num+2])-1])
				var = 1
			 #keep doing this about other keywords
			 
			else:
				tokens.append(code[num])
		if end:
			tokens.append(';')
			end = False
	return tokens

def varsComp(tokens, vars):
	isVar = 0
	for num in range(len(tokens)):
		if isVar > 0:
			vars.append(tokens[num])
			if isVar == 1:
				for x in range(len(vars)):
					if vars[x] == tokens[num] and not tokens[num - 1] == 'var':
						tokens[num] = vars[x]
						print('var declaration')
					print(tokens[num])
			if isVar == 2:
				isVar = 0
				vars.append(';')
				continue
			else:
				isVar +=1
			num += 1
		else:
			if tokens[num] == 'var':
				isVar = 1
				continue
	return vars

def comp(tokens):
	tokens = tokeIt(_code)
	print(tokens)
	print(varsComp(tokens, vars))

#start the script
comp(tokens)
