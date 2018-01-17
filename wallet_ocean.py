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
CHILL_TIME = 120 #let water height unchanged
SINK_SOURCE_TIME = 180 #raise or lower time
PHI = 1.618 #golden ratio
MAX_WATER_HEIGHT = -15
MIN_WATER_HEIGHT = WIN_HEIGHT/2 - 100 
SHARK_THRESHOLD = 30 #triggers shark_bait mode
COLOR_FRAMES = 5 #how often color updates
WATER_HEIGHT_CHOICES = [-1, 0, 1]
COLOR_CHANGE_CHOICES = [-2, -1, 0, 1, 2]
GROWTH_RATE = 0.2
COIN_RADIUS = 20
COIN_ACCEL = 0.1
COIN_SINK_SPEED = 2

#rgb color constants
NIGHT = (11, 22, 33)
OCEAN = (0, 153, 202)
BLOOD_OCEAN = (153, 0, 49)
GOLD = (240, 220, 20)
BLACK = (0, 0, 0)

#game vars
water_height = int(WIN_HEIGHT/(PHI+1))
wave_x = 0
sink_count = 0
sink_dir = 0
water_color = OCEAN
shark_bait = False
color_count = 0
happy_birth = 300
crazy_birth = 10 * happy_birth
scary_birth = 60
squid_count = 0
shark_count = 0
coin_count = 0
coin_birth = FPS*5

#init game spacetime
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Cora's Wallet Ocean")
clock = pygame.time.Clock()
font_obj = pygame.font.Font('freesansbold.ttf', 24)

#return image to given file path and scale factor
def init_image(path, sf):
	img = pygame.image.load(path)
	(w, h) = img.get_size()
	img = pygame.transform.scale(img, (int(sf*w), int(sf*h)))
	return img

#game images
HAPPY_SQUID = init_image("SquidPink.png", 0.18)
CRAZY_SQUID = init_image("SquidOrange.png", 0.18)
GATOR_CORN = init_image("GatorCorn.png", 0.65)
SHARK = init_image("SharkGrey.png", 0.65)
CORA = init_image("CoraAlpha.png", 0.34)

#draw waves and night sky
def draw_ocean(surf, x, clr):
	surf.fill(clr)
	n = int(WIN_WIDTH/WAVE_LENGTH)+3
	for i in range(n):
		pygame.draw.circle(surf, NIGHT, (WAVE_LENGTH*(i-1) + x, water_height), WAVE_RAD)
	pygame.draw.rect(surf, NIGHT, (0, 0, WIN_WIDTH, water_height))

#creates scrolling wave effect
def move_wave(x):
	if x > 0:
		x -= WAVE_SPEED
	else:
		x = WAVE_LENGTH
	return x

#randomized water height
def update_water_height(y):
	global sink_count, sink_dir
	if sink_count >= SINK_SOURCE_TIME:
		sink_count = 0
		sink_dir = 0
	elif sink_count == CHILL_TIME:
		if water_height < MAX_WATER_HEIGHT:
			sink_dir = 1
		elif water_height > MIN_WATER_HEIGHT:
			sink_dir = -1
		else:
			sink_dir = random.choice(WATER_HEIGHT_CHOICES)
		sink_count += 1
	else:
		sink_count += 1
	y += sink_dir
	return y
	
#randomized water color and shark bait trigger
def update_water_color(clr):
	global shark_bait
	reset = False
	r = random.choice(COLOR_CHANGE_CHOICES)
	if shark_bait and clr[0] < BLOOD_OCEAN[0]:
		r = 1
	elif shark_bait and clr[0] >= BLOOD_OCEAN[0]:
		r = -1
		shark_bait = False
		reset = True
	elif not shark_bait and clr[0] <= OCEAN[0]+1:
		r = 1
	elif not shark_bait and clr[0] >= SHARK_THRESHOLD:
		r = 1
		shark_bait = True
	red = clr[0]+r
	green = clr[1]-r
	blue = clr[2]-r
	new_color = (red, green, blue)
	if reset:
		new_color = OCEAN
	return new_color

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
		if shark_bait:
			self.x += 2*self.speed_x
		else:
			self.x -= self.speed_x
			if self.y > WIN_HEIGHT - 200:
				self.dir_y = -1
			if self.y <= water_height:
				self.dir_y = 1
			self.y += self.speed_y * self.dir_y

class CrazySquid():
	def __init__(self, x, y):
		self.img = CRAZY_SQUID
		self.x = x
		self.y = y
		self.dir_y = -1
		self.speed_x = 3
		self.speed_y = 5
		
	def draw(self, surf):
		surf.blit(self.img, (self.x, self.y))
	
	def move(self):
		if shark_bait:
			self.x += 2*self.speed_x
		else:
			self.x += self.speed_x * random.choice([-4, -3, -2, -1, 0])
			if self.y > WIN_HEIGHT - 200:
				self.dir_y = -1
			if self.y <= water_height:
				self.dir_y = 1
			self.y += random.choice([2, 4, 8]) * self.dir_y
			
class Shark():
	def __init__(self, y):
		self.img = SHARK
		self.x = random.choice([-7500, -7000, -6500, -6000, -5500])
		self.y = y
		self.speed_x = 21
		
	def draw(self, surf):
		surf.blit(self.img, (self.x, self.y))
	
	def move(self):
		self.x += self.speed_x

class GatorCorn():
	def __init__(self, x, y):
		self.img = SHARK
		self.x = x
		self.y = y
		self.dir_y = 1
		self.speed_x = 13
		self.speed_y = 5
		
	def draw(self, surf):
		surf.blit(self.img, (self.x, self.y))
	
	def move(self):
		if self.x >= WIN_WIDTH + 500:
			self.x = -6000
		else:
			self.x += self.speed_x
		
		
class Cora():
	def __init__(self, x, y):
		self.img = CORA
		self.x = x
		self.y = y
		self.speed_x = -1
		
	def draw(self, surf):
		surf.blit(self.img, (self.x, self.y))
	
	def move(self):
		self.x += self.speed_x
		
def calc_coin_speed(coin, t):
		if coin.y <= water_height:
			return int(0.5*COIN_ACCEL*t**2)
		else:
			return COIN_SINK_SPEED
		
class Coin():
	def __init__(self):
		self.x = random.randint(0, WIN_WIDTH)
		self.y = -COIN_RADIUS
		self.speed_x = -1
		self.drop_time = 0
		self.speed_y = 0
		self.value = random.choice([1, 5, 10, 25, 50])
	
	def draw(self, surf):
		pygame.draw.circle(surf, GOLD, (self.x, self.y), COIN_RADIUS)
		text_surf = font_obj.render(str(self.value), True, BLACK, GOLD)
		text_rect = text_surf.get_rect()
		text_rect.center = (self.x, self.y)
		surf.blit(text_surf, text_rect)
		
	def move(self):
		self.x += self.speed_x
		self.drop_time += 1
		speed_y = calc_coin_speed(self, self.drop_time)
		self.y += speed_y

squids = []
sharks = []
coins = []
cora = Cora(int(WIN_WIDTH/2), 400)

#game loop
while True:
	draw_ocean(screen, wave_x, water_color)
	for coin in coins:
		if coin.y >= WIN_HEIGHT + COIN_RADIUS:
			coins.remove(coin)
		coin.draw(screen)
		coin.move()
	for squid in squids:
		if squid.x <= -100:
			squids.remove(squid)
		squid.draw(screen)
		squid.move()
	for shark in sharks:
		if shark.x >= 6000:
			sharks.remove(shark)
		shark.draw(screen)
		shark.move()
	cora.draw(screen)
	wave_x = move_wave(wave_x)
	water_height = update_water_height(water_height)
	if color_count >= COLOR_FRAMES:
		water_color = update_water_color(water_color)
		color_count = 0
	else:
		color_count += 1
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
			
	pygame.display.update()
	if coin_count >= coin_birth:
		coins.append(Coin())
		coin_birth = max(int(FPS/2), coin_birth - 1)
		coin_count = -1
	coin_count += 1
	if squid_count == crazy_birth:
		squids.append(CrazySquid(WIN_WIDTH, random.randint(water_height, WIN_HEIGHT)))
		squid_count = -1
		crazy_birth = max(int(crazy_birth * (1-GROWTH_RATE)), FPS*3)
		happy_birth = max(int(happy_birth * (1-GROWTH_RATE)), FPS*2)
	elif squid_count % happy_birth == 0:
		squids.append(HappySquid(WIN_WIDTH, random.randint(water_height, WIN_HEIGHT)))
	squid_count += 1
	if shark_bait and len(sharks) < 2:
		sy = (water_height+53, WIN_HEIGHT-150)
		sharks.append(Shark(sy[len(sharks)%2]))
	
	keys = pygame.key.get_pressed()
	if keys[pygame.K_RIGHT]:
		cora.x += 5
	elif keys[pygame.K_LEFT] and cora.x > 0:
		cora.x -= 6
	elif cora.x > 0:
		cora.x -= 1
	if keys[pygame.K_DOWN]:
		cora.y += 5
	elif keys[pygame.K_UP] and cora.y > water_height:
		cora.y -= 6
	elif cora.y > water_height:
		cora.y -= 1
		
	clock.tick(FPS)

