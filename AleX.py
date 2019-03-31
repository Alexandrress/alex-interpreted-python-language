from sys import *
import fnmatch

tokens=[]
symbols = {}

def open_file(filename):
	if fnmatch.fnmatch(filename,'*.AleX'):
		data = open(filename, "r").read()
		data += "\n"
		return data
	else :
		return 0

def lex(filecontents):
	token=""
	string=""
	state = 0
	isexpr = 0
	varStarted = 0
	var = ""
	expr = ""
	n = ""
	filecontents = list(filecontents)
	for char in filecontents:
		token += char
		if token == " ":
			if state==0:
				token=""
			else:
				token=" "
		elif token == "\n" or token == "<EOF>":
			if expr != "" and isexpr == 1:
				tokens.append("EXPR:" + expr)
				expr = ""
				isexpr = 0
			elif expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			elif var != "":
				tokens.append("VAR:" + var)
				var = ""
				varStarted=0
			token = ""
		elif token == "=" and state == 0:
			if expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			if var != "":
				tokens.append("VAR:" + var)
				var = ""
				varStarted=0
			if  tokens[-1] == "EQUALS":
				tokens[-1]=("EQEQ")
			else:
				tokens.append("EQUALS")
			token=""
		elif token == "|" and state == 0:
			varStarted = 1
			var += token
			token = ""
		elif varStarted == 1:
			if token == "<" or token == ">":
				if var != "":
					tokens.append("VAR:" + var)
					var = ""
					varStarted=0
			var += token
			token = ""
		elif token.upper() == "PRINT":
			tokens.append("PRINT")
			token = ""
		elif token.upper() == "INPUT":
			tokens.append("INPUT")
			token = ""
		elif token.upper() == "ENDIF":
			tokens.append("ENDIF")
			token = ""
		elif token.upper() == "IF":
			tokens.append("IF")
			token = ""
		elif token.upper() == "THEN":
			if expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			if expr != "" and isexpr == 1:
				tokens.append("EXPR:" + expr)
				expr = ""
				isexpr = 0
			tokens.append("THEN")
			token = ""
		elif token>="0" and token<="9﻿" :
			expr += token
			token = ""
		elif token in ["+","-","*","/","(",")","%"]:
			isexpr = 1
			expr += token
			token = ""
		elif token == "\t" :
			token=""
		elif token == "\"" or token == " \"":
			if state == 0:
				state = 1
			elif state ==1:
				tokens.append("STRING:" + string + "\"")
				string = ""
				state = 0
				token = ""
		elif state == 1:
			string += token
			token = ""
	return tokens
	
def evalExpression(expr):
	return (eval(expr, {'__builtins__':{}}))

def doPRINT(toPRINT):
	if(toPRINT[0:6] == "STRING"):
		toPRINT= toPRINT[8:-1]
	elif(toPRINT[0:3] == "NUM"):
		toPRINT= toPRINT[4:]
	elif(toPRINT[0:4] == "EXPR"):
		toPRINT= evalExpression(toPRINT[5:])
	print(toPRINT)
	
def doASSIGN(varname, varvalue):
	symbols[varname[4:]] = varvalue
	
def getVAR(varvalue):
	varvalue=varvalue[4:]
	if varvalue in symbols:
		return(symbols[varvalue])
	else :
		print("VariableNotDefinedError: [Errno 3] undefined variable.")
		exit()

def getINPUT(string, varname):
	i = input(string[1:-1] + " ")
	symbols[varname] = "STRING:\"" + i + "\""

def parse(tok):
	i = 0
	cond = 0
	while(i < len(tok)):
		if tok[i] == "ENDIF":
			cond -= 1
			i+=1
		elif (tok[i] + " " + tok[i+1][0:6] == "PRINT STRING" or tok[i] + " " + tok[i+1][0:3] == "PRINT NUM" or tok[i] + " " + tok[i+1][0:4] == "PRINT EXPR" or tok[i] + " " + tok[i+1][0:3] == "PRINT VAR") :
			if cond == 0 :
				if tok[i+1][0:6] == "STRING" :
					doPRINT(tok[i+1])
				elif tok[i+1][0:3] == "NUM":
					doPRINT(tok[i+1])
				elif tok[i+1][0:4] == "EXPR":
					doPRINT(tok[i+1])	
				elif tok[i+1][0:3] == "VAR":
					doPRINT(getVAR(tok[i+1]))	
				i+=2
			else :
				i+=2
		elif (tok[i][0:3] + " " + tok[i+1] + " " + tok[i+2][0:6] == "VAR EQUALS STRING" or tok[i][0:3] + " " + tok[i+1] + " " + tok[i+2][0:3] == "VAR EQUALS NUM" or tok[i][0:3] + " " + tok[i+1] + " " + tok[i+2][0:4] == "VAR EQUALS EXPR" or tok[i][0:3] + " " + tok[i+1] + " " + tok[i+2][0:3] == "VAR EQUALS VAR") :
			if cond == 0 :
				if tok[i+2][0:6] == "STRING" :
					doASSIGN(tok[i],tok[i+2])
				elif tok[i+2][0:3] == "NUM":
					doASSIGN(tok[i],tok[i+2])
				elif tok[i+2][0:4] == "EXPR":
					doASSIGN(tok[i],"NUM:" + str(evalExpression(tok[i+2][5:])))
				elif tok[i+2][0:3] == "VAR":
					doASSIGN(tok[i],getVAR(tok[i+2]))
				i+=3
			else :
				i+=3
		elif tok[i] + " " + tok[i+1][0:6] + " " + tok[i+2][0:3] == "INPUT STRING VAR" and cond == 0 :
			if cond == 0 :
				getINPUT(tok[i+1][7:],tok[i+2][4:])
				i+=3
			else :
				i+=3
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF NUM EQEQ NUM THEN":
			if tok[i+1][4:] == tok[i+3][4:]:
				cond = cond
			else:
				cond += 1
			i+=5


def run():
	code = open_file(argv[1])
	if code == 0:
		print("FileNotRecognizedError: [Errno 1] can only open *.AleX files.")
		return(0)
	tok = lex(code)
	parse (tok)

run()
