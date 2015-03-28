# Misc comments
import chip8
import pygame
import time
from tkinter import filedialog, Tk

# File
root = Tk()
root.withdraw()
file = filedialog.askopenfilename(filetypes = [('Chip 8 ROM', '.c8'), ('All files','.*')])

# Key array
key = [False] * 16

def main():
	# Set up Pygame
	chip8Display = pygame.Surface([64,32])								# Display surface
	display_array = pygame.PixelArray(chip8Display)						# Array for manipulating the pixels
	mainDisplay = pygame.display.set_mode([320,160])					# Actual display window, 4x native size
	
	# Create the Chip 8 object
	system = chip8.Chip8(file)
	
	while True:	# Main loop		
		pygame.event.pump()
		keyStates = pygame.key.get_pressed()
		key[0x1] = keyStates[pygame.K_1]
		key[0x2] = keyStates[pygame.K_2]
		key[0x3] = keyStates[pygame.K_3]
		key[0xc] = keyStates[pygame.K_4]
		key[0x4] = keyStates[pygame.K_q]
		key[0x5] = keyStates[pygame.K_w]
		key[0x6] = keyStates[pygame.K_e]
		key[0xd] = keyStates[pygame.K_r]
		key[0x7] = keyStates[pygame.K_a]
		key[0x8] = keyStates[pygame.K_s]
		key[0x9] = keyStates[pygame.K_d]
		key[0xe] = keyStates[pygame.K_f]
		key[0xa] = keyStates[pygame.K_z]
		key[0x0] = keyStates[pygame.K_x]
		key[0xb] = keyStates[pygame.K_c]
		key[0xf] = keyStates[pygame.K_v]
		system.cycle(key)
		if system.drawFlag:
			for i in range(0,32):
				for j in range(0,64):
					if system.graphic[i][j]:
						display_array[j,i] = 0xffffff
					else:
						display_array[j,i] = 0x0
			pygame.transform.scale(chip8Display, (320,160), mainDisplay)	# Scales up the chip 8 display and puts it to the main display
			pygame.display.update()
			
if __name__ == "__main__":
	main()