import ply.lex as lex

#INTEGRANTES:
#Olger Quispe Vilca
#Jorge Olivera Ticona

#Palabras clave
reserved = {
  #LEXEMA : TIPO
  'funcion':'FUNCION',
  'entero':'ENTERO',
  'flotante':'FLOTANTE',
  'caracter':'CARACTER',
  'cadena':'CADENA',
  'booleano':'BOOLEANO',
  'verdadero':'VERDADERO',
  'falso':'FALSO',
  'si':'SI',
  'sino':'SINO',
  'mientras':'MIENTRAS',
  'imprimir':'IMPRIMIR',
  'retornar':'RETORNAR',
  'entrada':'ENTRADA',
}

#Lista de nombres de los tokens

tokens = [
  'COMENTARIO','LITERAL','IDENTIFICADOR','NUMERO','REAL','OP_SUM','OP_RES','OP_MUL',
  'OP_DIV','OP_Y','OP_O','OP_MENOR','OP_MEIGUAL','OP_MAYOR','OP_MAIGUAL','OP_IGUAL',
  'OP_DIGUAL','OP_DIST','OP_COM','OP_PCOMA','OP_IPARENT','OP_DPARENT','OP_ILLAV',
  'OP_DLLAV'
] + list(reserved.values())

#Expresion regular para tokens simples

t_OP_SUM = r'\+'
t_OP_RES = r'-'
t_OP_MUL = r'\*'
t_OP_DIV = r'\/'
t_OP_Y = r'Y'
t_OP_O = r'O'
t_OP_MENOR = r'\<'
t_OP_MEIGUAL = r'\<\='
t_OP_MAYOR = r'\>'
t_OP_MAIGUAL = r'\>\='
t_OP_IGUAL = r'\='
t_OP_DIGUAL = r'\=\='
t_OP_DIST = r'\!\='
t_OP_COM = r'\,'
t_OP_PCOMA = r'\;'
t_OP_IPARENT = r'\('
t_OP_DPARENT = r'\)'
t_OP_ILLAV = r'\{'
t_OP_DLLAV = r'\}'

def t_IDENTIFICADOR(t):
  r'[a-z][a-z0-9]*'
  t.type=reserved.get(t.value,'IDENTIFICADOR')# Comprobación de palabras reservadas
  return t

def t_COMENTARIO(t):
  r'([$].+)'
  return t

def t_NUMERO(t):
  #r'^([0-9]+)$'
  r'[0-9]+'
  t.value = int(t.value) # guardamos el valor del lexema
  return t

def t_REAL(t):
    r'([0-9]+.[0-9]*)|([0-9]*.[0-9]+)'
    t.value = float(t.value)
    return t

def t_LITERAL(t):
  #r'\d+'
  r'(["].+["])'
  return t

# Define una regla para que podamos rastrear los números de línea
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
  
# Una cadena que contiene caracteres ignorados (espacios y tabuladores)
t_ignore = ' \t'

# Regla de tratamiento de errores
def t_error(t):
  print("Caracter Ilegal '%s'" % t.value[0])
  t.lexer.skip(1)

#Construir el Lexer
lexer=lex.lex()

#Abrir el codigo y luego leerlo
with open('Compiladores_PARCIAL_2023/codigo_4.txt') as f:
  data = f.read()

#Entrada
lexer.input(data)

#Tokenize
tokens_lexico=[] #Lista para guardar diccionarios
while True:
  tok = lexer.token()
  if not tok:
    break
  C={}
  #print(tok)
  #print(tok.type,tok.value) 
  #print(tok.type, tok.value, tok.lineno, tok.lexpos)
  C['type'] = tok.type 
  C['lexeme'] = tok.value
  C['line'] = tok.lineno
  tokens_lexico.append(C)
  #print(tok.type,tok.value,tok.lineno)

#print(tokens_lexico)
  

