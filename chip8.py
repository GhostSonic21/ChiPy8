import time
import os
import random

class Chip8:
	# Properties of the chip 8
	memory = [0] * 4096
	V = [0] * 16
	i = 0
	pc = 0x200 			# Program counter starts a ROM space
	graphic = [[0] * 64 for i in range(36)]
	delay = 0
	sound = 0
	stack = [0] * 16
	stackp = 0 			# Stack pointer to keep track of where we are in the stack
	key = [False] * 16 	# For storing key states
	drawFlag = False 	# Set to true if the screen needs to be drawn
	
	random.seed() 		# Needed for generating random numbers
	
	cycleCount = 0 		# Mostly for debugging

	# The following is the Chip 8 Font set. Pre-programmed graphics for numbers and letters
	fontSet = [0xF0, 0x90, 0x90, 0x90, 0xF0, 
	  0x20, 0x60, 0x20, 0x20, 0x70, 
	  0xF0, 0x10, 0xF0, 0x80, 0xF0, 
	  0xF0, 0x10, 0xF0, 0x10, 0xF0, 
	  0x90, 0x90, 0xF0, 0x10, 0x10, 
	  0xF0, 0x80, 0xF0, 0x10, 0xF0, 
	  0xF0, 0x80, 0xF0, 0x90, 0xF0, 
	  0xF0, 0x10, 0x20, 0x40, 0x40, 
	  0xF0, 0x90, 0xF0, 0x90, 0xF0, 
	  0xF0, 0x90, 0xF0, 0x10, 0xF0,
	  0xF0, 0x90, 0xF0, 0x90, 0x90, 
	  0xE0, 0x90, 0xE0, 0x90, 0xE0, 
	  0xF0, 0x80, 0x80, 0x80, 0xF0, 
	  0xE0, 0x90, 0x90, 0x90, 0xE0, 
	  0xF0, 0x80, 0xF0, 0x80, 0xF0, 
	  0xF0, 0x80, 0xF0, 0x80, 0x80]
	
	def __init__(self, fileName):
		self.fileName = fileName
		# Load font set into memory
		for i in range(0,80):
			self.memory[i] = self.fontSet[i]			
		# Load rom into memory
		rom = open(fileName, 'rb')
		for i in range(0,os.path.getsize(fileName)):
			self.memory[512 + i] = ord(rom.read(1))
		rom.close()
	
	def cycle(self, key):
		if self.cycleCount == 60:
			self.cycleCount = 0
		
		self.cycleCount += 1
		self.key = key
		opcode = (self.memory[self.pc] << 8) | self.memory[self.pc+1] 	# opcodes are always 2bytes large
		self.executeInst(opcode)
		if self.delay != 0:
			self.delay -= 1
		if self.sound != 0:
			self.sound -= 1
		
	def executeInst(self, opcode):
		# Constants
		VX = (opcode & 0xF00) >> 8
		VY = (opcode & 0xF0)  >> 4
		first = opcode >> 12	# Most significant byte
		
		if first == 0x0:
			if (opcode & 0xFF) == 0xE0:
				self.graphic = [[0] * 64 for i in range(32)]
				self.drawFlag = True
			elif (opcode & 0xFF) == 0xEE:
				self.stackp -= 1
				self.pc = self.stack[self.stackp]
			self.pc = self.pc + 2
		if first == 0x1:
			self.pc = opcode & 0xfff	# Jumps to a point
		if first == 0x2:
			self.stack[self.stackp] = self.pc
			self.stackp += 1
			self.pc = opcode & 0xfff
		if first == 0x3:
			if self.V[VX] == (opcode & 0xFF):
				self.pc = self.pc + 4
			else:
				self.pc = self.pc + 2
		if first == 0x4:
			if self.V[VX] != (opcode & 0xFF):
				self.pc = self.pc + 4
			else:
				self.pc = self.pc + 2
		if first == 0x5:
			if self.V[VY] == self.V[VX]:
				self.pc = self.pc + 4
			else:
				self.pc = self.pc + 2
		if first == 0x6:
			self.V[VX] = (opcode & 0xFF)
			self.pc = self.pc + 2
		if first == 0x7:
			 # 7XNN add NN to VX
			self.V[VX] = (self.V[VX] + (opcode & 0xFF)) & 0xFF
			self.pc = self.pc + 2
		if first == 0x8:
			if (opcode & 0xF) == 0x0:
				self.V[VX] = self.V[VY]
			if (opcode & 0xF) == 0x1:
				self.V[VX] = self.V[VY] | self.V[VX]
			if (opcode & 0xF) == 0x2:
				self.V[VX] = self.V[VY] & self.V[VX]
			if (opcode & 0xF) == 0x3:
				self.V[VX] = self.V[VY] ^ self.V[VX]
			if (opcode & 0xF) == 0x4:
				self.V[VX] = self.V[VX] + self.V[VY]
				if self.V[VX] > 0xff:
					self.V[0xf] = 1
					self.V[VX] = self.V[VX] & 0xff
				else:
					self.V[0xf] = 0
			if (opcode & 0xF) == 0x5:
				self.V[VX] = self.V[VX] - self.V[VY]
				if self.V[VX] < 0x0:
					self.V[0xf] = 0
					self.V[VX] = self.V[VX] & 0xff
				else:
					self.V[0xf] = 1
			if (opcode & 0xF) == 0x6:
				self.V[0xf] = self.V[VX] & 0b1
				self.V[VX] = self.V[VX] >> 1
			if (opcode & 0xF) == 0x7:
				self.V[VX] = self.V[VY] - self.V[VX]
				if self.V[VX] < 0x0:
					self.V[0xf] = 0
					self.V[VX] = self.V[VX] & 0xff
				else:
					self.V[0xf] = 1
				
			if (opcode & 0xF) == 0xE:
				self.V[0xf] = self.V[VX] >> 7
				self.V[VX] = self.V[VX] << 1
				self.V[VX] = self.V[VX] & 0xff
				
			self.pc = self.pc + 2
		if first == 0x9:
			if self.V[VX] != self.V[VY]:
				self.pc = self.pc + 4
			else:
				self.pc = self.pc + 2
		if first == 0xa:
			self.I = opcode & 0xFFF
			self.pc = self.pc + 2
		if first == 0xb:
			self.pc = (opcode & 0xfff) + self.V[0x0]
		if first == 0xc:
			self.V[VX] = (random.randrange(0,255)) & (opcode & 0xFF)
			self.pc = self.pc + 2
		if first == 0xd:
			x = self.V[VX]
			y = self.V[VY]
			height = opcode & 0xF
			self.V[0Xf] = 0
			for yline in range (0,height):
				pixelState = self.memory[self.I+yline]
				for xline in range(0,8):
					if(pixelState & (0x80 >> xline)) != 0:
						if self.graphic[(y + yline)][(x + xline)] == 1:
							self.V[0xF] = 1
						self.graphic[(y + yline)][(x + xline)] ^= 1
						
			self.drawFlag = True
			self.pc = self.pc + 2
		if first == 0xe:
			if (opcode & 0xFF) == 0x9E:
				if self.key[self.V[VX]] == 1:
					self.pc += 4
				else:
					self.pc += 2
			if (opcode & 0xFF) == 0xA1:
				if self.key[self.V[VX]] != 1:
					self.pc += 4
				else:
					self.pc += 2
		if first == 0xf: 
			if (opcode & 0xFF) == 0x07:
				self.V[VX] = self.delay
			if (opcode & 0xFF) == 0x0A:
				keyPress = False
				for i in range(0,16):
					if self.key[i] != 0:
						self.V[VX] = i
						keyPress = True
				if not keyPress:
					return
			if (opcode & 0xFF) == 0x15:
				self.delay = self.V[VX]
			if (opcode & 0xFF) == 0x18:
				self.sound = self.V[VX]
			if (opcode & 0xFF) == 0x1E:
				self.I = self.I + self.V[VX]
				if self.I > 0xffff:
					self.I = self.I & 0xffff
					self.V[0xf] = 1
				else:
					self.V[0xf] = 0
			if (opcode & 0xFF) == 0x29:
				self.I = (self.V[VX] * 0x5) & 0xffff
			if (opcode & 0xFF) == 0x33:
				self.memory[self.I] = int(self.V[VX] /100) & 0xff
				self.memory[self.I+1] = int(self.V[VX]/10 % 10) & 0xff
				self.memory[self.I+2] = int(self.V[VX] % 10) & 0xff
			if (opcode & 0xFF) == 0x55:
				for i in range (0,VX+1):
					self.memory[self.I + i] = self.V[i]
			if (opcode & 0xFF) == 0x65:
				for i in range (0,VX+1):
					self.V[i] = self.memory[self.I + i]
				self.I = (self.I + VX + 1) & 0xFFFF
			self.pc = self.pc + 2