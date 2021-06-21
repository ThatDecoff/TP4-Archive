import pygame
from os import getcwd, path
from random import shuffle

class Button:
    sprites = ["Button_Sprite0.png", # Standby
               "Button_Sprite1.png", # Neutral
               "Button_Sprite2.png", # Flag
               "Button_Sprite3.png", # Bomb
               "Button_Sprite4.png", # Exploded
               "Button_Sprite5.png", # 1
               "Button_Sprite6.png",
               "Button_Sprite7.png",
               "Button_Sprite8.png",
               "Button_Sprite9.png",
               "Button_Sprite10.png",
               "Button_Sprite11.png",
               "Button_Sprite12.png"] # 8

    isActive = True
    isFlag = False
    
    adj = ["self.index+1", # index
            "self.index-1",
            "self.index-x", # index-x
            "self.index-x+1",
            "self.index-x-1",
            "self.index+x", # index+x
            "self.index+x+1",
            "self.index+x-1"]
                
    def __init__(self, x, y, i, bomb):
        global xButtons, yButtons
        self.swapSprite(0)
        self.imageBorder = self.imageSprite.get_rect()
        self.x = x
        self.y = y
        self.index = i
        self.xDraw = xButtons + x*16
        self.yDraw = yButtons + y*16
        self.isBomb = bomb
        self.adjCoord = [(self.x+1, self.y),
                        (self.x-1, self.y),
                        (self.x, self.y+1),
                        (self.x+1, self.y+1),
                        (self.x-1, self.y+1),
                        (self.x, self.y-1),
                        (self.x+1, self.y-1),
                        (self.x-1, self.y-1)]

    def __repr__(self):
        return f"Button object at({self.x}, {self.y})"

    def __str__(self):
        return f"(({self.x}, {self.y}), {self.index}, bomb = {self.isBomb})"

    def swapSprite(self, index):
        """ function for swapping the sprite of button """
        imagePath = path.join(getcwd(), "Assets",  self.sprites[index])
        self.imageSprite = pygame.image.load(imagePath)

    def draw(self, screen):
        """ function for drawing the button at predefined location """
        screen.blit(self.imageSprite, (self.xDraw, self.yDraw))

    def count(self):
        """ counts the amount of bombs in adjacent squares """
        global x, y
        count = 0
        for i in range(len(self.adj)):
            try:
                tmp = eval(self.adj[i])
                if ((buttonLst[tmp].x, buttonLst[tmp].y) in self.adjCoord):
                    if buttonLst[tmp].isBomb:
                        count += 1
            except IndexError:
                continue
        if count == 0:
            self.swapSprite(1)
            for i in range(len(self.adj)):
                try:
                    tmp = eval(self.adj[i])
                    if ((buttonLst[tmp].x, buttonLst[tmp].y) in self.adjCoord):
                        buttonLst[tmp].clicked("Click")
                except IndexError:
                    continue
        return count

    def clicked(self, event):
        """ a function that runs when a button is clicked.
            a Click event is a left click while
            a Flag event is a right click """
        global cooldown, tick
        if (event == "Flag"):
            if (cooldown <= 0):
                cooldown = tick//5
                if (self.isActive and (not self.isFlag)):
                    self.swapSprite(2)
                    self.isActive = False
                    self.isFlag = True
                elif ((not self.isActive) and self.isFlag):
                    self.swapSprite(0)
                    self.isActive = True
                    self.isFlag = False
        elif (event == "Click"):
            if self.isActive:
                self.isActive = False
                if self.isBomb:
                    self.swapSprite(4)
                    global defeat
                    defeat = True
                else:
                    count = self.count()
                    if (count > 0):
                        self.swapSprite(count+4)

def main():
    pygame.init()
    # Coordinates & Variables
    global x, y
    x = 16
    y = 16

    global xButtons, yButtons
    xButtons = 150
    yButtons = 50

    xScreen = x*16 + xButtons + yButtons
    yScreen = y*16 + yButtons + yButtons

    global cooldown, tick
    count = 0
    time = 900
    tick = 60
    cooldown = 0

    code = ""

    # Screens & clock
    screen = pygame.display.set_mode((xScreen, yScreen))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Buttons & Bombs
    bombCnt = (x*y)//4
    bombLst = [False for i in range(x*y)]
    bombLst[:bombCnt] = [True for i in range(bombCnt)]
    shuffle(bombLst)

    global buttonLst
    buttonLst = [Button(i%x, i//x, i,  bombLst[i]) for i in range(x*y)]

    # Game loop
    global game, defeat
    game = True
    defeat = False
    win = False
    cheat = False
    while game:
        # Begin step & exit code
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        # Cheat code input recognization
        if keys[pygame.K_h] and code == "":
            code = "H"
        elif keys[pygame.K_e] and code == "H":
            code = "HE"
        elif keys[pygame.K_s] and code == "HE":
            code = "HES"
        elif keys[pygame.K_o] and code == "HES":
            code = "HESO"
        elif keys[pygame.K_y] and code == "HESO":
            code = "HESOY"
        elif keys[pygame.K_a] and code == "HESOY":
            code = "HESOYA"
        elif keys[pygame.K_m] and code == "HESOYA":
            code = "HESOYAM"
            cheat = True

        # Step code
        mouse = pygame.mouse.get_pos()

        # Mouseclick check
        if ((xButtons < mouse[0] < xButtons+256) and
            (yButtons < mouse[1] < yButtons+256)):
            click = pygame.mouse.get_pressed()
            pos = (((mouse[0]-xButtons)//16) + ((mouse[1]-yButtons)//16)*x)
            if (click[2] == 1):
                buttonLst[pos].clicked("Flag")
            elif (click[0] == 1):
                buttonLst[pos].clicked("Click")

        # Defeated or cheating check
        if defeat or cheat:
            for i in range(x*y):
                if (buttonLst[i].isBomb and buttonLst[i].isActive):
                    buttonLst[i].swapSprite(3)
                    buttonLst[i].isActive = False
                    if cheat:
                        buttonLst[i].isFlag = True
                if defeat:
                    buttonLst[i].isActive = False

        # win check
        win = True
        for i in range(x*y):
            if ((not buttonLst[i].isBomb) and
                (buttonLst[i].isActive or buttonLst[i].isFlag)):
                win = False
                break
            elif (buttonLst[i].isBomb and (not buttonLst[i].isFlag)):
                win = False
                break
                
        # Draw code
        # Screen draw
        screen.fill((127, 127, 127))
        pygame.draw.rect(screen, (192, 192, 192),
                         (4, 4, xScreen-8, yScreen-8))
        pygame.draw.rect(screen, (225, 225, 225),
                         (xButtons-4, yButtons-4, 256+8, 256+8))
        # Time draw
        text = font.render("Time:", 1, (0, 0, 0))
        screen.blit(text, (40, 50))
        pygame.draw.rect(screen, (0, 0, 0),
                         (45, 90, 55, 35))
        text = font.render(f"{time}", 1, (255, 255, 255))
        screen.blit(text, (50, 95))
        # Cheat code draw
        text = font.render(f"{code}", 1, (255, 0, 255))
        screen.blit(text, (150, 15))
        # Button draw
        for i in range(x*y):
            buttonLst[i].draw(screen)
        # Conditional message draw
        if defeat:
            text = font.render("Game", 1, (255, 0, 0))
            screen.blit(text, (40, 150))
            text = font.render("Over", 1, (255, 0, 0))
            screen.blit(text, (40, 185))
        if win:
            text = font.render("You", 1, (0, 200, 0))
            screen.blit(text, (40, 150))
            text = font.render("Win!", 1, (0, 200, 0))
            screen.blit(text, (40, 185))
        pygame.display.flip()
        
        # End step code
        # Count is increased by 1 per frame
        count += 1
        # Reduce cooldown by 1 per frame
        if (cooldown > 0):
            cooldown -= 1
        # Reduce time by 1 per second
        if ((not defeat) and (not win)):
            if (count >= tick):
                time -= 1
                count = 0
        # If time reaches zero, player is defeated
        if (time <= 0):
            defeat = True
        clock.tick(tick)
    pygame.quit()

if __name__ == "__main__":
    main()
