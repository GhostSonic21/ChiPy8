import pygame
import time

def main():
	display = pygame.display.set_mode([64,32])
	display_array = pygame.PixelArray(display)
	
	for i in range(0,32):
			for j in range(0,64):
				display_array[j, i] = 0xffffff
	while 1:
		pygame.event.pump()
		pygame.display.update()
				
if __name__ == "__main__":
	main()