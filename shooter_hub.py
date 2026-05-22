# main content of game

import pygame
import random
import sys
import os
import json

# ================= MAIN MENU =================

from plane_shooter import plane_home_screen, plane_game
from tank_shooter import tank_home_screen, tank_game

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Hub")

font_big = pygame.font.SysFont(None, 72)
font = pygame.font.SysFont(None, 36)

def main_menu():

    plane_btn = pygame.Rect(250, 250, 300, 70)
    tank_btn = pygame.Rect(250, 350, 300, 70)
    exit_btn = pygame.Rect(250, 450, 300, 70)

    while True:
        screen.fill((20, 20, 40))

        title = font_big.render("SELECT GAME", True, (255,255,255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))

        pygame.draw.rect(screen, (0,150,0), plane_btn)
        pygame.draw.rect(screen, (0,0,200), tank_btn)
        pygame.draw.rect(screen, (150,0,0), exit_btn)

        screen.blit(font.render("PLANE SHOOTER", True, (255,255,255)),
                    (plane_btn.centerx-90, plane_btn.centery-15))

        screen.blit(font.render("TANK SHOOTER", True, (255,255,255)),
                    (tank_btn.centerx-85, tank_btn.centery-15))

        screen.blit(font.render("EXIT", True, (255,255,255)),
                    (exit_btn.centerx-25, exit_btn.centery-15))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if plane_btn.collidepoint(event.pos):
                    plane_home_screen()
                    plane_game()

                if tank_btn.collidepoint(event.pos):
                    tank_home_screen()
                    tank_game()

                if exit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

main_menu()

# ================= RUN GAME =================
main_menu()

pygame.init()
pygame.mixer.init()

# ================= SCREEN =================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Shooter")
clock = pygame.time.Clock()

# ================= FONTS =================
font_big = pygame.font.SysFont(None, 72)
font = pygame.font.SysFont(None, 36)

# ================= SAVE FILE (JSON) =================
SAVE_FILE = "save_data.json"

def save_data():
    data = {
        "coins": coins,
        "owned_planes": owned_planes,
        "selected_plane": selected_plane
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    global coins, owned_planes, selected_plane

    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                coins = data.get("coins", 0)
                owned_planes = data.get("owned_planes", [0])
                selected_plane = data.get("selected_plane", 0)
        except:
            coins = 0
            owned_planes = [0]
            selected_plane = 0
    else:
        coins = 0
        owned_planes = [0]
        selected_plane = 0

# Load save
load_data()

# ================= ASSETS =================
ASSETS = "assets"

background_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS, "background1.png")).convert(),
    (WIDTH, HEIGHT)
)

plane_prices = [0,3000,4000,6000,8000,10000,12000,14000]

plane_imgs = []
plane_imgs.append(pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS, "player.png")).convert_alpha(), (60,60)
))

for i in range(2,9):
    img = pygame.image.load(os.path.join(ASSETS, f"plane{i}.png")).convert_alpha()
    plane_imgs.append(pygame.transform.scale(img, (60,60)))

enemy_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS, "enemy.png")).convert_alpha(), (50, 50)
)

boss_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS, "boss.png")).convert_alpha(), (100, 100)
)

final_boss_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS, "final_boss.png")).convert_alpha(), (160, 130)
)

bullet_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS, "bullet.png")).convert_alpha(), (15, 30)
)

enemy_bullet_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS, "enemy_bullet.png")).convert_alpha(), (15, 30)
)

boss_bullet_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS, "boss_bullet.png")).convert_alpha(), (20, 30)
)

explosion_frames = []
for i in range(1,5):
    img = pygame.image.load(os.path.join(ASSETS, f"explosion{i}.png")).convert_alpha()
    explosion_frames.append(pygame.transform.scale(img, (50,50)))

shoot_sound = pygame.mixer.Sound(os.path.join(ASSETS, "shoot.wav"))
explosion_sound = pygame.mixer.Sound(os.path.join(ASSETS, "explosion.wav"))

pygame.mixer.music.load(os.path.join(ASSETS, "music.mp3"))
pygame.mixer.music.play(-1)
# ================= EXPLOSION =================
class Explosion:
    def __init__(self, center):
        self.frames = explosion_frames
        self.index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=center)
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer % 5 == 0:
            self.index += 1
            if self.index < len(self.frames):
                self.image = self.frames[self.index]

    def draw(self):
        screen.blit(self.image, self.rect)

    def finished(self):
        return self.index >= len(self.frames)-1
# ================= STORE =================
def store_screen():
    global coins, selected_plane, owned_planes

    while True:
        screen.blit(background_img, (0,0))
        screen.blit(font_big.render("STORE", True, (255,255,0)), (300,30))
        screen.blit(font.render(f"Coins: {coins}", True, (255,255,255)), (10,10))

        buttons = []

        for i in range(8):
            x = 70 + (i%4)*180
            y = 150 + (i//4)*200
            screen.blit(plane_imgs[i], (x,y))

            if i in owned_planes:
                text = "OWNED"
                color = (0,255,0)
            else:
                text = f"{plane_prices[i]} Coins"
                color = (255,255,0)

            screen.blit(font.render(text, True, color), (x-10,y+70))

            btn = pygame.Rect(x-10,y+100,100,35)
            pygame.draw.rect(screen,(0,0,200),btn)
            screen.blit(font.render("SELECT",True,(255,255,255)),(btn.x+10,btn.y+5))

            buttons.append((btn, i))

        back = pygame.Rect(320,520,160,40)
        pygame.draw.rect(screen,(150,0,0),back)
        screen.blit(font.render("BACK",True,(255,255,255)),(360,525))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                save_data()
                pygame.quit(); sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                for btn, i in buttons:
                    if btn.collidepoint(e.pos):
                        if i in owned_planes:
                            selected_plane = i
                        elif coins >= plane_prices[i]:
                            coins -= plane_prices[i]
                            owned_planes.append(i)
                            selected_plane = i
                            save_data()

                if back.collidepoint(e.pos):
                    save_data()
                    return

# ================= HOME =================
def plane_home_screen():
    start = pygame.Rect(280,300,240,55)
    store = pygame.Rect(280,380,240,55)
    exitb = pygame.Rect(280,460,240,55)

    while True:
        screen.blit(background_img,(0,0))
        screen.blit(font_big.render("PLANE SHOOTER",True,(255,255,255)),(200,180))

        pygame.draw.rect(screen,(0,150,0),start)
        pygame.draw.rect(screen,(0,0,200),store)
        pygame.draw.rect(screen,(150,0,0),exitb)

        screen.blit(font.render("START",True,(255,255,255)),(360,315))
        screen.blit(font.render("STORE",True,(255,255,255)),(360,395))
        screen.blit(font.render("EXIT",True,(255,255,255)),(370,475))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if start.collidepoint(e.pos): return
                if store.collidepoint(e.pos): store_screen()
                if exitb.collidepoint(e.pos):
                    pygame.quit(); sys.exit()

# ================= GAME OVER =================
def game_over_screen(text):
    restart_btn = pygame.Rect(WIDTH//2 - 120, 330, 240, 55)
    exit_btn = pygame.Rect(WIDTH//2 - 120, 400, 240, 55)

    while True:
        screen.blit(background_img, (0, 0))
        msg = font_big.render(text, True, (255,0,0))
        screen.blit(msg, (WIDTH//2-msg.get_width()//2, 200))

        pygame.draw.rect(screen, (0,150,0), restart_btn)
        pygame.draw.rect(screen, (150,0,0), exit_btn)

        screen.blit(font.render("RESTART", True, (255,255,255)),
                    (restart_btn.centerx-55, restart_btn.centery-15))
        screen.blit(font.render("EXIT", True, (255,255,255)),
                    (exit_btn.centerx-30, exit_btn.centery-15))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    return
                if exit_btn.collidepoint(event.pos):
                    pygame.quit(); sys.exit()


# ================= GAME =================
def plane_game():
    global coins

    player_img_current = plane_imgs[selected_plane]
    player = player_img_current.get_rect(center=(400,500))
    player_health = 100
    score = 0

    bullets, enemies, ebullets, bbullets, explosions = [],[],[],[],[]

    boss = None
    boss_health = boss_max_health = 30
    boss_active = False
    second_phase = False
    final_boss = False
    extra_kills = 0

    bg1,bg2 = 0,-HEIGHT

    def enemy_spawn():
        r = enemy_img.get_rect()
        r.x = random.randint(0,WIDTH-r.width)
        r.y = -40
        return r

    def spawn_boss(final=False):
        img = final_boss_img if final else boss_img
        return img.get_rect(center=(WIDTH//2,80))

    while True:
        clock.tick(60)

        bg1+=2; bg2+=2
        if bg1>=HEIGHT: bg1=-HEIGHT
        if bg2>=HEIGHT: bg2=-HEIGHT
        screen.blit(background_img,(0,bg1))
        screen.blit(background_img,(0,bg2))

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                save_data()
                pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_SPACE:
                bullets.append(bullet_img.get_rect(midbottom=player.midtop))
                shoot_sound.play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left>0: player.x-=6
        if keys[pygame.K_RIGHT] and player.right<WIDTH: player.x+=6
        if keys[pygame.K_UP] and player.top>0: player.y-=6
        if keys[pygame.K_DOWN] and player.bottom<HEIGHT: player.y+=6

        if random.randint(1,50)==1 and not boss_active:
            enemies.append(enemy_spawn())

        for b in bullets[:]:
            b.y-=8
            if b.bottom<0: bullets.remove(b)

        for e in enemies[:]:
            e.y+=3
            if random.randint(1,100)==1:
                ebullets.append(enemy_bullet_img.get_rect(midtop=e.midbottom))
            for b in bullets[:]:
                if e.colliderect(b):
                    enemies.remove(e); bullets.remove(b)
                    explosions.append(Explosion(e.center))
                    explosion_sound.play()
                    score+=1; coins+=5
                    save_data()
                    if second_phase: extra_kills+=1
                    break

        for b in ebullets[:]:
            b.y+=5
            if b.colliderect(player):
                ebullets.remove(b); player_health-=10
            elif b.top>HEIGHT: ebullets.remove(b)

        if score>=10 and not boss_active and not second_phase:
            boss=spawn_boss(); boss_active=True

        if second_phase and extra_kills>=10 and not final_boss:
            boss=spawn_boss(True)
            boss_health=boss_max_health=50
            boss_active=True; final_boss=True

        if boss_active:
            boss.x+=random.choice([-4,4])
            boss.x=max(0,min(WIDTH-boss.width,boss.x))

            if random.randint(1,20)==1:
                bbullets.append(boss_bullet_img.get_rect(midtop=boss.midbottom))

            for b in bullets[:]:
                if b.colliderect(boss):
                    bullets.remove(b); boss_health-=1
                    explosions.append(Explosion(b.center))
                    explosion_sound.play()

            if boss_health<=0:
                explosions.append(Explosion(boss.center))
                explosion_sound.play()
                boss_active=False; boss=None

                if final_boss:
                    coins+=100
                    save_data()
                    game_over_screen("YOU WIN")
                    return

                coins+=50
                save_data()
                second_phase=True

            if boss:
                img = final_boss_img if final_boss else boss_img
                bar=int(boss.width*(boss_health/boss_max_health))
                pygame.draw.rect(screen,(255,0,0),(boss.x,boss.y-15,boss.width,10))
                pygame.draw.rect(screen,(0,255,0),(boss.x,boss.y-15,bar,10))
                screen.blit(img,boss)

        for b in bbullets[:]:
            b.y+=6
            if b.colliderect(player):
                bbullets.remove(b); player_health-=15
            elif b.top>HEIGHT: bbullets.remove(b)

        screen.blit(player_img_current,player)
        for e in enemies: screen.blit(enemy_img,e)
        for b in bullets: screen.blit(bullet_img,b)
        for b in ebullets: screen.blit(enemy_bullet_img,b)
        for b in bbullets: screen.blit(boss_bullet_img,b)

        for ex in explosions[:]:
            ex.update(); ex.draw()
            if ex.finished(): explosions.remove(ex)

        screen.blit(font.render(f"Health: {player_health}",True,(0,255,0)),(10,10))
        screen.blit(font.render(f"Score: {score}",True,(255,255,255)),(10,40))
        screen.blit(font.render(f"Coins: {coins}",True,(255,255,0)),(10,70))

        if player_health<=0:
            save_data()
            game_over_screen("GAME OVER")
            return

        pygame.display.update()


# tank shooter

pygame.init()
pygame.mixer.init()

# ================= SCREEN =================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Shooter")
clock = pygame.time.Clock()

# ================= FONTS =================
font_big = pygame.font.SysFont(None, 72)
font = pygame.font.SysFont(None, 36)

# ================= SAVE FILE (JSON) =================
SAVE_FILE = "save_data2.json"

def save_data2():
    data = {
        "coins": coins,
        "owned_tank": owned_tank,
        "selected_tank": selected_tank
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    global coins, owned_tank, selected_tank

    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                coins = data.get("coins", 0)
                owned_tank = data.get("owned_tank", [0])
                selected_tank = data.get("selected_tank", 0)
        except:
            coins = 0
            owned_tank = [0]
            selected_tank = 0
    else:
        coins = 0
        owned_tank = [0]
        selected_tank = 0

# Load save
load_data()

# ================= ASSETS =================
ASSET = "asset"

background_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSET, "background1.png")).convert(),
    (WIDTH, HEIGHT)
)

tank_prices = [0,3000,4000,6000,8000,10000,12000,14000]

tank_imgs = []
tank_imgs.append(pygame.transform.scale(
    pygame.image.load(os.path.join(ASSET, "player.png")).convert_alpha(), (60,60)
))

for i in range(2,9):
    img = pygame.image.load(os.path.join(ASSET, f"tank{i}.png")).convert_alpha()
    tank_imgs.append(pygame.transform.scale(img, (60,60)))

enemy_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSET, "enemy.png")).convert_alpha(), (50, 50)
)

boss_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSET, "boss.png")).convert_alpha(), (100, 100)
)

final_boss_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSET, "final_boss.png")).convert_alpha(), (160, 130)
)

bullet_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSET, "bullet.png")).convert_alpha(), (15, 30)
)

enemy_bullet_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSET, "enemy_bullet.png")).convert_alpha(), (15, 30)
)

boss_bullet_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSET, "boss_bullet.png")).convert_alpha(), (20, 30)
)

explosion_frames = []
for i in range(1,5):
    img = pygame.image.load(os.path.join(ASSET, f"explosion{i}.png")).convert_alpha()
    explosion_frames.append(pygame.transform.scale(img, (50,50)))

shoot_sound = pygame.mixer.Sound(os.path.join(ASSET, "shoot.wav"))
explosion_sound = pygame.mixer.Sound(os.path.join(ASSET, "explosion.wav"))

pygame.mixer.music.load(os.path.join(ASSET, "music.mp3"))
pygame.mixer.music.play(-1)
# ================= EXPLOSION =================
class Explosion:
    def __init__(self, center):
        self.frames = explosion_frames
        self.index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=center)
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer % 5 == 0:
            self.index += 1
            if self.index < len(self.frames):
                self.image = self.frames[self.index]

    def draw(self):
        screen.blit(self.image, self.rect)

    def finished(self):
        return self.index >= len(self.frames)-1
# ================= STORE =================
def store_screen():
    global coins, selected_tank, owned_tank

    while True:
        screen.blit(background_img, (0,0))
        screen.blit(font_big.render("STORE", True, (255,255,0)), (300,30))
        screen.blit(font.render(f"Coins: {coins}", True, (255,255,255)), (10,10))

        buttons = []

        for i in range(8):
            x = 70 + (i%4)*180
            y = 150 + (i//4)*200
            screen.blit(tank_imgs[i], (x,y))

            if i in owned_tank:
                text = "OWNED"
                color = (0,255,0)
            else:
                text = f"{tank_prices[i]} Coins"
                color = (255,255,0)

            screen.blit(font.render(text, True, color), (x-10,y+70))

            btn = pygame.Rect(x-10,y+100,100,35)
            pygame.draw.rect(screen,(0,0,200),btn)
            screen.blit(font.render("SELECT",True,(255,255,255)),(btn.x+10,btn.y+5))

            buttons.append((btn, i))

        back = pygame.Rect(320,520,160,40)
        pygame.draw.rect(screen,(150,0,0),back)
        screen.blit(font.render("BACK",True,(255,255,255)),(360,525))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                save_data2()
                pygame.quit(); sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                for btn, i in buttons:
                    if btn.collidepoint(e.pos):
                        if i in owned_tank:
                            selected_tank = i
                        elif coins >= tank_prices[i]:
                            coins -= tank_prices[i]
                            owned_tank.append(i)
                            selected_tank = i
                            save_data2()

                if back.collidepoint(e.pos):
                    save_data2()
                    return

# ================= HOME =================
def tank_home_screen():
    start = pygame.Rect(280,300,240,55)
    store = pygame.Rect(280,380,240,55)
    exitb = pygame.Rect(280,460,240,55)

    while True:
        screen.blit(background_img,(0,0))
        screen.blit(font_big.render("Tank SHOOTER",True,(255,255,255)),(200,180))

        pygame.draw.rect(screen,(0,150,0),start)
        pygame.draw.rect(screen,(0,0,200),store)
        pygame.draw.rect(screen,(150,0,0),exitb)

        screen.blit(font.render("START",True,(255,255,255)),(360,315))
        screen.blit(font.render("STORE",True,(255,255,255)),(360,395))
        screen.blit(font.render("EXIT",True,(255,255,255)),(370,475))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if start.collidepoint(e.pos): return
                if store.collidepoint(e.pos): store_screen()
                if exitb.collidepoint(e.pos):
                    pygame.quit(); sys.exit()

# ================= GAME OVER =================
def game_over_screen(text):
    restart_btn = pygame.Rect(WIDTH//2 - 120, 330, 240, 55)
    exit_btn = pygame.Rect(WIDTH//2 - 120, 400, 240, 55)

    while True:
        screen.blit(background_img, (0, 0))
        msg = font_big.render(text, True, (255,0,0))
        screen.blit(msg, (WIDTH//2-msg.get_width()//2, 200))

        pygame.draw.rect(screen, (0,150,0), restart_btn)
        pygame.draw.rect(screen, (150,0,0), exit_btn)

        screen.blit(font.render("RESTART", True, (255,255,255)),
                    (restart_btn.centerx-55, restart_btn.centery-15))
        screen.blit(font.render("EXIT", True, (255,255,255)),
                    (exit_btn.centerx-30, exit_btn.centery-15))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    return
                if exit_btn.collidepoint(event.pos):
                    pygame.quit(); sys.exit()


# ================= GAME =================
def tank_game():
    global coins

    player_img_current = tank_imgs[selected_tank]
    player = player_img_current.get_rect(center=(400,500))
    player_health = 100
    score = 0

    bullets, enemies, ebullets, bbullets, explosions = [],[],[],[],[]

    boss = None
    boss_health = boss_max_health = 30
    boss_active = False
    second_phase = False
    final_boss = False
    extra_kills = 0

    bg1,bg2 = 0,-HEIGHT

    def enemy_spawn():
        r = enemy_img.get_rect()
        r.x = random.randint(0,WIDTH-r.width)
        r.y = -40
        return r

    def spawn_boss(final=False):
        img = final_boss_img if final else boss_img
        return img.get_rect(center=(WIDTH//2,80))

    while True:
        clock.tick(60)

        bg1+=2; bg2+=2
        if bg1>=HEIGHT: bg1=-HEIGHT
        if bg2>=HEIGHT: bg2=-HEIGHT
        screen.blit(background_img,(0,bg1))
        screen.blit(background_img,(0,bg2))

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                save_data2()
                pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_SPACE:
                bullets.append(bullet_img.get_rect(midbottom=player.midtop))
                shoot_sound.play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left>0: player.x-=6
        if keys[pygame.K_RIGHT] and player.right<WIDTH: player.x+=6
        if keys[pygame.K_UP] and player.top>0: player.y-=6
        if keys[pygame.K_DOWN] and player.bottom<HEIGHT: player.y+=6

        if random.randint(1,50)==1 and not boss_active:
            enemies.append(enemy_spawn())

        for b in bullets[:]:
            b.y-=8
            if b.bottom<0: bullets.remove(b)

        for e in enemies[:]:
            e.y+=3
            if random.randint(1,100)==1:
                ebullets.append(enemy_bullet_img.get_rect(midtop=e.midbottom))
            for b in bullets[:]:
                if e.colliderect(b):
                    enemies.remove(e); bullets.remove(b)
                    explosions.append(Explosion(e.center))
                    explosion_sound.play()
                    score+=1; coins+=5
                    save_data2()
                    if second_phase: extra_kills+=1
                    break

        for b in ebullets[:]:
            b.y+=5
            if b.colliderect(player):
                ebullets.remove(b); player_health-=10
            elif b.top>HEIGHT: ebullets.remove(b)

        if score>=10 and not boss_active and not second_phase:
            boss=spawn_boss(); boss_active=True

        if second_phase and extra_kills>=10 and not final_boss:
            boss=spawn_boss(True)
            boss_health=boss_max_health=50
            boss_active=True; final_boss=True

        if boss_active:
            boss.x+=random.choice([-4,4])
            boss.x=max(0,min(WIDTH-boss.width,boss.x))

            if random.randint(1,20)==1:
                bbullets.append(boss_bullet_img.get_rect(midtop=boss.midbottom))

            for b in bullets[:]:
                if b.colliderect(boss):
                    bullets.remove(b); boss_health-=1
                    explosions.append(Explosion(b.center))
                    explosion_sound.play()

            if boss_health<=0:
                explosions.append(Explosion(boss.center))
                explosion_sound.play()
                boss_active=False; boss=None

                if final_boss:
                    coins+=100
                    save_data2()
                    game_over_screen("YOU WIN")
                    return

                coins+=50
                save_data2()
                second_phase=True

            if boss:
                img = final_boss_img if final_boss else boss_img
                bar=int(boss.width*(boss_health/boss_max_health))
                pygame.draw.rect(screen,(255,0,0),(boss.x,boss.y-15,boss.width,10))
                pygame.draw.rect(screen,(0,255,0),(boss.x,boss.y-15,bar,10))
                screen.blit(img,boss)

        for b in bbullets[:]:
            b.y+=6
            if b.colliderect(player):
                bbullets.remove(b); player_health-=15
            elif b.top>HEIGHT: bbullets.remove(b)

        screen.blit(player_img_current,player)
        for e in enemies: screen.blit(enemy_img,e)
        for b in bullets: screen.blit(bullet_img,b)
        for b in ebullets: screen.blit(enemy_bullet_img,b)
        for b in bbullets: screen.blit(boss_bullet_img,b)

        for ex in explosions[:]:
            ex.update(); ex.draw()
            if ex.finished(): explosions.remove(ex)

        screen.blit(font.render(f"Health: {player_health}",True,(0,255,0)),(10,10))
        screen.blit(font.render(f"Score: {score}",True,(255,255,255)),(10,40))
        screen.blit(font.render(f"Coins: {coins}",True,(255,255,0)),(10,70))

        if player_health<=0:
            save_data2()
            game_over_screen("GAME OVER")
            return

        pygame.display.update()

# run
while True:
    main_menu()
