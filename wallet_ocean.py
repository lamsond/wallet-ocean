#Cora's Wallet Ocean
import pygame, sys, random

#game constants
WIN_WIDTH = 987
WIN_HEIGHT = 610
FPS = 30
WAVE_RAD = 30
WAVE_FACTOR = 1.6
WAVE_SPEED = 1
WAVE_LENGTH = int(WAVE_RAD * WAVE_FACTOR)
SINK_SOURCE_TIME = FPS*2

#color constants
NIGHT = (11, 22, 33)
OCEAN = (0, 153, 202)

#game vars
water_height = 100
wave_x = 0
sink_count = 0
sink_dir = 0

#init game time and space
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Cora's Wallet Ocean")
clock = pygame.time.Clock()

#return image to given scale
def init_image(path, sf):
	img = pygame.image.load(path)
	(w, h) = img.get_size()
	img = pygame.image.transform(int(sf*w), int(sf*h))
	return img

def draw_ocean(surf, x):
	surf.fill(OCEAN)
	n = int(WIN_WIDTH/WAVE_LENGTH)+3
	for i in range(n):
		pygame.draw.circle(surf, NIGHT, (WAVE_LENGTH*(i-1) + x, water_height), WAVE_RAD)
	pygame.draw.rect(surf, NIGHT, (0, 0, WIN_WIDTH, water_height))

def move_wave(x):
	if x < WAVE_LENGTH:
		x += WAVE_SPEED
	else:
		x = 0
	return x

def update_water_height(y):
	global sink_count, sink_dir
	if sink_count == SINK_SOURCE_TIME:
		sink_count = 0
		sink_dir = random.choice([-1, 0, 1])
	else:
		sink_count += 1
	y += sink_dir
	return y
	
#game loop
while True:
	draw_ocean(screen, wave_x)
	wave_x = move_wave(wave_x)
	water_height = update_water_height(water_height)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
			
	pygame.display.update()
	clock.tick(FPS)

