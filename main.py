# declare and intialize registers $0 to $31, lo, and hi to Zero
# reg stores register numbers from $0 - $31
# regVal stores the current value of the registers 
# regVal initialized to Zero
# register_Name stores the name of the registers
reg = []
regVal = []
Address = []
addressData = []
register_Name = [
	'$zero',
	'$at',
	'$v0',
	'$v1',
	'$a0',
	'$a1',
	'$a2',
	'$a3',
	'$t0',
	'$t1',
	'$t2',
	'$t3',
	'$t4',
	'$t5',
	'$t6',
	'$t7',
	'$s0',
	'$s1',
	'$s2',
	'$s3',
	'$s4',
  '$s5',
	'$s6',
	'$s7',
	'$t8',
	'$t9',
	'$k0',
	'$k1',
  '$gp',
	'$sp',
	'$fp',
  '$ra',
]

# assign reg[] with $0 - $31 and set them to zero
count = 0
while(count <= 32):
  reg.append(count)
  regVal.append(0)
  count += 1

# append pc, hi, lo @ index 33, 34, and 35 respectively
register_Name.append("pc")
register_Name.append("hi")
register_Name.append("lo")

# for pc @ index 33, hi @ index 34, lo @ index 35
regVal.append(0)
regVal.append(0)

# prints the registers info as shown in MARS
def printAll():
  i = 0
  print("Name      Number       Value")
  while i < 32:
    print(str(register_Name[i]) +'        $' + str(reg[i]) + '           ' + str(regVal[i]))
    i += 1

  # print index 32 - 35, pc, hi, lo
  i = 32
  while i >= 32 and i < 35:
   print(str(register_Name[i]) +'                       ' + str(regVal[i]))
   i += 1
 
printAll()

#address
count = 2000
while(count <= 3000):
   Address.append("0x" + str(count))
   addressData.append(0)
   count += 4

def printAddress():
  for x, y in zip(Address, addressData):
    # x is from Address, y is from addressData
    print("Address")
    print("0x" + str(x) + "    " +str(y))

    
        

def arithmetic(rd,rs,rt,instr):
  #reg[32] is pc 
  print("instr = ", instr)
  print("rd", rd)
  print("rs", rs)
  print("rt", rt)
  if(instr == "add"):
    regVal[rd] = regVal[rs] + regVal[rt]
    regVal[32] += 4
    print(reg[rd])
    print('$' + str(reg[rd]) + '  ' + str(regVal[rd]))
  elif(instr == "sub"):
    regVal[rd] = regVal[rs] - regVal[rt]
    regVal[32] += 4
    print(reg[rd])
    print('$' + str(reg[rd]) + '  ' + str(regVal[rd]))
  elif(instr == "mult"):
    # multiply
    result = regVal[rs] * regVal[rt]
    result_bin = bin(result)
    print(" # of result bits is", len(result_bin))
    regVal[32] += 4
    if(len(result_bin) <= 32):
      regVal[34] = result
    else: 
      hi = result_bin[0:32]
      lo = result_bin[32:64]
  
  elif(instr == "mfhi"):
    regVal[32] += 4              # update PC
    regVal[rs] = regVal[34]      # remainder moved from hi to register

  elif(instr == "mflo"):
    regVal[32] += 4              # update PC
    regVal[rs] = regVal[34]      # remainder moved from lo to register

  elif(instr == "addi"):
    regVal[32] += 4
    if(rt >= 8192 and rt <= 12288):
      regVal[rd] = hex(rt)
    else:
      regVal[rd] = regVal[rs] + rt 

    #regVal[rd] = regVal[rs] + rt 
    print(regVal[rd])

  elif(instr == "slt"):
    regVal[32] += 4
    print(regVal[rs])
    print(regVal[rt])
    if(regVal[rs] < regVal[rt]):
      regVal[rd] = 1
    else:
      regVal[rd] = 0   

  elif(instr == "sw"):
    regVal[32] += 4
    i = 0
    while(i<len(Address)):
      if(Address[i] == regVal[rt]):
        print(Address[i], regVal[rt])
        addressData[i] = regVal[rs]
        print("addressdata", addressData[i])
      i += 1    

  elif(instr == "lw"):
    regVal[32] += 4 
    print("rs is rd", rs)
    print("rt is source", rt) 
    i = 0
    while(i<len(Address)):
      if(Address[i] == regVal[rt]):
        print(Address[i], regVal[rt])
        regVal[rs] = addressData[i]
        print("addressdata", regVal[rs])
      i += 1   

  

# hex to binary conversion function
def hex_to_bin(instr):
    integer = int(instr, 16)
    binary = '{:032b}'.format(integer)
    return binary


# binary to hex conversion
def bin_to_hex(instr):
    integer = int(instr,2)
    hexadecimal = hex(integer).replace("0x","")
    hexadecimal = hexadecimal.zfill(8)
    return hexadecimal


# the value 255 is not fixed feel free to change it to any other value
def large_val_limiter(strVal):
    if(strVal>255):
        strVal = hex(strVal)
    return str(strVal)


# twos_complement
def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


def saveJumpLabel(asm, labelIndex, labelName):
    lineCount = 0
    for line in asm:
        line = line.replace(" ", "")
        if (line.count(":")):
            labelName.append(line[0:line.index(":")])  # append the label name
            labelIndex.append(lineCount)  # append the label's index
            asm[lineCount] = line[line.index(":") + 1:]
            print(labelName, labelIndex)
        lineCount += 1


def formatChecker(instr):
    checker = False
    if any(c>'f' for c in instr):
        print("Illegal characters")
    if not instr.isalnum():
        print("Special characters are not allowed")
    elif len(instr)!=8:
        print("Hex instruction must contain 8 characters")
    else:
        checker = True
    return checker


functions = {}
functions["100010"] = "sub"     # R-type
functions["100000"] = "add"     # R-type
functions["101010"] = "slt"     # R-type
functions["011000"] = "mult"    # R-type
functions["001100"] = "andi"    # I-type
functions["001000"] = "addi"    # I-type
functions["100011"] = "lw"      # I-type
functions["101011"] = "sw"      # I-type
functions["000100"] = "beq"     # I-type
functions["000101"] = "bne"     # I-type
functions["000010"] = "j"       # J-type


def disassembler(instr, functions):          # supports addi, andi, sub, add, lw, sw and slt

    if instr[0:6] == "000000":
        rs = instr[6:11]
        rt = instr[11:16]
        rd = instr[16:21]
        func = instr[26:32]
        assembly_code = functions[func] + " $" + str(int(rd, 2)) + ", $" + str(int(rs, 2)) + ", $" + str(int(rt, 2))
    else:
          func = instr[0:6]
          rs = instr[6:11]
          rt = instr[11:16]
          imm = twos_comp(int(instr[16:32], 2), 16)
          imm = large_val_limiter(imm)
          assembly_code = functions[func] + " $" + str(int(rt, 2)) + ", $" + str(int(rs, 2)) + ", " + imm

    return assembly_code


def assembler(dataFile, labelName, labelIndex, w):  # supports addi and j
    for line in dataFile:
        index = line.find('#')  # finds comments and removes them for easier processing
        if index != -1:
            line = line[0:index - 1]
        line = line.replace("\n", "")  # Removes extra chars
        line = line.replace("$", "")  # Removes extra chars
        line = line.replace(" ", "")  # Removes extra chars
        line = line.replace("zero", "0")  # can use both $zero and $0
        print(line[0:4])
        if (line[0:4] == "addi"):  # ADDI
            line = line.replace("addi", "")
            line = line.split(",")
            print("addi line 2", line[2], type(line[2]))
            hexdata = line[2]
            print(hexdata[0:2])
            if(hexdata[0:2] == "0x"):
              imm = bin(int(hexdata, 16))[2:].zfill(16)
              print("hex to binary", imm)

            elif (int(line[2]) >= 0):
                imm = format(int(line[2]), '016b')
                print("addi imm",imm)
            else:
                #imm = format(65536 + int(line[2]), '016b')
                imm = bin(int(line[2]))
                print("imm is", imm, type(imm))
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            #binary = "001000" + str(rs) + str(rt) + str(imm)
            #hex_file.write(bin_to_hex(binary) + "\n")
            print(int(rt, 2))
            print(int(rs, 2))
            #print(int(imm, base = 2))
            arithmetic(int(rt,2), int(rs,2), int(imm, base = 2), 'addi')
            printAll()

        elif (line[0:4] == "andi"):  # ANDI
            line = line.replace("andi", "")
            line = line.split(",")
            if (int(line[2]) >= 0):
                imm = format(int(line[2]), '016b')
            else:
                imm = format(65536 + int(line[2]), '016b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "001100" + str(rs) + str(rt) + str(imm)
            hex_file.write(bin_to_hex(binary) + "\n")

        elif (line[0:4] == "mult"):  # MULT
            line = line.replace("mult", "")
            line = line.split(",")
            rs = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')

            binary = "000000" + str(rs) + str(rt) + "0000000000" + "011000"
            hex_file.write(bin_to_hex(binary) + "\n")
            arithmetic(0, int(rt,2), int(rs,2), 'mult')
            printAll()

        elif (line[0:4] == "mflo"):  # MFLO
            line = line.replace("mflo", "")
            line = line.split(",")
            rt = format(int(line[0]), '05b')

            binary = "000000" + str(rs) + str(rt) + "0000000000" + "011000"
            hex_file.write(bin_to_hex(binary) + "\n")
            arithmetic(0, int(rt,2), 0, 'mflo')
            printAll()
        
        elif (line[0:3] == "beq"):  # BEQ
            line = line.replace("beq", "")
            line = line.split(",")
            for i in range(len(labelName)):
                if (labelName[i] == line[0]):
                    imm = str(format(int(labelIndex[i]), '016b'))
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "000100" + str(rt) + str(rs) + str(imm)
            hex_file.write(bin_to_hex(binary) + "\n")

        elif (line[0:3] == "bne"):  # BNE
            line = line.replace("bne", "")
            line = line.split(",")
            print("line", line)
            print("labelname", labelName)
            for i in range(len(labelName)):
                if (labelName[i] == line[0]):
                  print(labelName[i], labelIndex[i])
                  imm = str(format(int(labelIndex[i]), '016b'))
            
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            print("rs", rs)
            print("rt", rt)
            print("imm", imm)
            print(labelName[i], labelIndex[i])
            regVal[32] = labelIndex[i] * 4
            printAll()
            binary = "000101" + str(rt) + str(rs) + str(imm)
            hex_file.write(bin_to_hex(binary) + "\n")

        # TODO
        elif (line[0:2] == "lw"):  # LW
            line = line.replace("lw", "")
            line = line.split(",")
            line[1] = line[1].split('(')
            line[1][1] = line[1][1].replace(")", "")
            if (int(line[1][0]) >= 0):
                imm = format(int(line[1][0]), '016b')
            else:
                imm = format(65536 + int(line[1][0]), '016b')
            rs = format(int(line[1][1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "100011" + str(rs) + str(rt) + str(imm)
            hex_file.write(bin_to_hex(binary) + "\n")
            arithmetic(0, int(rt,2), int(rs,2), 'lw')
            printAll()
            printAddress()

        # TODO
        elif (line[0:2] == "sw"):  # SW
            line = line.replace("sw", "")
            line = line.split(",")
            line[1] = line[1].split('(')
            line[1][1] = line[1][1].replace(")", "")
            line[1][0] = line[1][0].replace("0x", "")
            line[1][0] = int(line[1][0], 16)
            if (int(line[1][0]) >= 0):
                imm = format(int(line[1][0]), '016b')
            else:
                imm = format(65536 + int(line[1][0]), '016b')
            rs = format(int(line[1][1]), '05b')
            rt = format(int(line[0]), '05b')
            print("sw rs", rs)
            print("sw rt", rt)
            print("sw imm", imm)
            binary = "101011" + str(rs) + str(rt) + str(imm)
            hex_file.write(bin_to_hex(binary) + "\n")
            arithmetic(0, int(rt,2), int(rs,2), 'sw')
            printAll()
            

        elif (line[0:3] == "add"):  # ADD
            line = line.replace("add", "")
            line = line.split(",")
            rd = format(int(line[2]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            print(int(rt, 2))
            print(int(rs, 2))
            print(int(rd, 2))
            binary = "000000" + str(rd) + str(rs) + str(rt) + "00000" + "100000"
            hex_file.write(bin_to_hex(binary) + "\n")
            arithmetic(int(rt,2), int(rs,2), int(rd,2), 'add')
            printAll()

        elif (line[0:3] == "sub"):  # SUB
            line = line.replace("sub", "")
            line = line.split(",")
            rd = format(int(line[2]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "000000" + str(rd) + str(rs) + str(rt) + "00000" + "100010"
            hex_file.write(bin_to_hex(binary) + "\n")
            arithmetic(int(rt,2), int(rs,2), int(rd,2), 'sub')
            printAll()


        elif (line[0:3] == "slt"):  # SLT
            line = line.replace("slt", "")
            line = line.split(",")
            rd = format(int(line[2]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "000000" + str(rd) + str(rs) + str(rt) + "00000" + "101010"
            hex_file.write(bin_to_hex(binary) + "\n")
            arithmetic(int(rt,2), int(rs,2), int(rd,2), 'slt')
            printAll()
        
        # TODO    
        elif (line[0:1] == 'j'):  # Jump
            line = line.replace("j", "")
            line = line.split(",")
            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location
            if (line[0].isdigit()):  # First,test to see if it's a label or an immediate (this won't support labels like ex: 1loop or 2exit)
                binary = '000010' + str(format(int(line[0]), '026b'))
                hex_file.write(bin_to_hex(binary) + "\n")
            else:  # Jumping to label
                for i in range(len(labelName)):
                    if (labelName[i] == line[0]):
                        binary = '000010' + str(format(int(labelIndex[i]), '026b'))
                        hex_file.write(bin_to_hex(binary) + '\n')


print("For disassembler press: 'd'\nFor assembler press:    'a'\nFor exit press:         'e' ")
program = input(">")


if (program == 'd'):
    while (program != 'e'):
        instr = input("Enter instruction in hex: ")
        instr = instr.lower()
        if (instr == 'e'):
            exit()
        if (formatChecker(instr)):
            binIstr = hex_to_bin(instr)
            out = disassembler(binIstr, functions)
            print(out + "\n")

if (program == 'a'):
    assembly_file = open("code.txt", "r")
    hex_file = open("hex.txt", "a+")
    labelIndex = []
    labelName = []
    dataFile = assembly_file.readlines()

    for data in range(dataFile.count('\n')):
        dataFile.remove("\n")

    for i in range(2):
        for data in dataFile:
            if (data.startswith('#')):
                dataFile.remove(data)

    saveJumpLabel(dataFile, labelIndex, labelName)

    assembler(dataFile, labelName, labelIndex, hex_file)
    print("Done! Hex_file consists of translated instructions in HEX.")
    hex_file.close()
    assembly_file.close()


