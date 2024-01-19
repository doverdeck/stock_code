# Import modules
import pygame
import math
import random
pygame.init()
# Initialize constants
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
yellow = (255, 255, 0)
boss=0
hits = 0
display_width = 800
display_height = 600
powerups=[]
powerups2=[]
powerups3=[]
boss_dir=0
player_size = 10
fd_fric = 0.5
bd_fric = 0.1
player_max_speed = 20
player_max_rtspd = 10
bullet_speed = 15
homing_speed =5
saucer_speed = 5
small_saucer_accuracy = 10 

# Make surface and display
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Asteroids")
timer = pygame.time.Clock()

# Import sound effects

# Create function to draw texts
def drawText(msg, color, x, y, s, center=True):
    screen_text = pygame.font.SysFont("Calibri", s).render(msg, True, color)
    if center: # center = true, the code below will run
        rect = screen_text.get_rect()
        rect.center = (x, y)
    else: #if center = false, the code below will run
        rect = (x, y)
    gameDisplay.blit(screen_text, rect)


# Create funtion to chek for collision
def isColliding(x, y, xTo, yTo, size):
        if x > xTo - size and x < xTo + size and y > yTo - size and y < yTo + size: #if collision occurs, true is returned.
            return True
        return False
           
# Create class asteroid
class Asteroid:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        if t == "Large": #creates the size of the "large" asteroid
            self.size = 30
        elif t == "Normal": #creates the size of the "normal" asteroid
            self.size = 20
        elif t=="Boss":
            self.size= 40
        else: #base asteroid size
            self.size = 10
        self.t = t

        # Make random speed and direction
        self.speed = random.uniform(1, (40 - self.size) * 4 / 15)
        self.dir = random.randrange(0, 360) * math.pi / 180
        print(self.dir)
        if boss==1 and self.t=="Boss":
            self.dir=math.atan2((player.y-self.y),(player.x-self.x))
            print(self.dir)
            self.speed=6

        # Make random asteroid sprites
        full_circle = random.uniform(18, 36)
        dist = random.uniform(self.size / 2, self.size)
        self.vertices = []
        while full_circle < 360:
            self.vertices.append([dist, full_circle])
            dist = random.uniform(self.size / 2, self.size)
            full_circle += random.uniform(18, 36)

    def updateAsteroid(self):
        # Move asteroid
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)
        # Checka for "wrapping"
        if self.x > display_width:
            self.x = 0
        elif self.x < 0:
            self.x = display_width
        elif self.y > display_height:
            self.y = 0
        elif self.y < 0:
            self.y = display_height

        # Draw asteroid
        for v in range(len(self.vertices)):
            if v == len(self.vertices) - 1:
                next_v = self.vertices[0]
            else:
                next_v = self.vertices[v + 1]
            this_v = self.vertices[v]
            pygame.draw.line(gameDisplay, white, (self.x + this_v[0] * math.cos(this_v[1] * math.pi / 180),
                                                  self.y + this_v[0] * math.sin(this_v[1] * math.pi / 180)),
                             (self.x + next_v[0] * math.cos(next_v[1] * math.pi / 180),
                              self.y + next_v[0] * math.sin(next_v[1] * math.pi / 180)))

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy
# Create class bullet
class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.dir = direction
        self.life = 30
    def updateBullet(self):
        self.x += bullet_speed * math.cos(self.dir * math.pi / 180)
        self.y += bullet_speed * math.sin(self.dir * math.pi / 180)

        # Drawing
        pygame.draw.circle(gameDisplay, white, (int(self.x), int(self.y)), 3)

        # Wrapping
        if self.x > display_width:
            self.x = 0
        elif self.x < 0:
            self.x = display_width
        elif self.y > display_height:
            self.y = 0
        elif self.y < 0:
            self.y = display_height
        self.life -= 1
class Homing_Missile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dir = boss_dir
        self.life = 100
    def updateBullet(self, player): 
        self.dir= math.degrees(math.atan2((player.y-self.y),(player.x-self.x)))
        self.x += homing_speed * math.cos(self.dir * math.pi / 180)
        self.y += homing_speed * math.sin(self.dir * math.pi / 180)

        # Drawing
        pygame.draw.polygon(gameDisplay, red, (rotate((self.x, self.y),(self.x-20,self.y-20),self.dir*math.pi/180), rotate((self.x, self.y),(self.x-20,self.y+20),self.dir*math.pi/180), rotate((self.x, self.y),(self.x-10,self.y+10),self.dir*math.pi/180), rotate((self.x, self.y),(self.x-20,self.y+10), self.dir*math.pi/180),rotate((self.x, self.y),(self.x+20,self.y+10), self.dir*math.pi/180), rotate((self.x, self.y),(self.x+40,self.y),self.dir*math.pi/180),rotate((self.x, self.y),(self.x+20,self.y-10), self.dir*math.pi/180),rotate((self.x, self.y),(self.x-10,self.y-10),self.dir*math.pi/180)))
        #rectangle=pygame.rect(gameDisplay, red, ((int(self.x)-37), int(self.y)-10, 40, 20))
        #picture=rectangle.get_rect()
        #pygame.transform.rotate(picture, self.dir)
        # Wrapping
        if self.x > display_width:
            self.x = 0
        elif self.x < 0:
            self.x = display_width
        elif self.y > display_height:
            self.y = 0
        elif self.y < 0:
            self.y = display_height
        self.life -= 1


# Create class saucer
class Saucer:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.state = "Dead"
        self.type = "Large"
        self.dirchoice = ()
        self.bullets = []
        self.cd = 0
        self.bdir = 0
        self.soundDelay = 0

    def updateSaucer(self):
        # Move player
        self.x += saucer_speed * math.cos(self.dir * math.pi / 180)
        self.y += saucer_speed * math.sin(self.dir * math.pi / 180)

        # Choose random direction
        if random.randrange(0, 100) == 1:
            self.dir = random.choice(self.dirchoice)

        # Wrapping
        if self.y < 0:
            self.y = display_height
        elif self.y > display_height:
            self.y = 0
        if self.x < 0 or self.x > display_width:
            self.state = "Dead"

        # Shooting
        if self.type == "Large":
            self.bdir = random.randint(0, 360)
        if self.cd == 0:
            self.bullets.append(Bullet(self.x, self.y, self.bdir))
            self.cd = 30
        else: 
            self.cd -= 1

        # Play SFX
        #if self.type == "Large":
        #else:

    def createSaucer(self):
        # Create saucer
        # Set state
        self.state = "Alive"

        # Set random position
        self.x = random.choice((0, display_width))
        self.y = random.randint(0, display_height)

        if boss!=1:
        # Set random type
            if random.randint(0, 1) == 0:
                self.type = "Large"
                self.size = 20
            else:
                self.type = "Small"
                self.size = 10
        else:
            self.size=150
       

        # Create random direction
        if self.x == 0:
            self.dir = 0
            self.dirchoice = (0, 45, -45)
        else:
            self.dir = 180
            self.dirchoice = (180, 135, -135)

        # Reset bullet cooldown
        self.cd = 0

    def drawSaucer(self):
        # Draw saucer
        pygame.draw.polygon(gameDisplay, white,
                            ((self.x + self.size, self.y),
                             (self.x + self.size / 2, self.y + self.size / 3),
                             (self.x - self.size / 2, self.y + self.size / 3),
                             (self.x - self.size, self.y),
                             (self.x - self.size / 2, self.y - self.size / 3),
                             (self.x + self.size / 2, self.y - self.size / 3)), 1)
        pygame.draw.line(gameDisplay, white,
                         (self.x - self.size, self.y),
                         (self.x + self.size, self.y))
        pygame.draw.polygon(gameDisplay, white,
                            ((self.x - self.size / 2, self.y - self.size / 3),
                             (self.x - self.size / 3, self.y - 2 * self.size / 3),
                             (self.x + self.size / 3, self.y - 2 * self.size / 3),
                             (self.x + self.size / 2, self.y - self.size / 3)), 1)


# Create class for shattered ship
class deadPlayer:
    def __init__(self, x, y, l):
        self.angle = random.randrange(0, 360) * math.pi / 180
        self.dir = random.randrange(0, 360) * math.pi / 180
        self.rtspd = random.uniform(-0.25, 0.25)
        self.x = x
        self.y = y
        self.lenght = l
        self.speed = random.randint(2, 8)

    def updateDeadPlayer(self):
        pygame.draw.line(gameDisplay, white,
                         (self.x + self.lenght * math.cos(self.angle) / 2,
                          self.y + self.lenght * math.sin(self.angle) / 2),
                         (self.x - self.lenght * math.cos(self.angle) / 2,
                          self.y - self.lenght * math.sin(self.angle) / 2))
        self.angle += self.rtspd
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)
# Class player
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hspeed = 0
        self.vspeed = 0
        self.dir = 270
        self.rtspd = 0
        self.thrust = False

    def updatePlayer(self):
        # Move player
        speed = math.sqrt(self.hspeed**2 + self.vspeed**2)
        if self.thrust:
            if speed + fd_fric < player_max_speed:
                self.hspeed += fd_fric * math.cos(self.dir * math.pi / 180)
                self.vspeed += fd_fric * math.sin(self.dir * math.pi / 180)
            else:
                self.hspeed = player_max_speed * math.cos(self.dir * math.pi / 180)
                self.vspeed = player_max_speed * math.sin(self.dir * math.pi / 180)
        else:
            if speed - bd_fric > 0:
                change_in_hspeed = (bd_fric * math.cos(self.vspeed / self.hspeed))
                change_in_vspeed = (bd_fric * math.sin(self.vspeed / self.hspeed))
                if self.hspeed != 0:
                    if change_in_hspeed / abs(change_in_hspeed) == self.hspeed / abs(self.hspeed):
                        self.hspeed -= change_in_hspeed
                    else:
                        self.hspeed += change_in_hspeed
                if self.vspeed != 0:
                    if change_in_vspeed / abs(change_in_vspeed) == self.vspeed / abs(self.vspeed):
                        self.vspeed -= change_in_vspeed
                    else:
                        self.vspeed += change_in_vspeed
            else:
                self.hspeed = 0
                self.vspeed = 0
        self.x += self.hspeed
        self.y += self.vspeed

        # Check for wrapping
        if self.x > display_width:
            self.x = 0
        elif self.x < 0:
            self.x = display_width
        elif self.y > display_height:
            self.y = 0
        elif self.y < 0:
            self.y = display_height

        # Rotate player
        self.dir += self.rtspd

    def drawPlayer(self):
        a = math.radians(self.dir)
        x = self.x
        y = self.y
        s = player_size
        t = self.thrust
        # Draw player
        pygame.draw.line(gameDisplay, white,
                         (x - (s * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) + a),
                          y - (s * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) + a)),
                         (x + s * math.cos(a), y + s * math.sin(a)))

        pygame.draw.line(gameDisplay, white,
                         (x - (s * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) - a),
                          y + (s * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) - a)),
                         (x + s * math.cos(a), y + s * math.sin(a)))

        pygame.draw.line(gameDisplay, white,
                         (x - (s * math.sqrt(2) / 2) * math.cos(a + math.pi / 4),
                          y - (s * math.sqrt(2) / 2) * math.sin(a + math.pi / 4)),
                         (x - (s * math.sqrt(2) / 2) * math.cos(-a + math.pi / 4),
                          y + (s * math.sqrt(2) / 2) * math.sin(-a + math.pi / 4)))
        if t:
            pygame.draw.line(gameDisplay, white,
                             (x - s * math.cos(a),
                              y - s * math.sin(a)),
                             (x - (s * math.sqrt(5) / 4) * math.cos(a + math.pi / 6),
                              y - (s * math.sqrt(5) / 4) * math.sin(a + math.pi / 6)))
            pygame.draw.line(gameDisplay, white,
                             (x - s * math.cos(-a),
                              y + s * math.sin(-a)),
                             (x - (s * math.sqrt(5) / 4) * math.cos(-a + math.pi / 6),
                              y + (s * math.sqrt(5) / 4) * math.sin(-a + math.pi / 6)))
    def killPlayer(self):
        # Reset the player
        self.x = display_width / 2
        self.y = display_height / 2
        self.thrust = False
        self.dir = -90
        self.hspeed = 0
        self.vspeed = 0
class Powerup:
    def __init__(self, x, y):
        print("ok")
        self.x=x
        self.y=y
        print(f"{self.x} {self.y}")
    def updatePowerUp(self):
        pygame.draw.circle(gameDisplay, red, (int(self.x), int(self.y)), 20)
class Powerup2:
    def __init__(self, x, y):
        self.x=x
        self.y=y
    def updatePowerUp2(self):
        pygame.draw.circle(gameDisplay, blue, (int(self.x), int(self.y)), 20)
    def drawShield(player):
        pygame.draw.circle(gameDisplay, blue, (int(player.x), int(player.y)), 20)
class Powerup3:
    def __init__(self, x, y):
        self.x=x
        self.y=y
    def updatePowerUp3(self):
        pygame.draw.circle(gameDisplay, green, (int(self.x), int(self.y)), 20)
class Powerup4:
    def __init__(self, x, y):
        self.x=x
        self.y=y
    def updatePowerUp4(self):
        pygame.draw.circle(gameDisplay, yellow, (int(self.x), int(self.y)), 20)

def gameLoop(startingState):
    global boss
    global boss_dir
    # Init variables
    asteroid_spawn=0
    homing_spawn=0
    counter=0
    boss=0
    boss_dir=0
    remove_boolean=0
    gameState = startingState
    player_state = "Alive"
    player_blink = 0
    player_pieces = []
    player_dying_delay = 0
    player_invi_dur = 0
    power_up_dur= 0
    power_up_dur2=0
    power_up_dur4=0
    hyperspace = 0
    next_level_delay = 0
    bullet_capacity = 4
    powerups=[]
    powerups2=[]
    powerups3=[]
    powerups4=[]
    bullets = []
    homing_missiles= []
    asteroids = []
    stage = 3
    score = 0
    live = 2
    oneUp_multiplier = 1
    playOneUpSFX = 0
    intensity = 0
    global player
    player = Player(display_width / 2, display_height / 2)
    saucer = Saucer()

    # Main loop
    while gameState != "Exit":
        # Game menu
        while gameState == "Menu":
            gameDisplay.fill(black)
            drawText("ASTEROIDS", white, display_width / 2, display_height / 2, 100)
            drawText("Press any key to START", white, display_width / 2, display_height / 2 + 100, 50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState = "Exit"
                if event.type == pygame.KEYDOWN:
                    gameState = "Playing"
            pygame.display.update()
            timer.tick(5)

        # User inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "Exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.thrust = True
                if event.key == pygame.K_LEFT:
                    player.rtspd = -player_max_rtspd
                if event.key == pygame.K_RIGHT:
                    player.rtspd = player_max_rtspd
                if event.key == pygame.K_SPACE and player_dying_delay == 0 and len(bullets) < bullet_capacity:
                    bullets.append(Bullet(player.x, player.y, player.dir))
                    if (counter==1):
                        bullets.append(Bullet(player.x, player.y, player.dir+45))
                        bullets.append(Bullet(player.x, player.y, player.dir-45))
                    # Play SFX
                if gameState == "Game Over":
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop("Playing")
                if event.key == pygame.K_LSHIFT:
                    hyperspace = 30
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.thrust = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.rtspd = 0

        # Update player
        player.updatePlayer()

        # Checking player invincible time
        if player_invi_dur != 0:
            player_invi_dur -= 1
        elif hyperspace == 0:
            player_state = "Alive"
        
        if power_up_dur !=0:
            power_up_dur -=1
        elif power_up_dur ==0:
            counter=0
        if power_up_dur4 !=0:
            power_up_dur4 -=1
        elif power_up_dur4 ==0:
            bullet_capacity=4
        def bossAsteroid():
            if (boss==1):
                print("bam")
                asteroids.append(Asteroid(saucer.x, saucer.y, "Boss"))
        def bossMissile():
            if (boss==1):
                print("bop")
                homing_missiles.append(Homing_Missile(saucer.x, saucer.y))
        if (asteroid_spawn==0):
            boss_dir=math.degrees(math.atan2((player.x-saucer.x),(player.y-saucer.y)))
            print("boss_dir")
            bossAsteroid()
            asteroid_spawn=100
        else:
            asteroid_spawn=asteroid_spawn-1 
        if (homing_spawn==0):
            bossMissile()
            homing_spawn=120
        else:
            homing_spawn=homing_spawn-1 
        # Reset display  
        gameDisplay.fill(black)
        if power_up_dur2 !=0:
            power_up_dur2-=1
            Powerup2.drawShield(player)
        elif power_up_dur2 ==0:
            pass
        for p in powerups:
            p.updatePowerUp()
            if (isColliding(player.x, player.y, p.x, p.y, 22)):
                counter=1
                power_up_dur=120
                powerups.remove(p)
        for p in powerups2:
            p.updatePowerUp2()
            if (isColliding(player.x, player.y, p.x, p.y, 22)):
                player_state = "Died"
                player_invi_dur=1000
                power_up_dur2=1000
                powerups2.remove(p)
        for p in powerups3:
            p.updatePowerUp3()
            if (isColliding(player.x, player.y, p.x, p.y, 22)):
                live+=1
                powerups3.remove(p)
        for p in powerups4:
            p.updatePowerUp4()
            if (isColliding(player.x, player.y, p.x, p.y, 22)):
                power_up_dur4=120
                bullet_capacity=1000
                powerups4.remove(p)
        # Hyperspace
        if hyperspace != 0:
            player_state = "Died"
            hyperspace -= 1
            if hyperspace == 1:
                player.x = random.randrange(0, display_width)
                player.y = random.randrange(0, display_height)
        # Check for collision w/ asteroid
        for a in asteroids:
            a.updateAsteroid()
            if player_state != "Died":
                if isColliding(player.x, player.y, a.x, a.y, a.size):
                    # Create ship fragments
                    player_pieces.append(deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_pieces.append(deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_pieces.append(deadPlayer(player.x, player.y, player_size))

                    # Kill player
                    player_state = "Died"
                    player_dying_delay = 30
                    player_invi_dur = 120
                    player.killPlayer()

                    if live != 0:
                        live -= 1
                    else:
                        counter=0
                        gameState = "Game Over"

                    # Split asteroid
                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        score += 20
                        if score > 5000:
                         boss = 1
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        score += 50
                        if score > 5000:
                         boss = 1
                    else:
                        score += 100
                        if score > 5000:
                         boss = 1
                    asteroids.remove(a)

        # Update ship fragments
        for f in player_pieces:
            f.updateDeadPlayer()
            if f.x > display_width or f.x < 0 or f.y > display_height or f.y < 0:
                player_pieces.remove(f)
        # Check for end of stage
        if (boss!=1):
            if len(asteroids) == 0 and saucer.state == "Dead":
                if next_level_delay < 30:
                    next_level_delay += 1
                else:
                    stage += 1
                    intensity = 0
                    # Spawn asteroid away of center
                    for i in range(stage):
                        xTo = display_width / 2
                        yTo = display_height / 2
                        while xTo - display_width / 2 < display_width / 4 and yTo - display_height / 2 < display_height / 4:
                            xTo = random.randrange(0, display_width)
                            yTo = random.randrange(0, display_height)
                        asteroids.append(Asteroid(xTo, yTo, "Large"))
                    next_level_delay = 0
        else:
            if (remove_boolean==0):
                remove_boolean=1
                for a in asteroids:
                    asteroids.remove(a)
                saucer.state=="Dead"
                saucer.createSaucer()
        # Update intensity
        if intensity < stage * 450:
            intensity += 1

        # Saucer
        if saucer.state == "Dead":
            if random.randint(0, 6000) <= (intensity * 2) / (stage * 9) and next_level_delay == 0:
                saucer.createSaucer()
                # Only small saucers >40000
                if (boss!=1):
                    if score >= 40000:
                        saucer.type = "Small"
                else:
                    saucer.type="Boss"
        else:
            # Set saucer targer dir
            acc = small_saucer_accuracy * 4 / stage
            saucer.bdir = math.degrees(math.atan2(-saucer.y + player.y, -saucer.x + player.x) + math.radians(random.uniform(acc, -acc)))

            saucer.updateSaucer()
            saucer.drawSaucer()
            
            # Check for collision w/ asteroid
            if (boss!=1):
                for a in asteroids:
                    if isColliding(saucer.x, saucer.y, a.x, a.y, a.size + saucer.size):
                        # Set saucer state
                        saucer.state = "Dead"

                        # Split asteroid
                        if a.t == "Large":
                            asteroids.append(Asteroid(a.x, a.y, "Normal"))
                            asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        # Play SFX
                        elif a.t == "Normal":
                            asteroids.append(Asteroid(a.x, a.y, "Small"))
                            asteroids.append(Asteroid(a.x, a.y, "Small"))
                        # Play SFX
                        else:
                            continue
                        # Play SFX
                        asteroids.remove(a)
            # Check for collision w/ bullet
            for b in bullets:
                if isColliding(b.x, b.y, saucer.x, saucer.y, saucer.size):
                    # Add points
                    if saucer.type == "Large":
                        score += 200
                        if score > 3000:
                            boss = 1
                    elif saucer.type == "Small":
                        score += 1000
                        if score > 3000:
                            boss = 1
                    else:
                        score == 0

                    # Set saucer state
                    if (boss!=1):
                        saucer.state = "Dead"
                    global hits
                    if (boss==1):
                        if (hits<40):
                            hits=hits+1
                                #asteroids.append(Asteroid(saucer.x, saucer.y, "Large"))
                            print(saucer.state)
                            score == 0
                        elif (hits==40):
                            saucer.state="Dead"
                            hits=0
                            score += 2000
                            gameState = "Game Over"
                    # Play SFX

                    # Remove bullet
                    bullets.remove(b)

            # Check collision w/ player
            if isColliding(saucer.x, saucer.y, player.x, player.y, saucer.size):
                if player_state != "Died":
                    # Create ship fragments
                    player_pieces.append(deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_pieces.append(deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                    player_pieces.append(deadPlayer(player.x, player.y, player_size))

                    # Kill player
                    player_state = "Died"
                    player_dying_delay = 30
                    player_invi_dur = 120
                    player.killPlayer()

                    if live != 0:
                        live -= 1
                    else:
                        counter=0
                        gameState = "Game Over"

                    # Play SFX
            # Saucer's bullets
            for b in saucer.bullets:
                # Update bullets
                b.updateBullet()

                # Check for collision w/ asteroids
                for a in asteroids:
                    if isColliding(b.x, b.y, a.x, a.y, a.size):
                        # Split asteroid
                        if a.t == "Large":
                            asteroids.append(Asteroid(a.x, a.y, "Normal"))
                            asteroids.append(Asteroid(a.x, a.y, "Normal"))
                            # Play SFX
                        elif a.t == "Normal":
                            asteroids.append(Asteroid(a.x, a.y, "Small"))
                            asteroids.append(Asteroid(a.x, a.y, "Small"))
                            # Play SF
                        else:
                            continue
                            # Play SFX

                        # Remove asteroid and bullet
                        asteroids.remove(a)
                        saucer.bullets.remove(b)

                        break
                # Check for collision w/ player
                if isColliding(player.x, player.y, b.x, b.y, 5):
                    if player_state != "Died":
                        # Create ship fragments
                        player_pieces.append(deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                        player_pieces.append(deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                        player_pieces.append(deadPlayer(player.x, player.y, player_size))

                        # Kill player
                        player_state = "Died"
                        player_dying_delay = 30
                        player_invi_dur = 120
                        player.killPlayer()

                        if live != 0:
                            live -= 1
                        else:
                            counter=0
                            gameState = "Game Over"

                        # Play SFX

                        # Remove bullet
                        saucer.bullets.remove(b)

                if b.life <= 0:
                    try:
                        saucer.bullets.remove(b)
                    except ValueError:
                        continue
        for b in homing_missiles:
                # Update bullets
                b.updateBullet(player)

                # Check for collision w/ asteroids
                for a in asteroids:
                    if isColliding(b.x, b.y, a.x, a.y, a.size):
                        # Split asteroid
                        if a.t == "Large":
                            asteroids.append(Asteroid(a.x, a.y, "Normal"))
                            asteroids.append(Asteroid(a.x, a.y, "Normal"))
                            # Play SFX
                        elif a.t == "Normal":
                            asteroids.append(Asteroid(a.x, a.y, "Small"))
                            asteroids.append(Asteroid(a.x, a.y, "Small"))
                            # Play SF
                        else:
                            continue
                            # Play SFX

                        # Remove asteroid and bullet
                        asteroids.remove(a)
                        homing_missiles.remove(b)

                        break
                # Check for collision w/ player
                if isColliding(player.x, player.y, b.x, b.y, 27):
                    if player_state != "Died":
                        # Create ship fragments
                        player_pieces.append(deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                        player_pieces.append(deadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3)))))
                        player_pieces.append(deadPlayer(player.x, player.y, player_size))

                        # Kill player
                        player_state = "Died"
                        player_dying_delay = 30
                        player_invi_dur = 120
                        player.killPlayer()

                        if live != 0:
                            live -= 1
                        else:
                            counter=0
                            gameState = "Game Over"

                        # Play SFX

                        # Remove bullet
                        homing_missiles.remove(b)

                if b.life <= 0:
                    try:
                        homing_missiles.remove(b)
                    except ValueError:
                        continue
        # Bullets
        for b in bullets:
            # Update bullets
            b.updateBullet()

            # Check for bullets collide w/ asteroid
            for a in asteroids:
                if b.x > a.x - a.size and b.x < a.x + a.size and b.y > a.y - a.size and b.y < a.y + a.size:
                    # Split asteroid
                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        score += 20
                        if (random.randint(0, 10)==10):
                            powerups.append(Powerup(a.x,a.y))
                        if (random.randint(0, 10)==10):
                            powerups2.append(Powerup2(a.x,a.y))
                        if (random.randint(0, 10)==10):
                            powerups3.append(Powerup3(a.x,a.y))
                        if (random.randint(0, 10)==10):
                            powerups4.append(Powerup4(a.x,a.y))
                        if score > 3000:
                            boss=1
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        score += 50
                        if (random.randint(0, 10)==10):
                            powerups.append(Powerup(a.x,a.y))
                        if (random.randint(0, 10)==10):
                            powerups2.append(Powerup2(a.x,a.y))
                        if (random.randint(0, 10)==10):
                            powerups3.append(Powerup3(a.x,a.y))
                        if (random.randint(0, 10)==10):
                            powerups4.append(Powerup4(a.x,a.y))
                        if score > 3000:
                            boss = 1
                    else:
                        print("huh")
                        if (random.randint(0, 10)==10):
                            powerups.append(Powerup(a.x,a.y))
                        if (random.randint(0, 10)==10):
                            powerups2.append(Powerup2(a.x,a.y))
                        if (random.randint(0, 10)==10):
                            powerups3.append(Powerup3(a.x,a.y))
                        if (random.randint(0, 10)==10):
                            powerups4.append(Powerup4(a.x,a.y))
                        score += 100
                        if score > 3000:
                            boss = 1
                    asteroids.remove(a)
                    bullets.remove(b)

                    break

            # Destroying bullets
            if b.life <= 0:
                try:
                    bullets.remove(b)
                except ValueError:
                    continue
        # Extra live
        if score > oneUp_multiplier * 10000:
            oneUp_multiplier += 1
            live += 1
            playOneUpSFX = 60
        # Play sfx
        if playOneUpSFX > 0:
            playOneUpSFX -= 1

        # Draw player
        if gameState != "Game Over":
            if player_state == "Died":
                if hyperspace == 0:
                    if player_dying_delay == 0:
                        if player_blink < 5:
                            if player_blink == 0:
                                player_blink = 10
                            else:
                                player.drawPlayer()
                        player_blink -= 1
                    else:
                        player_dying_delay -= 1
            else:
                player.drawPlayer()
        elif live < 1 and gameState == "Game Over":
            drawText("Game Over", white, display_width / 2, display_height / 2, 100)
            drawText("Press \"R\" to restart!", white, display_width / 2, display_height / 2 + 100, 50)
            live = -1
        else:
            drawText("YOU WIN!!!", white, display_width / 2, display_height / 2, 100)
            drawText("Press \"R\" to Play again!", white, display_width / 2, display_height / 2 + 100, 50)
            saucer.state="Dead"
            boss == 0
            score == 0
             

        # Draw score
        drawText(str(score), white, 60, 20, 40, False)

        # Draw Lives
        for l in range(live + 1):
            Player(75 + l * 25, 75).drawPlayer()

        # Update screen
        pygame.display.update()

        # Tick fps
        timer.tick(30)

# Start game
gameLoop("Menu")

# End game
pygame.quit()
quit()