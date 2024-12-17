import sys, getopt
import time

# By default I want the real input, and *not* to debug.
ARG_data = 'input.txt'
ARG_debugLogging = False

# Get the args off the command-line
opts, args = getopt.getopt(sys.argv[1:],"td",["test","debug"])
for opt, arg in opts:
    if opt in ("-t", "--test"):
        print(f"\33[31mUSING TEST DATA\33[0m")
        ARG_data = 'test.txt'
    elif opt in ("-d", "--debug"):
        ARG_debugLogging = True

# Useful during testing to see what the hell is going on
def debug(thing):
    if ARG_debugLogging:
        print(f"\33[39mDEBUG:\33[0m {thing}")

answer_p1 = 0
answer_p2 = 0

import re

registers, program = open(ARG_data).read().split('\n\n')

ra, rb, rc = list(map(int,re.findall(r'(\d+)\n.*(\d+)\n.*(\d+)', registers)[0]))
program = list(map(int,re.findall(r'([\d,]+)', program)[0].split(",")))

# ra, rb, rc = 0, 2024, 43690
# program = [4,0]

def computer(program, ra, rb, rc):
    def combo(operand):
        if operand < 4:
            return operand
        if operand == 4:
            return ra
        if operand == 5:
            return rb
        if operand == 6:
            return rc


    pointer = 0
    output = []

    while pointer < len(program):
        opcode = program[pointer]
        operand = program[pointer+1]

        #print(f"{opcode=}; {operand=}; {combo(operand)=}; {pointer=}; {ra=}; {rb=}; {rc=}")
        match opcode:
            # adv (division ra/combo, write to ra)
            case 0:
                #print("ra = ra // pow(2, combo(operand))")
                ra = ra // pow(2, combo(operand))

            # bxl (bitwise XOR of rb and literal operand, write to rb)
            case 1:
                #print("rb = rb ^ operand")
                rb = rb ^ operand

            # bst (modulo 8 of combo operand, write to rb)
            case 2:
                #print("rb = combo(operand) % 8")
                rb = combo(operand) % 8

            # jnz (nothing if ra == 0; set pointer to literal operand; don't increase pointer by 2)
            case 3:
                #print("set pointer to operand if ra != 0")
                if ra != 0:
                    pointer = operand
                    continue # skip to next opcode, without incrementing pointer at bottom of running loop

            # bxc (bitwise XOR of rb and rc, writes to rb; doesn't use operand)
            case 4:
                #print("rb = rb ^ rc")
                rb = rb ^ rc

            # out (modulo 8 of combo operand, writes to output)
            case 5:
                #print("output.append(combo(operand) % 8)")
                output.append(combo(operand) % 8)

            # bdv (division ra/combo, write to rb)
            case 6:
                #print("rb = ra // pow(2, combo(operand))")
                rb = ra // pow(2, combo(operand))
            
            # cdv (division ra/combo, write to rc)
            case 7:
                #print("rc = ra // pow(2, combo(operand))")
                rc = ra // pow(2, combo(operand))


        pointer += 2
        #print(f"{pointer=}; {ra=}; {rb=}; {rc=}")
        #print("")
    
    return output


answer_p1 = ",".join(list(map(str,computer( program, ra, rb, rc))))


# Print out the answers
print(f"\33[32m__P1__: \33[1m{answer_p1}\33[0m")
print(f"\33[32m__P2__: \33[1m{answer_p2}\33[0m")

# Tell me how inefficecient my code is
print(f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m")