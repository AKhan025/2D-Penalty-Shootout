import pygame, sys, math
from pygame.locals import QUIT

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