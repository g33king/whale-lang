
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
			if code[num] == 'print':
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
			 #להמשיך אותו דבר עם מילים אחרות
			 
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
			vars.append([tokens[num], tokens[num+1]])
			if isVar == 1:
				for x in range(len(tokens)):
					if vars[x][0] == tokens[num]:
						tokens[num] = vars[x][0]
			if isVar ==2:
				isVar == 0
				continue
			else:
				isVar +=1
			num += 1
		else:
			if tokens[num] == 'var':
				isVar = 1
				continue
	return [vars, tokens]
	
def comp(gg):
	print(varsComp(gg, vars))

#start the script
tokens = tokeIt(_code)
print(tokens)
comp(tokens)