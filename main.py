#Misc comments

import pygame
import time
import os
import random
from bitConversions import *

#File
file = "./pong2.c8"

#Storage
opcode = 0

memory = [0] * 4096 #4k memory
#0x000-0x1FF - Chip 8 interpreter (contains font set in emu)
#0x050-0x0A0 - Used for the built in 4x5 pixel font set (0-F)
#0x200-0xFFF - Program ROM and work RAM

V = [0] * 16 #fifteen registers
#carry = False #carry flag, sometimes called VF
I = 0 #Index register
pc = 0 #program counter
graphic = [0] * (64*32) #pixel array

delay = 0
sound = 0 #delay and sound timers

stack = [0] * 16 #stack
stackp = 0 #stack pointer

key = [False] * 16 #Key states

drawFlag = False #draw flag

#RNG
random.seed()

#cycle
cycleCount = 0

def main():
	global delay
	global sound
	global delay
	global sound
	global pc
	global I
	global V
	global cycleCount
	pass
	#Graphics
	#Input setup
	#Init system
	init()
	#Game load
	while True: #main emulation loop
		pass
		cycle()
		#Emulate cycle
		if cycleCount  == 60:
			#time.sleep(1)
			cycleCount = 0
		if drawFlag:
			pass #placeholder for drawing
		
def init():
	rom = open(file, 'rb')
	for i in range(0,os.path.getsize(file)):
		memory[512 + i] = ord(rom.read(1))

def cycle():
	pass	
	global delay
	global sound
	global pc
	global I
	global V
	global cycleCount 
	cycleCount += 1
	#Fetch
	opcode = (memory[pc] << 8) | memory[pc+1]
	#Decode
	#Execute, 3 step process
	print(hex(pc) + " " + hex(opcode))
	executeInst(opcode)
	#timer
	if delay != 0:
		delay = delay - 1
	if sound != 0:
		sound = sound - 1
	
def executeInst(opcode):
	#The first 4 most significant bits are the first indicator
	global delay
	global sound
	global pc
	global I
	global V
	
	def zero():
		global delay
		global sound
		global pc
		global I
		global V
		global stackp
		if (opcode & 0xFF) == 0xE0:
			pass #Clear the screen
		elif (opcode & 0xFF) == 0xEE:
			pass #return from a subroutine
			stackp -= stackp
			pc = stack[stackp]
		else:
			pass #0NNN the fuck does this do?
		pc = pc + 2
	def one():
		global delay
		global sound
		global pc
		global I
		global V
		pc = opcode & 0xfff #Jumps to a subroutine
	def two():
		global delay
		global sound
		global pc
		global I
		global V
		global stack
		global stackp
		stack[stackp] = pc
		stackp = stackp + 1
		pc = opcode & 0xfff
		pc = pc + 2
	def three():
		global delay
		global sound
		global pc
		global I
		global V
		if V[((opcode & 0xF00) >> 8)] == (opcode & 0xFF):
			pc = pc + 4
		else:
			pc = pc + 2
	def four():
		global delay
		global sound
		global pc
		global I
		global V
		if V[((opcode & 0xF00) >> 8)] != (opcode & 0xFF):
			pc = pc + 4
		else:
			pc = pc + 2
	def five():
		global delay
		global sound
		global pc
		global I
		global V
		if V[((opcode & 0xFF0) >> 4)] == V[((opcode & 0xFF0) >> 8)]:
			pc = pc + 4
		else:
			pc = pc + 2
	def six():
		global delay
		global sound
		global pc
		global I
		global V
		V[((opcode & 0xF00) >> 8)] = (opcode & 0xFF)
		pc = pc + 2
	def seven():
		global delay
		global sound
		global pc
		global I
		global V
		pass #7XNN add NN to VX
		V[((opcode & 0xF00) >> 8)] = 0xFF & (V[((opcode & 0xF00) >> 8)] + (opcode & 0xFF))
		pc = pc + 2
	def eight():
		global delay
		global sound
		global pc
		global I
		global V
		#Theres a bit of shit here
		if (opcode & 0xF) == 0x0:
			V[((opcode & 0XF00) >> 8)] = V[((opcode & 0XF0) >> 4)]
		if (opcode & 0xF) == 0x1:
			V[((opcode & 0XF00) >> 8)] = V[((opcode & 0XF0) >> 4)] | V[((opcode & 0XF00) >> 8)]
		if (opcode & 0xF) == 0x2:
			V[((opcode & 0XF00) >> 8)] = V[((opcode & 0XF0) >> 4)] & V[((opcode & 0XF00) >> 8)]
		if (opcode & 0xF) == 0x3:
			V[((opcode & 0XF00) >> 8)] = V[((opcode & 0XF0) >> 4)] ^ V[((opcode & 0XF00) >> 8)]
		if (opcode & 0xF) == 0x4:
			pass #Adds VY to VX. VF is set to 1 when there's a carry, and to 0 when there isn't.
			V[((opcode & 0XF00) >> 8)] = V[((opcode & 0XF00) >> 8)] + V[((opcode & 0XF0) >> 4)]
			if V[((opcode & 0XF00) >> 8)] > 0xff:
				V[0xf] = 1
				V[((opcode & 0XF00) >> 8)] = V[((opcode & 0XF00) >> 8)] & 0xff
			else:
				V[0xf] = 0
		if (opcode & 0xF) == 0x5:
			pass #VY is subtracted from VX. VF is set to 0 when there's a borrow, and 1 when there isn't.
			V[((opcode & 0XF00) >> 8)] = V[((opcode & 0XF00) >> 8)] - V[((opcode & 0XF0) >> 4)]
			if V[((opcode & 0XF00) >> 8)] < 0x0:
				V[0xf] = 1
				V[((opcode & 0XF00) >> 8)] = V[((opcode & 0XF00) >> 8)] & 0xff
			else:
				V[0xf] = 0
		if (opcode & 0xF) == 0x6:
			pass #Shifts VX right by one. VF is set to the value of the least significant bit of VX before the shift
			V[0xf] = V[((opcode & 0XF00) >> 8)] & 0b1
			V[((opcode & 0XF00) >> 8)] = V[((opcode & 0XF00) >> 8)] >> 1
		if (opcode & 0xF) == 0x7:
			pass #Sets VX to VY minus VX. VF is set to 0 when there's a borrow, and 1 when there isn't.
			V[((opcode & 0XF00) >> 8)] = V[((opcode & 0XF0) >> 4)] - V[((opcode & 0XF00) >> 8)]
			if V[((opcode & 0XF00) >> 8)] < 0x0:
				V[0xf] = 1
				V[((opcode & 0XF00) >> 8)] = V[((opcode & 0XF00) >> 8)] & 0xff
			else:
				V[0xf] = 0
			
		if (opcode & 0xF) == 0xE:
			pass #Shifts VX left by one. VF is set to the value of the most significant bit of VX before the shift
			V[0xf] = V[((opcode & 0XF00) >> 7)]
			V[((opcode & 0XF00) >> 8)] = V[((opcode & 0XF00) >> 8)] << 1
			V[((opcode & 0XF00) >> 8)] = V[((opcode & 0XF00) >> 8)] & 0xff
			
		pc = pc + 2
	def nine():
		global delay
		global sound
		global pc
		global I
		global V
		pass #Skips the next instruction if VX doesn't equal VY.
		if V[((opcode & 0xFF0) >> 4)] != V[((opcode & 0xFF0) >> 8)]:
			pc = pc + 4
		else:
			pc = pc + 2
	def A():
		global delay
		global sound
		global pc
		global I
		global V
		I = opcode & 0xFFF
		pc = pc + 2
	def B():
		global delay
		global sound
		global pc
		global I
		global V
		pass #Jumps to the address NNN plus V0.
		pc = (opcode & 0xfff) + V[0x0]
	def C():
		global delay
		global sound
		global pc
		global I
		global V
		pass #Sets VX to a random number, masked by NN.
		V[((opcode & 0xFF0) >> 8)] = random.randrange(0,255) & (opcode & 0xFF)
		pc = pc + 2
	def D():
		global delay
		global sound
		global pc
		global I
		global V
		pass #Too fucking long to put here
		pc = pc + 2
	def E():
		global delay
		global sound
		global pc
		global I
		global V
		if (opcode & 0xFF) == 0x9E:
			pass
		if (opcode & 0xFF) == 0xA1:
			pass
		pc = pc + 2
	def F(): #This has a fuckton
		global delay
		global sound
		global pc
		global I
		global V
		if (opcode & 0xFF) == 0x07:
			pass
			V[((opcode & 0xFF0) >> 8)] = delay
		if (opcode & 0xFF) == 0x0A:
			pass
			
		if (opcode & 0xFF) == 0x15:
			pass
			delay = V[((opcode & 0xFF0) >> 8)]
		if (opcode & 0xFF) == 0x18:
			pass
			sound = V[((opcode & 0xFF0) >> 8)]
		if (opcode & 0xFF) == 0x1E:
			pass
			I = I + V[((opcode & 0xFF0) >> 8)]
		if (opcode & 0xFF) == 0x29:
			pass
			
		if (opcode & 0xFF) == 0x33:
			pass
			#V[((opcode & 0xFF0) >> 8)] = VX
			memory[I] = int(V[((opcode & 0xFF0) >> 8)] /100)
			memory[I+1] = int(V[((opcode & 0xFF0) >> 8)]/10 % 10)
			memory[I+2] = int(V[((opcode & 0xFF0) >> 8)] % 10)
		if (opcode & 0xFF) == 0x55:
			pass
			for i in range (0,16):
				memory[I + i] = V[i]
		if (opcode & 0xFF) == 0x65:
			pass
			for i in range (0,16):
				V[i] = memory[I + i]
		pc = pc + 2
		
	#
	first = {	0x0 : zero,
				0x1 : one,
				0x2 : two,
				0x3 : three,
				0x4 : four,
				0x5 : five,
				0x6 : six,
				0x7 : seven,
				0x8 : eight,
				0x9 : nine,
				0xA : A,
				0xB : B,
				0XC : C,
				0xD : D,
				0xE : E,
				0xF : F,
			}
	first[opcode >> 12]()
	time.sleep(1/60)
	#

if __name__ == "__main__":
	main()