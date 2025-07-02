import operator as op
import sys
from math import sqrt


# boloshi damatebuli maqvs logika rom bevri xazis wakitxva sheedzlos (magalitad bevri define ro aqvs), aseve shua xazshi rom gawyvitos sqemis kodi
#gaagrdzelebs manam sanam frchxilebs sworad ar sheiyvans momxmarebeli


# P.S. bodishit legacy kodistvis


def to_list(*args):
    lst = []
    for i in args:
        lst.append(i)
    return lst

def addition(*args):
    sum = 0
    for i in args :
        sum = sum + i
    return sum
def cons_logic(elem,lst):
    lst.insert(0,elem)
    return lst
def append_logic(*args):
    res = []
    for lst in args:
        for i in lst:
            res.append(i)
    return res

my_dict = {
    '+' : addition,
    '-' : op.sub,
    '*' : op.mul,
    '/' : op.truediv,
    '>' : op.gt,
    '<' : op.lt,
    '<=' : op.le,
    '>=' : op.ge,
    '==' : op.eq,
    'car' : lambda x : x[0],
    'cdr' : lambda x : x[1:],
    'list' : to_list,
    'null?' : lambda x : x is None,
    'length' : lambda x : len(x),
    'and' : lambda x,y : x and y,
    'or' : lambda x,y : x or y,
    'append' : append_logic,
    'sqrt' : lambda x : sqrt(x)
}

def translate_input(str1) : 
    return str1.replace("("," ( ").replace(")", " ) ").split()


def interpret(column,environment):
    return evaluate(tokenize(translate_input(column),environment),environment)


#yofs shemotanil informacias listebad (yoveli gaxsnili da shesabamisi daxuruli frchxili warmoadgens lists)
def tokenize(input_list,dict):
    if(len(input_list) == 0):
        print("Enter Something")
        return None
    first_elem = input_list.pop(0)
    if(first_elem == '('):
        tmp_list = []
        while(input_list[0] != ')'):
            tmp_list.append(tokenize(input_list,dict))
        input_list.pop(0)
        return tmp_list
    elif(first_elem in dict):
        return first_elem
    elif(first_elem == 'define'):
        if(input_list[0] == '('):
            arr = tokenize(input_list,dict)
            body = tokenize(input_list,dict)
            dict.update({arr[0] : procedure(arr[1:],body)})
        else:
            new_name = input_list.pop(0)
            body = evaluate(tokenize(input_list,dict),my_dict)
            dict.update({new_name : body})
        return "define"
    elif(first_elem == "\'"):
        arr = []
        arr.append("quote")
        arr.append(tokenize(input_list,dict))
        return arr
    x = number_or_boolean(first_elem)
    if(x is not None):
        return x
    else:
        return first_elem


def evaluate(tokenized_list, dict):
    if(isinstance(tokenized_list,list)):
        if(len(tokenized_list) == 0) :
            return []
        if(isinstance(tokenized_list[0],list)):
            tokenized_list[0] = evaluate(tokenized_list[0],dict)
            return evaluate(tokenized_list,dict)
        if(tokenized_list[0] in dict):
            proc3 = dict[tokenized_list[0]]
            args = []
            for arg in tokenized_list[1:] :
                args.append(evaluate(arg,dict))
            return proc3(*args)
        elif(tokenized_list[0] == "define"):
            return tokenized_list[0]
        elif(tokenized_list[0] == "if"):
            return evaluate(tokenized_list[2],dict) if evaluate(tokenized_list[1],dict) else evaluate(tokenized_list[3],dict)
        elif(tokenized_list[0] == "quote"):
            return tokenized_list[1]
        elif(tokenized_list[0] == "lambda"):
            body = tokenized_list[2].copy()
            proc2 = procedure(tokenized_list[1],body)
            dict.update({"n_procedure" : proc2})
            return "n_procedure"
        elif(tokenized_list[0] == "apply"):
            tokenized_list.pop(0)
            proc1 = tokenized_list[0]
            new_tokenized_list = evaluate(tokenized_list[1],dict)
            new_tokenized_list.insert(0,proc1)
            return evaluate(new_tokenized_list,dict)
        elif(tokenized_list[0] == "cons"):
            elem = tokenized_list[1]
            lst = tokenized_list[2][1]
            lst.insert(0,elem)
            return lst
        elif(tokenized_list[0] == "eval"):
            return evaluate(evaluate(tokenized_list[1],dict),dict)
        elif(tokenized_list[0] == "map"):
            proc = evaluate(tokenized_list[1],dict)
            if(proc == "n_procedure"):
                proc = dict["n_procedure"]
            lists = []
            for i in tokenized_list[2:] :
                lists.append(evaluate(i,dict))
            res = []
            ind = 0
            for i in lists[0] :
                tmp = []
                for lst in lists:
                    tmp.append(lst[ind])
                ind = ind+1
                res.append(proc(*tmp))
            return res
        return tokenized_list
    elif(tokenized_list in dict):
        return dict[tokenized_list]
    x = number_or_boolean(tokenized_list)
    if(x is not None):
        return x
    print("error")
    return None
    

def number_or_boolean(elem):
    
    try:
        return int(elem)
    except (ValueError,TypeError) as e:
        if(elem == "#t" or elem == "#T"):
            return True
        elif(elem == "#f" or elem == "#F"):
            return False
        else:
            return None


#klasis meshveobit vinaxav momxmareblis mier shemotanil metods da __call__ metodi maqvs gadatvirtuli
class procedure: 
    def __init__(self,parameters,body):
        self.parameters = parameters
        self.body = body
    def __call__(self, *args): # (+ a b)
        my_env = my_dict
        cur_ind = 0
        for param in self.parameters : 
            my_env.update({param : args[cur_ind]})
            cur_ind = cur_ind+1
        return evaluate(self.body.copy(),my_env)



#aq konsolshi shemotanis logika miweria
prev_inp_buffer = ""
brace_counter = 0
while(True):
    inp = input("kawa>>")
    if(inp.lower() == "exit"):
        break
    to_interpret = ""
    for i in inp:
        to_interpret += i
        if (i == '('):
            brace_counter = brace_counter+1
        elif(i == ')'):
            brace_counter = brace_counter-1
        if(brace_counter == 0 and to_interpret.strip() != ""):
            print(interpret(prev_inp_buffer + to_interpret,my_dict))
            to_interpret = ""
            prev_inp_buffer = ""
    if(brace_counter != 0):
        prev_inp_buffer = prev_inp_buffer + to_interpret