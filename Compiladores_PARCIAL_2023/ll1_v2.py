import pandas as pd
import lexico_v2 as l2
import graphviz

counter = 1
dot = ''
#Tabla de la diapositiva
syntax_table = pd.read_csv("Compiladores_PARCIAL_2023/Tabla_comas_3.csv", index_col=0)


# Función para buscar un nodo en una lista de nodos
def buscar_en_arbol(node_list, id):
  for nod in node_list:
    if nod.symbol.id == id:
      return nod
# Función para imprimir el árbol sintáctico en formato Graphviz
def imprimir_arbol(node, node_list):
    global dot
    dot = "digraph G { \n"    
    # Iteramos sobre cada nodo de la lista de nodos
    for nod in node_list:
        # Si es un nodo terminal, lo representamos con su símbolo y su lexema
        if nod.symbol.terminal: 
            if nod.symbol.symbol == 'e':
                dot += str(nod.symbol.id) + ' [ label=< <b>' + nod.symbol.symbol + '</b> > ]; \n'            
            else:             
                lexeme = nod.lexeme
                lexeme = "&#38;" if lexeme == '&' else nod.lexeme # el & genera errores en dot, por eso lo pasamos en codigo HTML
                dot += str(nod.symbol.id) + ' [ label=< <b>' + nod.symbol.symbol + '</b> <br/>' + str(lexeme) + ' <br/> line '+ str(nod.line) + ' > ]; \n'                       
        else:
            # Si es un nodo no terminal, lo representamos con su símbolo
            dot += str(nod.symbol.id) + ' [ label=" ' + nod.symbol.symbol + ' " ]; \n' 
    
    imprimir_arbol_r(node) # Llamamos a la función auxiliar para imprimir las conexiones entre los nodos     
    dot += "}" # Cerramos la cadena Graphviz

def imprimir_arbol_r(node):
    global dot
    tmp = []
    for child in node.children:
        # Imprimimos una conexión desde el nodo padre hasta cada uno de sus hijos
        dot += str(node.symbol.id) + ' -> ' + str(child.symbol.id) + '; \n'
        tmp.append(str(child.symbol.id))
        imprimir_arbol_r(child)

    if len(node.children) > 0:
         # Si el nodo padre tiene hijos, los colocamos en la misma fila
        dot += "{ \n"
        dot += "    rank = same; \n"
        dot += "    edge[ style=invis]; \n"
        dot += " -> ".join(tmp) + "; \n"
        dot += "    rankdir = LR; \n"
        dot += "} \n" 


class Node:
  def __init__(self, symbol, lexeme = None, children = [], father = None, line = None):
    self.symbol = symbol
    self.lexeme = lexeme
    self.line = line
    self.children = children
    self.father = father
 
class NodeStack:
  def __init__(self, symbol, terminal):
    global counter
    self.id = counter
    self.symbol = symbol
    self.terminal = terminal
    counter += 1

class Token:
  def __init__(self, type, lexeme, line):
    self.type = type
    self.lexeme = lexeme
    self.line = line

def parser_t(tokens):
  band = False
  while True:
    if stack[0].symbol == '$' and tokens[0].type == '$':
      band = True #Son dolar
      break
    #Cuando son terminales 
    if stack[0].terminal:
      #print("Terminales ...") 
      #Si son iguales
      if stack[0].symbol == tokens[0].type:
        #Actualizar el arbol sintactico
        nod = buscar_en_arbol(node_list, stack[0].id)
        #Actualizamos lexeme y line
        nod.lexeme = tokens[0].lexeme
        nod.line = tokens[0].line
        #Eliminamos el simbolo de la pila y el token de la lista
        stack.pop(0)
        tokens.pop(0)
      else:
        band = False
        print("Error sintactico: Los terminales son diferentes. ")
        break
    #cuando reemplazar en la pila, segun tabla sintactica
    else:
      if not Actualizar_pila(stack,tokens[0].type):
        band = False
        print("Error sintactico: No se actualizo la pila")
        break

  return band

def Actualizar_pila(stack, tokens):
  #print("S: ",stack[0].symbol, " t: ",tokens)
  production = syntax_table.loc[ stack[0].symbol][tokens]
  #print("Primera produccion: ",production)
  if str(production) == "nan": #produccion 
    return False
  
  elementos = production.split(" ")
  elementos.pop(0)
  elementos.pop(0) 

  #Reemplazo
  father = stack.pop(0) # eliminamos el primer elemento de la pila
  node_father = buscar_en_arbol(node_list, father.id)

  if elementos[0] == " ":
        # error sintactico
        return False    
  if elementos[0] == "''":
    return True
 
    
  for prod in range(len(elementos)-1,-1,-1):
    #se crea un nuevo objeto NodeStack 
    new_symbol = NodeStack( elementos[prod], True if elementos[prod].isupper() else False )
    # que se inserta en la pila en la parte superior
    stack.insert(0, new_symbol)
    #y un nuevo objeto Node 
    node_tree = Node(new_symbol, None, [], node_father) 
    # que se inserta en el árbol como hijo del nodo padre
    node_father.children.insert(0, node_tree)
    node_list.append(node_tree)
  return True

if __name__ == "__main__":
  
  #Lista de tokens
  tokens=[]
  #Recorrer hasta el tamaño de la lista tokens_lexico_v2
  for i in l2.tokens_lexico:
    tipo = i['type']
    lexeme = i['lexeme']
    line = i['line']
    token_ = Token(tipo, lexeme, line)
    tokens.append(token_)

  #Agregar el $ al final
  token_end = Token("$", "$", 1)
  tokens.append(token_end)

  #print("Primer elemento: ", tokens[0].type)
  
  stack = []
  node_symb = NodeStack("programa", False) #Simbolo
  node_dolar = NodeStack("$", True) #Terminal
  stack = [ node_symb, node_dolar ]

 #Crear nodo del arbol sintactico empenzando por el primero
  root = Node(node_symb)
  node_list = [] # creamos una lista para guardar los nodos
  node_list.append(root)

  #Imprime True o False
  print(parser_t(tokens))
  
  imprimir_arbol(root,node_list)

  #Crear objeto Source y dot es la cadena de texto
  graph = graphviz.Source(dot)
  #Generamos archivo DOT PDF
  graph.render('Compiladores_PARCIAL_2023/ouput_4.dot', view=True)

  #print(dot)