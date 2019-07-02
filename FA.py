class FA:
    def __init__(self, nstates):
        self.transitions = [{} for i in range(nstates)]
        self.accept_states = [False] * nstates

    def register(self, source_state, char, target_state):
        self.transitions[source_state][char] = target_state

    def register_accept(self, state):
        self.accept_states[state] = True

    def accept(self, input):
        state = 0
        try:
            for char in input:
                state = self.transitions[state][char]
            return self.accept_states[state]
        except KeyError:
            return False

    def longest_prefix_accepted(self, input):
        state = 0
        prefix = ""
        try:
            for char in input:
                state = self.transitions[state][char]
                prefix += char
            return prefix
        except KeyError:
            return prefix

    def get_transitions(self):
        return self.transitions

    def get_accept_states(self):
        return self.accept_states


def read_inputs():
    with open('input.txt', 'r') as f:
        statesNumber = int(f.readline())
        autfin = FA(statesNumber)
        acceptedStatesLine = f.readline()
        acceptedStates = acceptedStatesLine.split(",")
        for i in acceptedStates:
            autfin.register_accept(int(i))
        for line in f:
            transitionsInputs = line.split(",")
            startState = transitionsInputs[0]
            char =  transitionsInputs[1]
            targetState = transitionsInputs[2]
            autfin.register(int(startState), char, int(targetState))
    return autfin


def main_menu():
    print("Main Menu:")
    print("0.Exit.")
    print("1.Read Inputs.")
    print("2.Print menu.")
    print("3.Check if a sequence is accepted by DFA.")
    print("4.Get the longest prefix from a sequence accepted by DFA")
    print()


def print_menu():
    print("Print Menu:")
    print("0.Exit to main menu.")
    print("1.Print states.")
    print("2.Print alphabet.")
    print("3.Print transitions.")
    print("4.Print final states")
    print()


def print_states(autfin):
    transitions = autfin.get_transitions()
    states = ""
    print("States:\n")
    for i in range(transitions.__len__()):
            states += str(i) + ","
    print(states)
    print()


def print_alphabet(autfin):
    transitions = autfin.get_transitions()
    alphabet = ""
    print("Alphabet:\n")
    for i in range(transitions.__len__()):
        for key in transitions[i]:
            if key not in alphabet:
                alphabet += key + ","
    print(alphabet+"\n")


def print_transitions(autfin):
    transitions = autfin.get_transitions()
    print("Transitions:\n")
    for i in range(transitions.__len__()):
        for key in transitions[i]:
            print("Start state: {}, Char: {}, End state: {}\n".format(i,key,transitions[i][key]))
    print()


def print_final_states(autfin):
    transitions = autfin.get_transitions()
    print("Final States:\n")
    finalStates = ""
    for i in range(transitions.__len__()):
        if (not transitions[i]):
            finalStates += str(i) + ","
        else:
            finalStateToken = True
            for key in transitions[i]:
                if(i != transitions[i][key]):
                    finalStateToken = False
            if(finalStateToken == True):
                finalStates += str(i) + ","
    print(finalStates+"\n")


def check_sequence(autfin, sequence):
    print(str(autfin.accept(sequence))+"\n")


def longest_prefix(autfin, sequence):
    prefix = autfin.longest_prefix_accepted(sequence)
    if prefix == "" :
        print("None.\n")
    else:
        print(str(prefix)+"\n")


if __name__ == '__main__':
    autfin = FA(0)
    exitToken = 0
    while exitToken == 0:
        main_menu()
        try:
            option = int(input('Enter the option: \n'))
            print()
            if option == 0:
                exitToken = 1
                print("Exiting program.\n")
            elif option == 1:
                autfin = read_inputs()
            elif option == 2:
                exitToken2 = 0
                while exitToken2 == 0:
                    print_menu()
                    try:
                        option2 = int(input('Enter the option for print menu: \n'))
                        print()
                        if option2 == 0:
                            exitToken2 = 1
                        elif option2 == 1:
                            print_states(autfin)
                        elif option2 == 2:
                            print_alphabet(autfin)
                        elif option2 == 3:
                            print_transitions(autfin)
                        elif option2 == 4:
                            print_final_states(autfin)
                        else:
                            print("Option number '{}' is not a valid option.Please choose another option:\n".format(option2))
                    except:
                        print("Option must be a number.")
            elif option == 3:
                sequence = input('Enter the sequence: \n')
                print()
                check_sequence(autfin, sequence)
            elif option == 4:
                sequence = input('Enter the sequence: \n')
                print()
                longest_prefix(autfin, sequence)

            else:
                print("Option number '{}' is not a valid option.Please choose another option:\n".format(option))
        except:
            print("Option must be a number.\n")
