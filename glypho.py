import sys
import string

# instructions decimal value
NOP = 0
INPUT = 1
ROT = 3
SWAP = 4
PUSH = 5
RROT = 9
DUP = 10
ADD = 11
L_BRACE = 12
OUTPUT = 13
MULTIPLY = 14
EXECUTE = 15
NEGATE = 16
POP = 17
R_BRACE = 18

def int2base(x, base):
	digs = string.digits + string.ascii_uppercase

	if x < 0:
		sign = -1
	elif x == 0:
		return digs[0]
	else:
		sign = 1

	x *= sign
	digits = []

	while x:
		digits.append(digs[int(x % base)])
		x = x // base

	if sign < 0:
		digits.append('-')

	digits.reverse()

	return ''.join(digits)

def translateInstruction(instruction):
	# translate from ASCII chars into instruction opcode
	instr_len = 4
	opcode = [-1] * instr_len
	k = -1
	for i in range(instr_len):
		if opcode[i] == -1:
			k += 1
			opcode[i] = k
			for j in range(i + 1, instr_len):
				if instruction[i] == instruction[j]:
					opcode[j] = k

	# map instruction opcode to a decimal value using base 3
	res = 0
	exp = 1
	for x in reversed(opcode):
		res += x * exp
		exp *= 3
	return res

def parseCode(instructions):
	# read from file
	file = sys.argv[1]
	f = open(file, "r")
	while True:
		instruction = f.read(4)
		if len(instruction) == 0:
			break
		if len(instruction) < 4:
			print("Error:{}".format(len(instructions)), file = sys.stderr)
			sys.exit(-1)
		instructions.append(translateInstruction(instruction))
	f.close()

	# check for [] corectness
	k = 0  # counts the number of [
	for i in range(len(instructions)):
		instruction = instructions[i]
		if instruction == L_BRACE:
			k += 1
		if instruction == R_BRACE:
			if k == 0:
				print("Error:{}".format(i), file = sys.stderr)
				sys.exit(-1)
			k -= 1
	if k > 0:
		print("Error:{}".format(len(instructions)), file = sys.stderr)
		sys.exit(-1)

	return 0

def checkInput(input, base):
	if base <= 10:
		max_char = ord('0') + base - 1
	else:
		max_char = ord('A') + base - 11

	for digit in input:
		if (not (digit >= '0' and digit <= '9') and 
				not (digit >= 'A' and digit <= 'Z') and
				digit != '-'):
			return False
		if ord(digit) > max_char:
			return False

	return True

def runInstruction(instruction, stack, i, instructions, base):
	stack_len = len(stack)

	if instruction == INPUT:
		x = input()
		if checkInput(x, base):
			stack.append(int(x, base))
		else:
			print("Exception:{}".format(i), file = sys.stderr)
			sys.exit(-2)

	elif instruction == ROT:
		if stack_len < 1:
			print("Exception:{}".format(i), file = sys.stderr)
			sys.exit(-2)

		x = stack.pop(-1)
		stack.insert(0, x)

	elif instruction == SWAP:
		if stack_len < 2:
			print("Exception:{}".format(i), file = sys.stderr)
			sys.exit(-2)

		x = stack[-1]
		stack[-1] = stack[-2]
		stack[-2] = x

	elif instruction == PUSH:
		stack.append(1)

	elif instruction == RROT:
		if stack_len < 1:
			print("Exception:{}".format(i), file = sys.stderr)
			sys.exit(-2)

		x = stack.pop(0)
		stack.append(x)

	elif instruction == DUP:
		if stack_len < 1:
			print("Exception:{}".format(i), file = sys.stderr)
			sys.exit(-2)

		stack.append(stack[-1])

	elif instruction == ADD:
		if stack_len < 2:
			print("Exception:{}".format(i), file = sys.stderr)
			sys.exit(-2)

		x = stack.pop(-1)
		y = stack.pop(-1)
		stack.append(x + y)

	elif instruction == L_BRACE:
		if stack_len < 1:
			print("Exception:{}".format(i), file = sys.stderr)
			sys.exit(-2)

		if stack[-1] == 0:
			k = 1  # number of [
			index = i
			while k != 0:
				i += 1
				if i >= len(instructions):
					print("Exception:{}".format(index), file = sys.stderr)
					sys.exit(-2)
				if instructions[i] == L_BRACE:
					k += 1
				elif instructions[i] == R_BRACE:
					k -= 1

	elif instruction == OUTPUT:
		if stack_len < 1:
			print("Exception:{}".format(i), file = sys.stderr)
			sys.exit(-2)

		x = stack.pop(-1)
		if base == 10:
			print(x)
		else:
			print(int2base(x, base))

	elif instruction == MULTIPLY:
		if stack_len < 2:
			print("Exception:{}".format(i), file = sys.stderr)
			sys.exit(-2)

		x = stack.pop(-1)
		y = stack.pop(-1)
		stack.append(x * y)

	elif instruction == EXECUTE:
		if stack_len < 4:
			print("Exception:{}".format(i), file = sys.stderr)
			sys.exit(-2)

		new_instruction = []
		for j in range(4):
			new_instruction.append(stack.pop(-1))
		i = runInstruction(translateInstruction(new_instruction), stack, i,
			instructions, base)

	elif instruction == NEGATE:
		if stack_len < 1:
			print("Exception:{}".format(i), file = sys.stderr)
			sys.exit(-2)

		stack[-1] *= -1

	elif instruction == POP:
		if stack_len < 1:
			print("Exception:{}".format(i), file = sys.stderr)
			sys.exit(-2)

		stack.pop(-1)

	elif instruction == R_BRACE:
		k = 1  # number of ]
		index = i
		while k != 0:
			i -= 1
			if i < 0:
				print("Exception:{}".format(index), file = sys.stderr)
				sys.exit(-2)
			if instructions[i] == R_BRACE:
				k += 1
			elif instructions[i] == L_BRACE:
				k -= 1
		i -= 1

	return i

def runProgram(instructions, base):
	stack = []
	i = 0
	l = len(instructions)
	while i < l:
		i = runInstruction(instructions[i], stack, i, instructions, base)
		i += 1

def main():
	if len(sys.argv) == 3:
		base = int(sys.argv[2])
	else:
		base = 10
	instructions = []
	parseCode(instructions)
	runProgram(instructions, base)

if __name__ == "__main__":
	main()