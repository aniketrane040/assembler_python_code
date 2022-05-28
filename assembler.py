class Instruction:
    def __init__(self,type,label,opcode,operand1,operand2,lc):
        self.type = type
        self.label = label
        self.opcode = opcode
        self.operand1 = operand1
        self.operand2 = operand2
        self.location = lc
        
class SymbolTable:
    def __init__(self,symbol,defined,used,value,location):
        self.symbol = symbol
        self.defined = defined
        self.used = used
        self.value = value
        self.location = location
        
class PoolTable:
    def __init__(self,no,pointer):
        self.sr_no = no
        self.literal_pointer = pointer

assembly_file = open("./assembly_program.asm","r")
assembler_directives = ["START","END"]
imperative_statements = ["STOP","ADD","SUB","MUL","MOVER","MOVEM","BC","DIV","READ","PRINT"]
declarative_statements = ["DC","DS"]

labels = []

instruction_list = []
labels_list = []
symboltable_list = []
literal_list = []
pool_list = []
location_counter = no = 0

print("\n\nAssembly Program :\n")
for line1 in assembly_file:
    print(line1)
    execute1 = execute2 = 0
    instruction_array = line1.split()
    instruction_length = len(instruction_array)
    first = instruction_array[0]
    
    for dir in assembler_directives:
        if(first == dir):
            type = "AD"
            opcode = first
            operand2 = ""
            if instruction_length == 2:
                operand2 = instruction_array[1]
            
            if opcode == "END":
                obj = Instruction(type,"",opcode,"",operand2,"")
            else:
                obj = Instruction(type,"",opcode,"",operand2,location_counter)
            
            instruction_list.append(obj)
            if(opcode == "START"): 
                location_counter = int(operand2)
                location_counter+=1
                
            execute1 = execute1 + 1
            break 
    
    if execute1 > 0:
        continue
        
    for stat in imperative_statements:
        if(first == stat):
            type = "IS"
            opcode = first
            operand1 = ""
            operand2 = ""
            if instruction_length == 2:
                operand2 = instruction_array[1]
            elif instruction_length == 3:
                operand1 = instruction_array[1]
                operand2 = instruction_array[2]
            
            obj = Instruction(type,"",opcode,operand1,operand2,location_counter)
            instruction_list.append(obj)
            location_counter+=1
            execute2 = execute2 + 1
            break
    
    if execute2 > 0:
        continue
      
    if first != "END":
        label = first
        labels.append(label)
        type = "DL"
        opcode = ""
        operand2 = ""
        opcode = instruction_array[1]
        if instruction_length == 3:
            operand2 = instruction_array[2]            
        obj = Instruction(type,label,opcode,"",operand2,location_counter)
        instruction_list.append(obj)
        labels_list.append(obj)
        if opcode == "DS":
            location_counter = location_counter + int(operand2)
        else:
            location_counter+=1
        

label_in_symboltable = []
errors = []
myLiteralDict = {}

print("\n\nInstruction Table")
print("Type   Label   Opcode  operand1 oper2   Location Counter")
print("____________________________________________________")
for tmp in instruction_list:
    print(tmp.type,"\t",tmp.label,"\t",tmp.opcode,"\t",tmp.operand1,"\t",tmp.operand2,"\t",tmp.location)
    if tmp.type == "IS" and tmp.opcode != "STOP":
        operand2 = tmp.operand2
        if operand2[0] == "=":
            no+=1
            obj2 = PoolTable(no,"#"+str(no))
            pool_list.append(obj2)
            myLiteralDict[operand2] = location_counter
            location_counter+=1
        else:
            label_done = label_in_symboltable.count(operand2)
            if label_done > 0:
                print("",end = "")
            else:
                location = value = 0
                for i in labels_list:
                    if i.label == operand2:
                        location = i.location
                        value = int(i.operand2)
                label_in_symboltable.append(operand2)
                exists = labels.count(operand2)
                defined = "YES" if exists > 0 else " NO"
                used = "YES"
                obj = SymbolTable(operand2,defined,used,value,location)
                symboltable_list.append(obj)
                if defined == " NO":
                    errors.append("symbol "+operand2+" is not defined")

print("\n\nSymbol Table :\n")
print("symbols     defined     used   value     Location")
print("____________________________________________________")
for tmp in symboltable_list:
    print(tmp.symbol,end = "            ")
    print(tmp.defined,end = "        ")
    print(tmp.used,end = "      ")
    print(tmp.value,end = "         ")
    print(tmp.location)

srno = 1
print("\n\nLiteral Table :\n")
print("Sr.no     literals          LocationCounter")
print("____________________________________________________")
for tmp in myLiteralDict.keys():
    print(srno,end = "           ")
    print(tmp,end = "           ")
    print(myLiteralDict[tmp])
    srno+=1

print("\n\nPool Table :\n")
print("Sr.no     literal pointer")
print("____________________________________________________")
for tmp in pool_list:
    print(tmp.sr_no,end = "           ")
    print(tmp.literal_pointer)    

print("\n\nErrors ",len(errors))
for error in errors:
    print(error)      
