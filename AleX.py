"""

AleX interpreted language - Made by LEVEQUE Alexandre

"""

from sys import *
import fnmatch
import random
import pygame, random, sys
from pygame.locals import *

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
			elif token.upper() == "RAND":
				tokens.append("RAND")
				token = ""
			elif token.upper() == "SNAKE":
				tokens.append("SNAKE")
				token = ""
			elif token.upper() == "NPRINT":
				tokens.append("NPRINT")
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
			elif token.upper() == "CREDIT":
				tokens.append("CREDIT")
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
			elif token.upper() == "TO":
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
				tokens.append("TO")
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
	ir2 = 0
	cond = 0
	condw = 0
	while(i < len(tok)):
		if tok[i] == "ENDIF" :
			if cond!=0:
				cond -= 1
			i+=1
		elif tok[i] == "ENDWHILE" :	
			if ir!=0:
				ir2 = i
				i = ir
			if ir==0 :
				condw -= 1
				i+=1
		elif tok[i] == "CREDIT" :
			if cond == 0 and condw == 0 :
				print("   _____  .__                                    .___                .____     _______________   _______________________   ____ ______________")
				print("  /  _  \ |  |   ____ ___  ________    ____    __| _/______   ____   |    |    \_   _____/\   \ /   /\_   _____/\_____  \ |    |   \_   _____/")
				print(" /  /_\  \|  | _/ __ \\  \/  /\__  \  /    \  / __ |\_  __ \_/ __ \  |    |     |    __)_  \   Y   /  |    __)_  /  / \  \|    |   /|    __)_ ")
				print("/    |    \  |_\  ___/ >    <  / __ \|   |  \/ /_/ | |  | \/\  ___/  |    |___  |        \  \     /   |        \/   \_/.  \    |  / |        /")
				print("\____|__  /____/\___  >__/\_ \(____  /___|  /\____ | |__|    \___  > |_______ \/_______  /   \___/   /_______  /\_____\ \_/______/ /_______  /")
				print("        \/          \/      \/     \/     \/      \/             \/          \/        \/                    \/        \__>                \/ ")
			i+=1
		elif tok[i] == "NPRINT" :
			if cond == 0 and condw == 0 :
				print("\n")
			i+=1
		elif tok[i] == "SNAKE" :
			if cond == 0 and condw == 0 :
				def collide(x1, x2, y1, y2, w1, w2, h1, h2):
					if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:return True
					else:return False
				def die(screen, score):
					f=pygame.font.SysFont('Arial', 30);t=f.render('Your score was: '+str(score), True, (0, 0, 0));screen.blit(t, (10, 270));pygame.display.update();pygame.time.wait(2000);sys.exit(0)
				xs = [290, 290, 290, 290, 290];ys = [290, 270, 250, 230, 210];dirs = 0;score = 0;applepos = (random.randint(0, 590), random.randint(0, 590));pygame.init();s=pygame.display.set_mode((600, 600));pygame.display.set_caption('Snake');appleimage = pygame.Surface((10, 10));appleimage.fill((255, 0, 0));img = pygame.Surface((20, 20));img.fill((0, 255, 0));f = pygame.font.SysFont('Arial', 20);clock = pygame.time.Clock()
				while True:
					clock.tick(10)
					for e in pygame.event.get():
						if e.type == QUIT:
							sys.exit(0)
						elif e.type == KEYDOWN:
							if e.key == K_UP and dirs != 0:dirs = 2
							elif e.key == K_DOWN and dirs != 2:dirs = 0
							elif e.key == K_LEFT and dirs != 1:dirs = 3
							elif e.key == K_RIGHT and dirs != 3:dirs = 1
					i = len(xs)-1
					while i >= 2:
						if collide(xs[0], xs[i], ys[0], ys[i], 20, 20, 20, 20):die(s, score)
						i-= 1
					if collide(xs[0], applepos[0], ys[0], applepos[1], 20, 10, 20, 10):score+=1;xs.append(700);ys.append(700);applepos=(random.randint(0,590),random.randint(0,590))
					if xs[0] < 0 or xs[0] > 580 or ys[0] < 0 or ys[0] > 580: die(s, score)
					i = len(xs)-1
					while i >= 1:
						xs[i] = xs[i-1];ys[i] = ys[i-1];i -= 1
					if dirs==0:ys[0] += 20
					elif dirs==1:xs[0] += 20
					elif dirs==2:ys[0] -= 20
					elif dirs==3:xs[0] -= 20	
					s.fill((255, 255, 255))	
					for i in range(0, len(xs)):
						s.blit(img, (xs[i], ys[i]))
					s.blit(appleimage, applepos);t=f.render(str(score), True, (0, 0, 0));s.blit(t, (10, 10));pygame.display.update()
			i+=1
		elif tok[i][0:3] + " " + tok[i+1] + " " + tok[i+2][0:3] + " " + tok[i+3][0:4] == "VAR EQUALS VAR EXPR" : #considering VAR not INPUT
			if condw == 0 and cond == 0 :
				VAR1=getVAR(tok[i])
				VAR2=getVAR(tok[i+2])
				VAR1=int(VAR1[4:])
				VAR2=int(VAR2[4:])
				tok3=int(tok[i+3][5:])
				VAR1=VAR2+tok3
				VAR1=str(VAR1)
				doASSIGN(tok[i],"NUM:"+VAR1)
			i+=4
		elif (tok[i] + " " + tok[i+1][0:6] == "PRINT STRING" or tok[i] + " " + tok[i+1][0:3] == "PRINT NUM" or tok[i] + " " + tok[i+1][0:4] == "PRINT EXPR" or tok[i] + " " + tok[i+1][0:3] == "PRINT VAR") :
			if cond == 0 and condw == 0 :
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
			if cond == 0 and condw == 0:
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
			if cond == 0 and condw == 0 :
				getINPUT(tok[i+1][7:],tok[i+2][4:])
				i+=3
			else :
				i+=3
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF NUM EQEQ NUM THEN" :
			if condw == 0 :
				if tok[i+1][4:] == tok[i+3][4:]:
					cond = cond
				else:
					cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF NUM EQEQ VAR THEN" : #considering VAR comes from INPUT
			if condw == 0 :
				VAR=(getVAR(tok[i+3])) #Get the VAR Value NUM
				if tok[i+1][4:] == VAR[8:-1]:
						cond = cond
				else :
						cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF VAR EQEQ NUM THEN" : #considering VAR comes from INPUT
			if condw == 0 :
				VAR=(getVAR(tok[i+1])) #Get the VAR Value NUM
				if tok[i+3][4:] == VAR[8:-1] or tok[i+3][4:] == VAR[4:] :
						cond = cond
				else :
						cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF VAR EQEQ VAR THEN" : #considering VAR comes from INPUT
			if condw == 0 :
				VAR=(getVAR(tok[i+3])) #Get the VAR Value NUM
				VAR2=(getVAR(tok[i+1]))
				if VAR2[4:] == VAR[8:-1]:
						cond = cond
				else :
						cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF NUM < NUM THEN" :
			if condw == 0 :
				tok4=int(tok[i+1][4:])
				tok5=int(tok[i+3][4:])
				if tok4 < tok5:
					cond = cond
				else:
					cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF NUM < VAR THEN" : #considering VAR comes from INPUT
			if condw == 0 :
				VAR=(getVAR(tok[i+3])) #Get the VAR Value NUM
				VAR=int(VAR[8:-1])
				tok2=int(tok[i+1][4:])
				if tok2 < VAR :
						cond = cond
				else :
						cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF VAR < NUM THEN" : #considering VAR comes from INPUT
			if condw == 0 :
				VAR=(getVAR(tok[i+1])) #Get the VAR Value NUM
				VAR=int(VAR[8:-1])
				tok3=int(tok[i+3][4:])
				if VAR < tok3:
						cond = cond
				else :
						cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF VAR < VAR THEN" : #considering VAR comes from INPUT
			if condw == 0 :
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
			if condw == 0 :
				tok6=int(tok[i+1][4:])
				tok7=int(tok[i+3][4:])
				if tok6 > tok7:
					cond = cond
				else:
					cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF NUM > VAR THEN" : #considering VAR comes from INPUT
			if condw == 0 :
				VAR=(getVAR(tok[i+3])) #Get the VAR Value NUM
				VAR=int(VAR[8:-1])
				tok8=int(tok[i+1][4:])
				if tok8 > VAR:
						cond = cond
				else :
						cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF VAR > NUM THEN" : #considering VAR comes from INPUT
			if condw == 0 :
				VAR=(getVAR(tok[i+1])) #Get the VAR Value NUM
				VAR=int(VAR[8:-1])
				tok1=int(tok[i+3][4:])
				if VAR > tok1 :
						cond = cond
				else :
						cond += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "IF VAR > VAR THEN" : #considering VAR comes from INPUT
			if condw == 0 :
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
			if condw == 0 and cond == 0 :
				VAR=(getVAR(tok[i+1])) #Get the VAR Value NUM
				tok9=int(tok[i+3][4:])
				VAR=int(VAR[4:])
				if tok9 == VAR :
					ir = i
				else :
					if ir2!=0 :
						i=ir2-5
					ir = 0
					ir2 = 0
					condw += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "WHILE NUM EQEQ VAR THEN" : #considering VAR not INPUT
			if condw == 0 and cond == 0 :
				VAR=(getVAR(tok[i+3])) #Get the VAR Value NUM
				tok9=int(tok[i+1][4:])
				VAR=int(VAR[4:])
				if tok9 == VAR :
					ir = i
				else :
					if ir2!=0 :
						i=ir2-5
					ir = 0
					ir2 = 0
					condw += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "WHILE VAR EQEQ VAR THEN" : #considering VAR not INPUT
			if condw == 0 and cond == 0 :
				VAR=(getVAR(tok[i+1]))
				VAR2=(getVAR(tok[i+3])) #Get the VAR2 Value NUM
				if VAR2[4:] == VAR[8:-1] :
					ir = i
				else :
					if ir2!=0 :
						i=ir2-5
					ir = 0
					ir2 = 0
					condw += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "WHILE VAR > VAR THEN" : #considering VAR INPUT
			if condw == 0 and cond == 0 :
				VAR=(getVAR(tok[i+1]))
				VAR2=(getVAR(tok[i+3])) #Get the VAR2 Value NUM
				VAR=int(VAR[8:-1])
				VAR2=int(VAR2[4:])
				if VAR > VAR2 :
					ir = i
				else :
					if ir2!=0 :
						i=ir2-5
					ir = 0
					ir2 = 0
					condw += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "WHILE VAR < VAR THEN" : #considering VAR INPUT
			if condw == 0 and cond == 0 :
				VAR=(getVAR(tok[i+1]))
				VAR2=(getVAR(tok[i+3])) #Get the VAR2 Value NUM
				VAR=int(VAR[8:-1])
				VAR2=int(VAR2[4:])
				if VAR < VAR2 :
					ir = i
				else :
					if ir2!=0 :
						i=ir2-5
					ir = 0
					ir2 = 0
					condw += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "WHILE NUM < VAR THEN" : #considering VAR not INPUT
			if condw == 0 and cond == 0 :
				VAR=(getVAR(tok[i+3])) #Get the VAR Value NUM
				tok9=int(tok[i+1][4:])
				VAR=int(VAR[4:])
				if tok9 < VAR :
					ir = i
				else :
					if ir2!=0 :
						i=ir2-5
					ir = 0
					ir2 = 0
					condw += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "WHILE NUM > VAR THEN" : #considering VAR not INPUT
			if condw == 0 and cond == 0 :
				VAR=(getVAR(tok[i+3])) #Get the VAR Value NUM
				tok9=int(tok[i+1][4:])
				VAR=int(VAR[4:])
				if tok9 > VAR :
					ir = i
				else :
					if ir2!=0 :
						i=ir2-5
					ir = 0
					ir2 = 0
					condw += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "WHILE VAR < NUM THEN" : #considering VAR not INPUT
			if condw == 0 and cond == 0 :
				VAR=(getVAR(tok[i+1])) #Get the VAR Value NUM
				tok9=int(tok[i+3][4:])
				VAR=int(VAR[4:])
				if tok9 < VAR :
					ir = i
				else :
					if ir2!=0 :
						i=ir2-5
					ir = 0
					ir2 = 0
					condw += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "WHILE VAR > NUM THEN" : #considering VAR not INPUT
			if condw == 0 and cond == 0 :
				VAR=(getVAR(tok[i+1])) #Get the VAR Value NUM
				tok9=int(tok[i+3][4:])
				VAR=int(VAR[4:])
				if tok9 > VAR :
					ir = i
				else :
					if ir2!=0 :
						i=ir2-5
					ir = 0
					ir2 = 0
					condw += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "WHILE NUM EQEQ NUM THEN" : #considering VAR not INPUT
			if condw == 0 and cond == 0 :
				tok9=int(tok[i+3][4:])
				tok8=int(tok[i+1][4:])
				if tok8 == tok9 :
					ir = i
				else :
					if ir2!=0 :
						i=ir2-5
					ir = 0
					ir2 = 0
					condw += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "WHILE NUM < NUM THEN" : #considering VAR not INPUT
			if condw == 0 and cond == 0 :
				tok9=int(tok[i+3][4:])
				tok8=int(tok[i+1][4:])
				if tok8 < tok9 :
					ir = i
				else :
					if ir2!=0 :
						i=ir2-5
					ir = 0
					ir2 = 0
					condw += 1
			i+=5
		elif tok[i] + " " + tok[i+1][0:3] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] == "WHILE NUM > NUM THEN" : #considering VAR not INPUT
			if condw == 0 and cond == 0 :
				tok9=int(tok[i+3][4:])
				tok8=int(tok[i+1][4:])
				if tok8 > tok9 :
					ir = i
				else :
					if ir2!=0 :
						i=ir2-5
					ir = 0
					ir2 = 0
					condw += 1
			i+=5
		elif tok[i][0:3] + " " + tok[i+1] + " " + tok[i+2] + " " + tok[i+3][0:3] + " " + tok[i+4] + " " + tok[i+5][0:3] == "VAR EQUALS RAND NUM TO NUM" : #considering VAR not INPUT
			if condw == 0 and cond == 0 :
				tok2=int(tok[i+3][4:])
				tok3=int(tok[i+5][4:])
				hasard=str(random.randint(tok2,tok3))
				doASSIGN(tok[i],"NUM:"+hasard)
			i+=6


def run():
	code = open_file(argv[1])
	if code == 0:
		print("FileNotRecognizedError: [Errno 1] can only open *.AleX files.")
		return(0)
	tok = lex(code)
	parse (tok)

run()
