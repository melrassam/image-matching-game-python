import pygame, os, random, sys
from util import load_image, load_font

pygame.init()
pygame.mixer.init()

def EasyGame():
  #Screen, resolution, and caption
  resolution = game_width, game_height =  1000, 600
  screen = pygame.display.set_mode(resolution)

  #background
  background = load_image("assets/GUI/background.png")
  background = pygame.transform.scale(background,resolution)
  screen.blit(background,(0,0))

  #Game properties
  columns,rows,padding,score,card_width, card_height = 4,3,10,0,100,150
  clicked,now,win,pause =False,False,False,False
  font = load_font("assets/Font/BAUHS93.TTF",40)
  left_margin = (game_width-card_width*columns - padding*(columns-1))//2
  top_margin = (game_height-card_height*rows - padding*(rows-1))//2

  #Control lists
  images_display, permission = [], []

  #Card back
  card_back = load_image("assets/GUI/Full Card back.png")
  card_back = pygame.transform.scale(card_back,(card_width,card_height))

  #Music
  winning_music = pygame.mixer.Sound("assets/Sounds/Winning.mp3")
  bonus_music = pygame.mixer.Sound("assets/Sounds/Bonus.mp3")
  wrong_music = pygame.mixer.Sound("assets/Sounds/Wrong.mp3")

  ###   Mazen   ###
  #pause button
  pause_button = load_image("assets/GUI/pause.png")
  pause_button = pygame.transform.scale(pause_button,(50,40))
  pause_rect = pause_button.get_rect()
  pause_rect.left, pause_rect.top = 950,20
  screen.blit(pause_button,pause_rect)
  #menu
  menu = load_image("assets/GUI/menu.png")
  menu = pygame.transform.scale(menu,(600,450))
  menu_rect = menu.get_rect()
  menu_rect.left, menu_rect.top = (game_width-600) // 2, (game_height-450) // 2

  #continue button
  continue_button = load_image("assets/GUI/continue.png")
  continue_button = pygame.transform.scale(continue_button,(400,100))
  continue_rect = continue_button.get_rect()
  continue_rect.left, continue_rect.top = (game_width-400) // 2, (game_height-450) // 2 + 120

  #exit buttons
  exit_button = load_image("assets/GUI/exit.png")
  exit_button = pygame.transform.scale(exit_button,(400,100))
  exit_rect = exit_button.get_rect()
  exit_rect.left, exit_rect.top = (game_width - 400) // 2, (game_height-500) // 2 + 150

  exit2_rect = exit_rect
  exit2_rect.left, exit2_rect.top = (game_width - 400) // 2, (game_height-500) // 2 + 250

  #you win text
  you_win = pygame.font.Font("assets/Font/BAUHS93.TTF",70)
  you_win = you_win.render('You Win!', True, "dark green")

  #play again button
  play_again = load_image("assets/GUI/play again.png")
  play_again = pygame.transform.scale(play_again,(400,100))
  play_again_rect = play_again.get_rect()
  play_again_rect.left, play_again_rect.top = 300,200

  ###   Mazen   ###
  def animation(name, reverse=False):
    sprite = []
    for k in range(9):
      sprite.append(load_image(f"assets/Animation/{name}/0{k}_{name} Sprite2.png"))

    sprite_scale = []
    for i in sprite:
      sprite1 = pygame.transform.scale(i,(card_width,card_height))
      sprite_scale.append(sprite1)

    if reverse:
      return sprite_scale[::-1]
    else:
      return sprite_scale

  def check_display():
    for i in range(len(images)):
      if images_display[i]:
        screen.blit(images[i],images_rect[i])
      else:
        screen.blit(card_back,images_rect[i])

  def wait(seconds):
    start_time = pygame.time.get_ticks()
    wait_duration = seconds * 1000  # Convert seconds to milliseconds

    while (pygame.time.get_ticks() - start_time) < wait_duration:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

      pygame.display.flip()

  #List of images names
  pic_names_list = [image.split(".")[0] for image in os.listdir("assets/Easy Images/")]
  pic_names_list += pic_names_list[:]
  random.shuffle(pic_names_list)

  #List of images & rect
  images, images_rect = [], []
  for k in pic_names_list:
    image = load_image(f"assets/Easy Images/{k}.png")
    image = pygame.transform.scale(image,(card_width,card_height))
    images.append(image)
    image_rect= image.get_rect()
    images_rect.append(image_rect)
    images_display.append(True)
    permission.append("permitted")

  #Positions of rectangles
  for k in range(len(images)):
    images_rect[k].left = left_margin + (card_width+padding) * (k % columns)
    images_rect[k].top = top_margin + (card_height+padding) * (k % rows)

  #Showing Cards
  check_display()

  #Score text
  score_text = font.render(f"Score: {score}",True,"dark cyan")
  screen.blit(score_text,(20,5))

  wait(1.5)

  #Hiding Images
  for j in range(9):
    animation_vars = [animation(pic_names_list[k],True)[j] for k in range(12)]
    wait(0.005)
    screen.blit(background,(0,0))
    screen.blit(pause_button,pause_rect)
    screen.blit(score_text,(20,5))

    for i in range(len(animation_vars)):
      screen.blit(animation_vars[i],images_rect[i])

  images_display = [False] * len(pic_names_list)
  check_display()

  now, pause, win, game_flag = True, False, False, True
  while True:
    pygame.display.update()
    screen.blit(background,(0,0))
    screen.blit(pause_button,pause_rect)

    #Images display
    check_display()

    #score text
    score_text=font.render(f"Score: {score}",True,"dark cyan")
    screen.blit(score_text,(20,5))

    #WIN
    if score == 300 and game_flag:
      winning_music.play(0)
      win=True
      game_flag = False
    #Events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

      #Clicking events
      elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        if not pause or win:
          for i in range(len(images)):
                if images_rect[i].collidepoint(event.pos):
                  # First card
                  if not(clicked) and permission[i] == "permitted" and not pause:
                    clicked = images_display[i] = "2"
                    check_display()
                    selection1 = pic_names_list[i]
                    selection1_index=i

                    for j in range(9):
                      animation_var = animation(selection1)[j]
                      wait(0.005)
                      screen.blit(background,(0,0))
                      screen.blit(pause_button,pause_rect)
                      screen.blit(score_text,(20,5))
                      check_display()
                      screen.blit(animation_var,images_rect[i])
                    images_display[i]=True

                  #Second Card
                  elif clicked and permission[i] == "permitted" and now and not pause:
                    now = False
                    images_display[i] = "2"

                    check_display()
                    selection2 = pic_names_list[i]

                    if selection1 == selection2 and i != selection1_index:
                      for j in range(9):
                        animation_var = animation(selection2)[j]
                        wait(0.005)
                        screen.blit(background,(0,0))
                        screen.blit(pause_button,pause_rect)
                        screen.blit(score_text,(20,5))
                        check_display()
                        screen.blit(animation_var,images_rect[i])
                      images_display[i] = True

                      bonus_music.play(0)
                      score += 50
                      permission[i] = permission[selection1_index] = "not permitted"
                      now = True
                      clicked = False

                    elif selection1 == selection2 and i == selection1_index:
                      wrong_music.play(0)
                      wait(0.5)
                      images_display[i] = images_display[selection1_index] = "2"
                      check_display()
                      now=True

                      for j in range(9):
                        animation_var0 = animation(selection1,True)[j]
                        wait(0.005)
                        screen.blit(background,(0,0))
                        screen.blit(pause_button,pause_rect)
                        screen.blit(score_text,(20,5))
                        check_display()
                        screen.blit(animation_var0,images_rect[selection1_index])
                      clicked = False
                      images_display[i]=images_display[selection1_index] = False

                    else:
                      for j in range(9):
                        animation_var = animation(selection2)[j]
                        wait(0.005)
                        screen.blit(background,(0,0))
                        screen.blit(pause_button,pause_rect)
                        screen.blit(score_text,(20,5))
                        check_display()
                        screen.blit(animation_var,images_rect[i])
                      images_display[i] = True

                      wrong_music.play(0)
                      wait(0.5)
                      images_display[i] = images_display[selection1_index] = "2"
                      check_display()
                      now = True

                      for j in range(9):
                        animation_var0=animation(selection1,True)[j]
                        animation_var1=animation(selection2,True)[j]
                        wait(0.005)
                        screen.blit(background,(0,0))
                        screen.blit(pause_button,pause_rect)
                        screen.blit(score_text,(20,5))
                        check_display()
                        screen.blit(animation_var0,images_rect[selection1_index])
                        screen.blit(animation_var1,images_rect[i])
                      clicked = False
                      images_display[i]=images_display[selection1_index]=False

        if pause_rect.collidepoint(event.pos) and not pause:
          pause = True
        elif continue_rect.collidepoint(event.pos) and pause:
          pause = False
        elif exit_rect.collidepoint(event.pos) and pause:
          pygame.quit()
          sys.exit()
        elif play_again_rect.collidepoint(event.pos) and win:
          EasyGame()
        elif exit2_rect.collidepoint(event.pos) and win:
          pygame.quit()
          sys.exit()

    ###   Mazan   ###
    if pause:
      screen.blit(menu,menu_rect)
      screen.blit(continue_button,continue_rect)
      screen.blit(exit_button,exit_rect)
    if win:
      screen.blit(menu,menu_rect)
      screen.blit(you_win,(365,110))
      screen.blit(play_again,play_again_rect)
      screen.blit(exit_button,exit2_rect)