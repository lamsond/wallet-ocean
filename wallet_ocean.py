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
CHILL_TIME = FPS*4
SINK_SOURCE_TIME = FPS*6
PHI = 1.618

#color constants
NIGHT = (11, 22, 33)
OCEAN = (0, 153, 202)

#game vars
water_height = int(WIN_HEIGHT/(PHI+1))
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
	img = pygame.transform.scale(img, (int(sf*w), int(sf*h)))
	return img

def draw_ocean(surf, x):
	surf.fill(OCEAN)
	n = int(WIN_WIDTH/WAVE_LENGTH)+3
	for i in range(n):
		pygame.draw.circle(surf, NIGHT, (WAVE_LENGTH*(i-1) + x, water_height), WAVE_RAD)
	pygame.draw.rect(surf, NIGHT, (0, 0, WIN_WIDTH, water_height))

def move_wave(x):
	if x > 0:
		x -= WAVE_SPEED
	else:
		x = WAVE_LENGTH
	return x

def update_water_height(y):
	global sink_count, sink_dir
	if sink_count >= SINK_SOURCE_TIME:
		sink_count = 0
		sink_dir = 0
	elif sink_count == CHILL_TIME:
		sink_dir = random.choice([-1, 0, 1])
		sink_count += 1
	else:
		sink_count += 1
	y += sink_dir
	return y

HAPPY_SQUID = init_image("SquidPink.png", 0.2)
CRAZY_SQUID = init_image("SquidOrange.png", 0.2)
GATOR_CORN = init_image("GatorCorn.png", 0.2)
SHARK = init_image("GatorCorn.png", 0.2)

class HappySquid():
	def __init__(self, x, y):
		self.img = HAPPY_SQUID
		self.x = x
		self.y = y
		self.dir_y = -1
		self.speed_x = 3
		self.speed_y = 5
		
	def draw(self, surf):
		surf.blit(self.img, (self.x, self.y))
	
	def move(self):
		if self.x < 0 - 50:
			self.x = WIN_WIDTH
		self.x -= self.speed_x
		if self.y > WIN_HEIGHT - 250 or self.y <= water_height+13:
			self.dir_y *= -1
		self.y += self.speed_y * self.dir_y
		
bob = HappySquid(WIN_WIDTH, WIN_HEIGHT/2)		
	
#game loop
while True:
	draw_ocean(screen, wave_x)
	bob.draw(screen)
	wave_x = move_wave(wave_x)
	water_height = update_water_height(water_height)
	bob.move()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
			
	pygame.display.update()
	clock.tick(FPS)

