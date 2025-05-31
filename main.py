import pygame, sys, math
from pygame.locals import QUIT
from random import choice, randint

class Aim(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()

    self.position = (75, 170)
    
    self.image = pygame.image.load('Graphics/Crosshair.png').convert_alpha()
    self.rect = self.image.get_rect(center = self.position)

    self.click1 = False
    self.click2 = False

    self.right_movement = True
    self.up_movement = True

  def movement(self):
    global speed, speedDebuff # Global variable which can be changed for higher levels.
    if speedDebuff:
      speed = 9
    else:
      speed = 7
    if self.click1: # Checks if mouse button has been clicked.
      if self.rect.x < 700 and self.rect.x > 100: # ensures sprite stops between 100 and 700 x positions and not off screen.
        self.rect.x += 0
    else: # Mouse button not clicked.
      if self.right_movement: # Sprite is moving right.
          if self.rect.right < 100: # Checks if sprite hits 100 x position.
              self.right_movement = False
          self.rect.x -= speed # Moves the sprite's x position.
      else: # Sprite is moving left.
          if self.rect.left > 700: # Checks if sprite hits 700 x position
              self.right_movement = True
          self.rect.x += speed # Moves the sprite's X position.

    if self.click2: # Checks if mouse button has been clicked twice.
      if self.rect.y < 190 and self.rect.y > 45: # Checks if y position is between 190 and 45.
        self.rect.y += 0 # Stops the sprite.
    else: # Mouse button has not been clicked for a second time.
      if self.click1: # Checks if mouse button has been clicked once.
        if self.up_movement: # Checks if sprite is moving up.
          if self.rect.bottom < 45: # checks if sprite has hit the the top y position.
            self.up_movement = False # changes variable to move sprite down.
          self.rect.y -= speed # Moves Sprite upwards.
        else:
          if self.rect.bottom > 190: # checks if sprite has hit the bottom y position.
            self.up_movement = True # changes variable to move sprite up.
          self.rect.y += speed # Moves Sprite downwards.

  def playerInput(self):
    # Player input Function
    down = pygame.MOUSEBUTTONDOWN
    keys = pygame.mouse.get_pressed(num_buttons=3)
    if down:
      # makes constant true if left mouse button is cliked.
      if keys[0] and not self.click1:
        self.click1 = True
      # makes second constant true if right mouse button is clicked.
      if keys[2] and self.click1:    
        self.click2 = True
  def outputPosition(self):
    # Adds crosshair position to a global array
    global target_pos
    if self.click2:
      target_pos.append(self.rect.center)
      
  def hitbox(self):
    #hitbox detection/where the player has aimed.
    global placement
    x = self.rect.center[0]
    y = self.rect.center[1]
    if self.click2:
      if x >= 158 and x <= 333 and y >= 20 and y <= 105:
        placement.append("TL")
      elif x >= 158 and x <= 333 and y >= 100 and y <= 185:
        placement.append("BL")
      elif x > 333 and x < 466 and y >= 20 and  y <= 188:
        placement.append("M")
      elif x >= 466 and x <= 641 and y >= 100 and y <= 185:
        placement.append("BR")
      elif x >= 466 and x <= 641 and y >= 20 and y <= 105:
        placement.append("TR")
      else:
        placement.append("OUT")

  def reset(self):
    global placement, target_pos, aim_reset
    # This function returns the crosshair to its original position after a shot.
    if aim_reset:
      self.click1 = False
      self.click2 = False
      self.up_movement = True
      self.right_movement = True
      placement.clear()
      target_pos.clear()
      self.rect.x = 75
      self.rect.y = 145
      
  def update(self):
    self.playerInput()
    self.movement()
    self.outputPosition()
    self.hitbox()
    self.reset()

class Ball(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
   
    self.position = (400,400)
    
    self.image = pygame.image.load('Graphics/Ball.png').convert_alpha()
    self.image = pygame.transform.rotozoom(self.image,0,0.5) # Resizes the image
    self.rect = self.image.get_rect(center = self.position) # positions the ball at the spot

  def animate(self):
    # Global array used to receive position of crosshair.
    global target_pos, ball_check, ball_reset, speedBoost
    if not ball_reset:
      if target_pos:
        # X and Y coordinates split into 2 different variables.
        self.target_x_pos = (target_pos[0])[0]
        self.target_y_pos = (target_pos[0])[1]
        x_speed = []
        y_speed = []
  
        # Distance in X and Y coordinates between ball and crosshair.
        y = ((self.target_y_pos - 25) - self.rect.y)
        x = ((self.target_x_pos - 25) - self.rect.x)

        if ball_reset:
          x = 0
          y = 0
          x_speed.clear()
          y_speed.clear()
          target_pos.clear()
        
        # Makes the speed 0 if the distance is 0.
        if y == 0 or x == 0 or ball_reset:
          y_speed.append(0)
          x_speed.append(0)
          ball_check = True
        else:
          # The speed is gained using the speed distance and time equation, setting time as 5 seconds and distance already set on line 92 and 93.
          if speedBoost:
            y_speed.append(y/2)
            x_speed.append(x/2)
          else:  
            y_speed.append(y/5)
            x_speed.append(x/5)
          
        # Logic behind the ball movement.
        if self.rect.x != (self.target_x_pos - 25): # Checks if the ball x positon has not reached the crosshair.
          if ball_reset: # checks if ball needs resetting
            self.rect.x += 0 # ball speed is 0
          self.rect.x += x_speed[0] # Moves the ball x position towards the crosshair x position.
        elif self.rect.x <= (self.target_x_pos - 25): # Need to - 52 as the ball x position is not the center x position whereas the crosshair x position is the center.
          self.rect.x += 0 # Stops the ball x position from moving if the position is the same.
        ball_check = True
  
        if self.rect.y != (self.target_y_pos - 25): # Checks if the ball y position has not reached the crosshair.
            if y_speed[0] < 0: # Checks if the y speed is less than 0.
              self.rect.y += y_speed[0] # Moves the y coordinates.
            else:
              self.rect.y -= y_speed[0] # Moves the y coordinates.
        elif self.rect.y <= (self.target_y_pos - 25):
          if ball_reset: # checks if ball needs resetting
            self.rect.y += 0 # Ball speed is 0
          self.rect.y -=0 # Stops the ball y position from moving if the position is the same
        ball_check = True
          
  def reset(self):
    # This function returns the ball to its original position after a shot.
    global ball_reset, target_pos
    if ball_reset:
      self.rect.x = 375
      self.rect.y = 380
      if target_pos:
        target_pos.clear()
      
      if self.rect.x == 375 and self.rect.y == 380:
        ball_reset = False

  def buffCollision(self):
    global ball_check, buffCollided, debuffCollided
    if ball_check:
      if pygame.sprite.groupcollide(ball ,buff, False, False):
        buffCollided = True
        print("buffCollided")
      if pygame.sprite.groupcollide(ball, debuff, False, False):
        debuffCollided = True
        print("debuffCollided")
  
  def update(self):
    self.animate()
    self.reset()
    self.buffCollision()
class Keeper(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
  
    keeperIdle = pygame.image.load('Graphics/BG Middle.png').convert_alpha()
    keeperSide = pygame.image.load('Graphics/BG Sideways.png').convert_alpha()
    keeperSide = pygame.transform.rotate(keeperSide,0)
    self.keeper = [keeperIdle,keeperSide]
    self.keeper_index = 0

    self.image = self.keeper[self.keeper_index]
    self.rect = self.image.get_rect(midbottom = (400,190))
    self.guess = []

    self.check = False

  def position(self):
    global score, placement, score_check, goalBoost, speedBoost, goalDebuff, speed
    self.guess.append(choice(["BL","BR","M","BL","TL"]))
    if placement:
      if placement[0]:
        if self.guess:
          if not self.check:
            if speedBoost and (placement[0] != "OUT"):
              score += 1
              score_check = "Goal"
            elif (self.guess[0] != placement[0]) and (placement[0] != "OUT"):
              if goalBoost:
                score += 2
              elif goalDebuff:
                score -= 2
                goalDebuff = False
              else:
                score += 1
              score_check = "Goal"
            elif (self.guess[0] == placement[0]) or (placement[0] == "OUT"):
              score_check = "Miss"
              if goalDebuff:
                score -= 1
                goalDebuff = False
            print("Score: "+ str(score))
            print("Speed: " + str(speed))
            print("U: " + placement[0])
            print("K: " + self.guess[0])
            print("-------------")
  def movement(self, x, y):
    # This functions moves the keeper to the position it chose.
    # Speed stored in arrays
    x_speed = []
    y_speed = []
    # Distance Calculations
    distance_x = x - self.rect.x
    distance_y = y - self.rect.y

    # speed calculations
    if y == 0 or x == 0:
      y_speed.append(0)
      x_speed.append(0)
    else:
      y_speed.append(distance_y/5)
      x_speed.append(distance_x/5)

    # If sprite has not reached its intended destination keep on moving, if it has stop moving.
    if self.rect.x != x:
       self.rect.x += x_speed[0]
    else:
      self.rect.x += 0
      
    if self.rect.y != y:
      self.rect.y += y_speed[0]
    else:
      self.rect.y += 0

  def rotate(self):
    #This function changes the keeper's sprite, and orientation depending on the position it chose.
    global target_pos
    if target_pos:
      if self.guess:
        if self.guess[0] == "TR":
          self.movement(450,30)
          self.image = pygame.transform.rotozoom(self.keeper[1], 15, 0.9)
          self.check = True
        elif self.guess[0] == "BR":
          self.movement(450, 120)
          self.image = pygame.transform.rotozoom(self.keeper[1], 0, 0.95)
          self.check = True
        elif self.guess[0] == "TL":
          self.movement(170, 30)
          self.image = pygame.transform.rotozoom(self.keeper[1], 165, 0.9)
          self.check = True
        elif self.guess[0] == "BL":
          self.movement(170, 120)
          self.image = pygame.transform.rotozoom(self.keeper[1], 180, 0.95)
          self.check = True
        elif self.guess[0] == "M":
          self.image = pygame.transform.rotate(self.keeper[0], 0)
          self.check = True
 
  def keeperReset(self):
    global keeper_reset
    # This function resets the keeper to its original position after a shot.
    if keeper_reset:
      self.angle = 0
      self.rect.x = 330
      self.rect.y = 40
      self.image = self.keeper[0]
      self.guess.clear()
      self.check = False

  def update(self):
    self.position()
    self.rotate()
    self.keeperReset()

class Buff(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()

    self.Speed = pygame.image.load('Graphics/Buffs/BallSpeedBuff.png').convert_alpha()
    self.Goal = pygame.image.load('Graphics/Buffs/GoalBuff.png').convert_alpha()
    self.Time = pygame.image.load('Graphics/Buffs/TimerBuff.png').convert_alpha()

    self.Buff = [self.Speed, self.Goal, self.Time]
    self.buffIndex = 2

    self.position = (250, 40)
    self.image = self.Buff[0]
    self.rect = self.image.get_rect(center = self.position)

    self.effect = False
    self.position = False

  def randomBuff(self):
    global buff_spawned
    if not buff_spawned:
      self.buffIndex = randint(0,2)
      self.image = self.Buff[self.buffIndex]
      self.effect = True

  def randomPos(self):
    global buff_spawned
    if not buff_spawned:
      self.rect = self.image.get_rect(center = (randint(158, 641),randint(20, 180)))
      self.position = True
  def main(self):
    global buffCollided, goalBoost, timerBoost, speedBoost
    if buffCollided:
      if self.buffIndex == 0:
        speedBoost = True
      elif self.buffIndex == 1:
       goalBoost = True
      elif self.buffIndex == 2:
        timerBoost = True

  def reset(self):
    global ball_reset, goalBoost, speedBoost
    if ball_reset:
      self.effect = False
      self.position = False
      goalBoost = False
      speedBoost = False
  def update(self):
    global buff_spawned, buffCollided
    if self.effect and self.position:
      buff_spawned = True
      buffCollided = False
    self.randomBuff()
    self.randomPos()
    self.main()
    self.reset()

class Debuff(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()

    self.Goal = pygame.image.load('Graphics/Debuffs/Goal Debuff.png').convert_alpha()
    self.Time = pygame.image.load('Graphics/Debuffs/Seconds Debuff.png').convert_alpha()
    self.Speed = pygame.image.load('Graphics/Debuffs/Speed Debuff.png').convert_alpha()

    self.Debuff = [self.Goal, self.Speed, self.Time]
    self.debuffIndex = 2

    self.position = (250,40)
    self.image = self.Debuff[self.debuffIndex]
    self.rect = self.image.get_rect(center = self.position)

    self.effect = False
    self.position = False

  def randomDebuff(self):
    global debuff_spawned
    if not debuff_spawned:
      self.debuffIndex = randint(0,1)
      self.image = self.Debuff[self.debuffIndex]
      self.effect = True

  def randomPos(self):
    global debuff_spawned
    if not debuff_spawned:
      self.rect = self.image.get_rect(center = (randint(158, 641),randint(20, 180)))
      self.position = True

  def main(self):
    global debuffCollided, goalDebuff, speedDebuff
    if debuffCollided:
      if self.debuffIndex == 0:
        goalDebuff = True
      elif self.debuffIndex == 1:
        speedDebuff = True
        

  def reset(self):
    global ball_reset, goalDebuff, debuffCollided, speedDebuff
    if ball_reset:
      self.effect = False
      self.position = False
      speedDebuff = False

  def update(self):
    global debuff_spawned, debuffCollided
    if self.position and self.effect:
      debuff_spawned = True
      debuffCollided = False
    self.randomDebuff()
    self.randomPos()
    self.reset()
    self.main()
    
def displayScore(state):
  if state == 'Game':
    scorefont = pygame.font.Font(None, 25)
    score_surface = scorefont.render('Score: ' + str(score), False, 'White')
    score_rect = score_surface.get_rect(center = (50, 50))
    screen.blit(score_surface, score_rect)
  elif state == 'Over':
    scorefont = pygame.font.Font(None, 115)
    score_surface = scorefont.render('Score: ' + str(score), False, 'White')
    screen.blit(score_surface, overScore_Rect)
def goalUpdate(current_time):
  global gamestate, ball_check, score_check, t2
  if ball_check and score_check == "Goal":
    if t2 == 0:
      t2 = current_time

    if current_time >= t2 + 1000:
      gamestate = "Goal"
      t2 = 0
  elif ball_check and score_check == "Miss":
    if t2 == 0:
      t2 = current_time

    if current_time >= t2 + 1000:
      gamestate = "Miss"
      t2 = 0
    
def displayTimer(t):
  # Displays how long the user has left.
  global gamestate, timerBoost
  if timerBoost:
    timeBoosted = t + (math.floor((pygame.time.get_ticks() - gameTime)/1000)) + 5
    timerBoost = False
    print("True")
    print("time -", str(timeBoosted))
  else:  
    timeBoosted = t
  time = timeBoosted - math.floor((pygame.time.get_ticks() - gameTime)/1000)
  minute = math.floor(time/60)
  seconds = math.floor(time % 60)
  timerfont = pygame.font.Font(None, 25)
  # Adds a 0 next to single digit numbers
  if seconds < 10:
    timer_surface = timerfont.render('Timer: ' + str(minute) + ':0' + str(seconds), False, 'White')
  else:
    timer_surface = timerfont.render('Timer: ' + str(minute) + ':' + str(seconds), False, 'White')
  timer_rect = timer_surface.get_rect(center = (50, 75))
  screen.blit(timer_surface, timer_rect)
  if time <= 0:
    gamestate = "Over"
    time = 0
    seconds = 0
  #return timer_surface, timer_rect
  #return time
def buttonClicked(rect, pos, newstate):
  global gamestate, aim_reset, score
  if newstate == "Game":
    aim_reset = True
  
  if rect.collidepoint(pos):
    if pygame.mouse.get_pressed()[0] == 1:
      gamestate = newstate
      score = 0  

# Initalising
pygame.init()
screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption('Penalty Shootout')
fps = pygame.time.Clock()

# Variables
speed = 7
score = 0
target_pos = []
placement = []
gamestate = "Menu"
buffArray = []

# Booleans used to loop playing.
# checks if the crosshair has stopped moving.
aim_reset = False
# sends crosshair back to original position with original speed.
aim_check = False
# checks if keeper has taken a guess.
keeper_check = False
# sends keeper back to original position, ready for next shot and removes old guess.
keeper_reset = False
# checks if the ball has reached the intended target before resetting.
ball_check = False
# resets the ball to penalty spot, ready for next shot.
ball_reset = False
# Ensures multiple buffs dont spawn at the same time.
buff_spawned = False
# Delets/resets the buff so it does not appear constantly.
buff_reset = False
# used in GoalUpdate function to show 'Goal' and 'Miss' images.
score_check = ""
# Checks if buff has collided with ball
buffCollided = False
# Goal Boost Buff
goalBoost = False
# Timer Boost Buff
timerBoost = False
# Speed Boost Buff
speedBoost = False
# Pause Variable
Paused = False
# ensures timer only starts when game is being played and not in menu screens etc.
timeSet = False
# Ensures multiple debuffs dont spawn at the same time.
debuff_spawned = False
# Delets/resets the debuff so it does not appear constantly.
debuff_reset = False
# Checks if debuff has collided with ball
debuffCollided = False
# Goal Debuff
goalDebuff = False
# Speed Debuff
speedDebuff = False
# Will only randomise buff and debuffs once during a round.
randomised = False

# Images
gameBackground = pygame.image.load("Graphics/Background.png").convert()
goalScreen = pygame.image.load('Graphics/Goal Screen.png').convert()
missScreen = pygame.image.load('Graphics/Miss Screen.png').convert()
menuScreen = pygame.image.load('Graphics/Main Menu.png').convert()
tutorialScreen = pygame.image.load('Graphics/Tutorial Screen.png').convert()
overScreen = pygame.image.load('Graphics/Game Over.png').convert()
pauseScreen = pygame.image.load('Graphics/Pause Menu.png').convert()

# Buttons                L,  T,  W,  H
# Menu Rectangles Positions and Size
play_Rect = pygame.Rect(307,70,180,93)
tutorial_Rect = pygame.Rect(284,200,234,87)
exit_Rect = pygame.Rect(340,335, 115, 90)
# Tutorial Rectangle
tutorialB_Rect = pygame.Rect(20,25,140,45)
# Game Over Rectangles
overB_Rect = pygame.Rect(20,324,343,70)
next_Rect = pygame.Rect(506, 329, 265, 66)
overScore_Rect = pygame.Rect(255, 150, 312, 92)
# Pause Menu Rectangles
resumeRect = pygame.Rect(280, 152, 250, 90)
exitPRect = pygame.Rect(340, 300, 118, 90)

# Classes
crosshair = pygame.sprite.GroupSingle()
crosshair.add(Aim())

ball = pygame.sprite.GroupSingle()
ball.add(Ball())

keeper = pygame.sprite.GroupSingle()
keeper.add(Keeper())

buff = pygame.sprite.GroupSingle()
buff.add(Buff())

debuff = pygame.sprite.GroupSingle()
debuff.add(Debuff())

timer = 0
reset_timer = 0
num = 0 
t1 = 0
t2 = 0
# Game running
while True:
  for event in pygame.event.get():
      if event.type == QUIT:
          pygame.quit()
          sys.exit()

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_p:
          Paused = not Paused

  current_time = pygame.time.get_ticks()
  pos = pygame.mouse.get_pos()
  
  if t1 == 0:
    t1 = current_time

  if current_time >= t1 + 1000:
    print("Gamestate:", gamestate)
    t1 = current_time

  if gamestate == "Game":

    if not timeSet:
      gameTime = pygame.time.get_ticks()
      timeSet = True
    
    if Paused:
      gamestate = "Paused"
    
    if aim_reset:
      if reset_timer == 0:
        reset_timer = current_time

      if current_time >= reset_timer + 1000:
        aim_reset = False
        reset_timer = 0

    if ball_reset:
      if reset_timer == 0:
        reset_timer = current_time

      if current_time >= reset_timer + 1000:
        ball_reset = False
        reset_timer = 0

    if keeper_reset:
      if reset_timer == 0:
        reset_timer = current_time

      if current_time >= reset_timer + 1000:
        keeper_reset = False
        reset_timer = 0

    if buff_reset:
      if reset_timer == 0:
        reset_timer = current_time

      if current_time >= reset_timer + 0000:
        buff_reset = False
        buff_spawned = False
        reset_timer = 0
    
    if debuff_reset:
      if reset_timer == 0:
        reset_timer = current_time

      if current_time >= reset_timer + 1000:
        debuff_reset = False
        debuff_spawned = False
        randomised = False
        reset_timer = 0
    
    screen.blit(gameBackground, (0,0))
  
    keeper.draw(screen)
    keeper.update()

    if not randomised:
      num = randint(1,10)
      randomised = True
      print("Random Num: " + str(num))
    if num >=1 and num <= 4:
      buff.draw(screen)
      buff.update()
    #print("Buff Spawned")
    elif num >=5 and num <=6:
      debuff.draw(screen)
      debuff.update()
    
    crosshair.draw(screen)
    crosshair.update()
    
    ball.draw(screen)
    ball.update()

    displayTimer(120)
    displayScore("Game")
    goalUpdate(current_time)
  elif gamestate == "Goal":
    
    ball_reset = True
    aim_reset = True
    keeper_reset = True
    buff_reset = True
    debuff_reset = True
    # Set the goal timer to the current time when entering the goal state
    if timer == 0:
        timer = current_time

    # Check if 5 seconds have passed since entering the goal state
    if current_time >= timer + 1000:
      ball_check = False
      score_check = ""
      gamestate = "Game"
      timer = 0
    screen.blit(goalScreen,(0,0))
  elif gamestate == "Miss":
    
    ball_reset = True
    aim_reset = True
    keeper_reset = True
    buff_reset = True
    debuff_reset = True
    # Set the goal timer to the current time when entering the miss state
    if timer == 0:
        timer = current_time

    # Check if 5 seconds have passed since entering the miss state
    if current_time >= timer + 1000:
      ball_check = False
      score_check = ""
      gamestate = "Game"
      timer = 0
    screen.blit(missScreen,(0,0))

  elif gamestate == "Menu":
    screen.blit(menuScreen,(0,0))

    pygame.draw.rect(screen, 'White', play_Rect, -1)
    buttonClicked(play_Rect, pos, "Game")
    
    pygame.draw.rect(screen, 'White', tutorial_Rect, -1)
    buttonClicked(tutorial_Rect, pos, "Tutorial")
    
    pygame.draw.rect(screen, 'White', exit_Rect, -1)
    buttonClicked(exit_Rect, pos, "Exit")

  elif gamestate == "Tutorial":
    screen.blit(tutorialScreen,(0,0))

    pygame.draw.rect(screen, 'White', tutorialB_Rect, -1)
    buttonClicked(tutorialB_Rect, pos, "Menu")
  elif gamestate == "Exit":
    pygame.quit()
    sys.exit()
  elif gamestate == "Over":
    screen.blit(overScreen,(0,0))

    pygame.draw.rect(screen, 'White', overB_Rect, -1)
    buttonClicked(overB_Rect, pos, "Menu")

    pygame.draw.rect(screen, 'White', next_Rect, -1)
    buttonClicked(next_Rect, pos, "Game")

    pygame.draw.rect(screen, 'Red', overScore_Rect)
    displayScore('Over')
  elif gamestate == "Paused":

    if not Paused:
      gamestate = "Game"
    screen.blit(pauseScreen,(0,0))

    pygame.draw.rect(screen, 'White', resumeRect, -1)
    buttonClicked(resumeRect, pos, "Game")

    pygame.draw.rect(screen, 'White', exitPRect, -1)
    buttonClicked(exitPRect, pos, "Menu")
    timeSet = False
  pygame.display.update()
  fps.tick(60)
    