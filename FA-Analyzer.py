import FA
import string

def only_letters(string):
    letters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]

    for c in string:
        if c.lower() not in letters:
            return False
    return True


def is_separator(c):
    if c in [';', ',', '(', ')', '[', ']', ':', ' ']:
        return True
    return False


def is_composite_operator(c1, c2):
    if (c1+c2 == '==' or c1+c2 == '!=' or c1+c2 == '<=' or c1+c2 == '>='):
        return 2
    else:
        if (c1 == '+' or c1 == '-' or c1 == '*' or c1 == '/' or c1 == '%' or
                c1 == '=' or c1 == '<' or c1 == '>' or c1 == '!'):
            return 1
        return 0
    
def is_present(token, ST, token_type):
    res = -1
    for i in range(len(ST)):
        if (ST[i][0] == token_type and ST[i][1] == token) :
            res = i
    return res


def process_separators(c, PIF):
    separatorsDict = {
        ';': 101,
        ',': 102,
        '(': 103,
        ')': 104,
        '[': 105,
        ']': 106,
        ':': 107,
        ' ': 108
    }
    PIF.append((separatorsDict[c], -1))


def process_operator(PIF, c1, c2=None):
    operatorsDict = {
        '+': 201,
        '-': 202,
        '*': 203,
        '/': 204,
        '%': 205,
        '=': 206,
        '<': 207,
        '<=': 208,
        '==': 209,
        '!=': 210,
        '>=': 211,
        '>': 212,
        '!': 213
    }
    if c2 is None:
        PIF.append((operatorsDict[c1], -1))
    else:
        PIF.append((operatorsDict[c1+c2], -1))


def process_token(token, PIF, ST, lineIdx , iFA, cFA):
    tokensDict = {
        'INT': 301,
        'CHAR': 302,
        'STR': 303,
        'BOOL': 304,
        'LIST': 305,
        'WHILE': 306,
        'DO': 307,
        'ENDWHILE': 308,
        'IF': 309,
        'THEN': 310,
        'ELIF': 311,
        'ELSE': 312,
        'ENDIF': 313,
        'READ': 314,
        'WRITE': 315,
        'START': 316,
        'END': 317,
        'BEGIN': 318,
    }
    if token != '':
        # Constant
        if cFA.accept(token):
            print("Token: {} is accepted as constant by ConstantsFA.".format(token))
            token_type = 2
            res = is_present(int(token), ST, token_type)
            if res == -1:
                ST.append((2,int(token)))
                PIF.append((2, len(ST)))
            else:
                PIF.append((2, res+1))

        # Reserved word
        elif token.upper() in tokensDict:
            PIF.append((tokensDict[token.upper()], -1))

        # Identifier
        else:
            token_type = 1 
            if iFA.accept(token):
                print("Token: {} is accepted as identifier by IdentifiersFA".format(token))
                res = is_present(token, ST, token_type)
                if res == -1:
                    ST.append((1,token))
                    PIF.append((1, len(ST)))
                else:
                    PIF.append((1, res+1))
            elif len(token) > 250:
                raise Exception(
                    "Identifier '{}' on line {}".format(token, lineIdx) +
                    " has a length higher than 250 characters!")
            else:
                raise Exception("Identifier '{}'".format(token) +
                                " is invalid on line {}!".format(lineIdx))


def process_string_token(token, PIF, ST, lineIdx, sFA):
    allowedChars = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1',
        '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ', '-', '_', '.'
    ]

    token_type = 3
    if sFA.accept(token):
        print("Token: {} is accepted as string by StringsFA".format(token))
        res = is_present(str(token), ST, token_type)
        if res == -1:
            ST.append((3,str(token)))
            PIF.append((3, len(ST)))
        else:
            PIF.append((3, res+1))


def print_ST(ST):
    
    print('\nSymbol Table:\n')
    for i in range(len(ST)):
        print("Nr: {} Type: {} Value: {}.".format(i,ST[i][0],ST[i][1]))


def print_PIF(PIF):

    print('\nProgram Internal Form:\n')
    for i in range(len(PIF)):
        print("Token: {} Position in ST: {}".format(PIF[i][0],PIF[i][1]))



if __name__ == '__main__':

    #Creating FA for Identifiers
    identifierFA = FA.FA(2)
    identifierFA.register_accept(1)
    identifierFA.register(0, "_", 1)
    for i in string.ascii_letters:
        identifierFA.register(0,i,1)
        identifierFA.register(1, i, 1)
    for i in string.digits:
        identifierFA.register(1,i,1)
    identifierFA.register(1,"_",1)

    #Creating FA for Constants
    constantsFA = FA.FA(3)
    constantsFA.register_accept(1)
    constantsFA.register_accept(2)
    constantsFA.register(0,"-",1)
    for i in ("123456789"):
        constantsFA.register(0,i,1)
    for i in string.digits:
        constantsFA.register(1,i,1)
    constantsFA.register(0,"0",2)

    #Creating FA for Strings
    stringsFA = FA.FA(2)
    stringsFA.register_accept(1)
    for i in string.printable:
        stringsFA.register(0,i,1)
        stringsFA.register(1,i,1)

    symbolTable = []
    programInternalForm = []
    lineIdx = 0
    
    # Read from keybord the name of the file.
    nb = input('Enter the name of the file: ')
    
    # Open the input file
    with open(nb+".txt" , 'r') as fh:
        line = fh.readline()

        # Read line by line
        while line:
            # print('Line:\n' + line)
            lineIdx += 1
            pos = 0

            # Skip over the indentation spaces
            while is_separator(line[pos]):
                process_separators(line[pos], programInternalForm)
                pos += 1
            token = line[pos]
            pos += 1
            tokenFlag = False
            stringFlag = False
            
            # Iterate over each character
            while pos < len(line) - 1:
                # print('Token:\n' + token)
                # print('CHAR:\n' + line[pos])
                
                # Check if character inside a strig
                if stringFlag is True and not (line[pos] == "'"):
                    token += line[pos]
                elif only_letters(line[pos]) is True:
                    token += line[pos]
                elif line[pos].isdigit() is True:
                    token += line[pos]
                    
                # Check if character is the start of a string symbol (') 
                elif line[pos] == "'" and stringFlag is False:
                    stringFlag = True
                    programInternalForm.append((4, -1))
                    
                # Check if the character is the end of a string symbol (')
                elif line[pos] == "'" and stringFlag is True:
                    stringFlag = False
                    process_string_token(
                        token, programInternalForm, symbolTable, lineIdx, stringsFA
                    )
                    programInternalForm.append((4, -1))
                    token = ''
                elif line[pos] == '-' and line[pos + 1].isdigit() is True:
                    token += line[pos]
                    
                # Check if the character is a separator
                elif is_separator(line[pos]) is True:
                    process_token(
                        token, programInternalForm, symbolTable, lineIdx, identifierFA, constantsFA
                    )
                    tokenFlag = True
                    process_separators(line[pos], programInternalForm)
                    token = ''
                # Check if the character is an operator
                else:
                    res = is_composite_operator(line[pos], line[pos + 1])

                    # If we have a simple operator
                    if res == 1:
                        process_token(
                            token, programInternalForm, symbolTable, lineIdx, identifierFA, constantsFA
                        )
                        tokenFlag = True
                        process_operator(programInternalForm, line[pos])
                        token = ''

                    # If we have a composite operator
                    elif res == 2:
                        process_token(
                            token, programInternalForm, symbolTable, lineIdx, identifierFA, constantsFA
                        )
                        tokenFlag = True
                        process_operator(programInternalForm,
                                         line[pos], line[pos + 1])
                        token = ''

                    # If we have an unsupported character
                    else:
                        raise Exception(
                            "Invalid character at line: {}!". format(lineIdx))
                pos += 1
            # If is not ending with a separator
            if tokenFlag is False:
                process_token(
                    token, programInternalForm, symbolTable, lineIdx, identifierFA, constantsFA
                )
            # Read next line
            line = fh.readline()
    print_ST(symbolTable)
    print_PIF(programInternalForm)
    
