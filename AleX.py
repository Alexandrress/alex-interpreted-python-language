"""

AleX interpreted language - Made by LEVEQUE Alexandre

"""

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
	com = 0
	var = ""
	expr = ""
	n = ""
	filecontents = list(filecontents)
	for char in filecontents:
		token += char
		if token == "~" :
			if com == 1 :
				com = 0
			else :
				com = 1
			token=""
		if com == 1 :
			token=""
		else :
			if token == " ":
				if state==0:
					token=""
					if varStarted==1: #You can't have space in VAR
						tokens.append("VAR:" + var)
						var = ""
						varStarted=0
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
			elif token == "<" and state == 0:
				if expr != "" and isexpr == 0:
					tokens.append("NUM:" + expr)
					expr = ""
				if var != "":
					tokens.append("VAR:" + var)
					var = ""
					varStarted=0
				else:
					tokens.append("<")
				token=""
			elif token == ">" and state == 0:
				if expr != "" and isexpr == 0:
					tokens.append("NUM:" + expr)
					expr = ""
				if var != "":
					tokens.append("VAR:" + var)
					var = ""
					varStarted=0
				else:
					tokens.append(">")
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
			elif token.upper() == "WHILE":
				tokens.append("WHILE")
				token = ""
			elif token.upper() == "ENDWHILE":
				tokens.append("ENDWHILE")
				token = ""
			elif token.upper() == "<":
				tokens.append("<")
				token = ""
			elif token.upper() == ">":
				tokens.append(">")
				token = ""
			elif token.upper() == "THEN":
				if expr != "" and isexpr == 0:
					tokens.append("NUM:" + expr)
					expr = ""
				if expr != "" and isexpr == 1:
					tokens.append("EXPR:" + expr)
					expr = ""
					isexpr = 0
				if var != "" and varStarted==1:
					tokens.append("VAR:" + var)
					var = ""
					varStarted=0
				tokens.append("THEN")
				token = ""
			elif token>="0" and token<="9﻿" and state!=1:
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
		if(toPRINT == "\\n"):
			toPRINT=""
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
	ir = 0
	cond = 0
	while(i < len(tok)):
		if tok[i] == "ENDIF" :
			if cond!=0:
				cond -= 1
			i+=1
		elif tok[i] == "ENDWHILE" :	
			if ir!=0:
				i = ir
			else :
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
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF NUM EQEQ NUM THEN" :
			if tok[i+1][4:] == tok[i+3][4:]:
				cond = cond
			else:
				cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF NUM EQEQ VAR THEN" : #considering VAR comes from INPUT
			VAR=(getVAR(tok[i+3])) #Get the VAR Value NUM
			if tok[i+1][4:] == VAR[8:-1]:
					cond = cond
			else :
					cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF VAR EQEQ NUM THEN" : #considering VAR comes from INPUT
			VAR=(getVAR(tok[i+1])) #Get the VAR Value NUM
			if tok[i+3][4:] == VAR[8:-1]:
					cond = cond
			else :
					cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF VAR EQEQ VAR THEN" : #considering VAR comes from INPUT
			VAR=(getVAR(tok[i+3])) #Get the VAR Value NUM
			VAR2=(getVAR(tok[i+1]))
			if VAR2[4:] == VAR[8:-1]:
					cond = cond
			else :
					cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF NUM < NUM THEN" :
			tok4=int(tok[i+1][4:])
			tok5=int(tok[i+3][4:])
			if tok4 < tok5:
				cond = cond
			else:
				cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF NUM < VAR THEN" : #considering VAR comes from INPUT
			VAR=(getVAR(tok[i+3])) #Get the VAR Value NUM
			VAR=int(VAR[8:-1])
			tok2=int(tok[i+1][4:])
			if tok2 < VAR :
					cond = cond
			else :
					cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF VAR < NUM THEN" : #considering VAR comes from INPUT
			VAR=(getVAR(tok[i+1])) #Get the VAR Value NUM
			VAR=int(VAR[8:-1])
			tok3=int(tok[i+3][4:])
			if VAR < tok3:
					cond = cond
			else :
					cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF VAR < VAR THEN" : #considering VAR comes from INPUT
			VAR=(getVAR(tok[i+3])) #Get the VAR Value NUM
			VAR2=(getVAR(tok[i+1]))
			VAR=int(VAR[8:-1])
			VAR2=int(VAR2[4:])
			if VAR2 < VAR:
					cond = cond
			else :
					cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF NUM > NUM THEN" :
			tok6=int(tok[i+1][4:])
			tok7=int(tok[i+3][4:])
			if tok6 > tok7:
				cond = cond
			else:
				cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF NUM > VAR THEN" : #considering VAR comes from INPUT
			VAR=(getVAR(tok[i+3])) #Get the VAR Value NUM
			VAR=int(VAR[8:-1])
			tok8=int(tok[i+1][4:])
			if tok8 > VAR:
					cond = cond
			else :
					cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF VAR > NUM THEN" : #considering VAR comes from INPUT
			VAR=(getVAR(tok[i+1])) #Get the VAR Value NUM
			VAR=int(VAR[8:-1])
			tok1=int(tok[i+3][4:])
			if VAR > tok1 :
					cond = cond
			else :
					cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF VAR > VAR THEN" : #considering VAR comes from INPUT
			VAR=(getVAR(tok[i+3])) #Get the VAR Value INPUT
			VAR2=(getVAR(tok[i+1])) #NOT INPUT
			VAR=int(VAR[8:-1])
			VAR2=int(VAR2[4:])
			if VAR2 > VAR:
					cond = cond
			else :
					cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "WHILE VAR EQEQ NUM THEN" : #considering VAR not INPUT
			VAR=(getVAR(tok[i+1])) #Get the VAR Value NUM
			tok9=int(tok[i+3][4:])
			VAR=int(VAR[4:])
			if tok9 == VAR :
				ir = i
			else :
				ir = 0
			i+=5



def run():
	code = open_file(argv[1])
	if code == 0:
		print("FileNotRecognizedError: [Errno 1] can only open *.AleX files.")
		return(0)
	tok = lex(code)
	parse (tok)

run()
