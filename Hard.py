import pygame, os, random, sys
from util import load_font, load_image, load_sound

pygame.init()
pygame.mixer.init()

def HardGame():
  # Screen and Resolution
  resolution = (GameWidth,GameHeight)= (1000,600)
  screen = pygame.display.set_mode(resolution)

  background = load_image("assets/GUI/background.png")
  background = pygame.transform.scale(background,resolution)
  screen.blit(background,(0,0))

  # Game properties
  columns, rows, padding, score, card_width, card_height = 5, 4, 10, 0, 78, 120
  clicked, now, win, pause, game_flag = False, False, False, False, True
  font = load_font("assets/Font/BAUHS93.TTF",40)

  left_margin = (GameWidth-card_width*columns - padding*(columns-1))//2
  top_margin = (GameHeight-card_height*rows - padding*(rows-1))//2

  images_display, permission = [], []

  card_back = load_image("assets/GUI/Full Card back.png")
  card_back = pygame.transform.scale(card_back,(card_width,card_height))

  # Music
  winning_music = load_sound("assets/Sounds/Winning.mp3")
  bonus_music = load_sound("assets/Sounds/Bonus.mp3")
  wrong_music = load_sound("assets/Sounds/Wrong.mp3")
  Lose_music = load_sound("assets/Sounds/YouLose.wav")

  #Timer/Time's up
  timer_font = pygame.font.Font("assets/Font/BAUHS93.TTF",60)
  timesup_text = pygame.font.Font("assets/Font/BAUHS93.TTF",70)
  timesup_text = timer_font.render("Time\'s up", True, "dark green")       
  timer_start = 59


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
  menu_rect.left = int(0.5*(GameWidth-600))
  menu_rect.top = int(0.5*(GameHeight-450))

  #continue button
  continue_button = load_image("assets/GUI/continue.png")
  continue_button = pygame.transform.scale(continue_button,(400,100))
  continue_rect = continue_button.get_rect()
  continue_rect.left = int(0.5*(GameWidth-400))
  continue_rect.top = int(0.5*(GameHeight-450)+120)

  #exit buttons
  exit_button = load_image("assets/GUI/exit.png")
  exit_button = pygame.transform.scale(exit_button,(400,100))
  exit_rect = exit_button.get_rect()
  exit_rect.left = int(0.5*(GameWidth-400))
  exit_rect.top = int(0.5*(GameHeight-500)+150)

  exit2_rect = exit_rect
  exit2_rect.left = int(0.5*(GameWidth-400))
  exit2_rect.top = int(0.5*(GameHeight-500)+250)

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
    for counter in range(len(images)):
      if images_display[counter]:
        screen.blit(images[counter], images_rect[counter])
      # mazen
      elif images_display[counter] == "2":
        pass
      ##
      else:
        screen.blit(card_back,images_rect[counter])
  def wait(seconds):
    start_time = pygame.time.get_ticks()
    wait_duration = seconds * 1000  # Convert seconds to milliseconds

    while (pygame.time.get_ticks() - start_time) < wait_duration:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

      pygame.display.flip()
      try:
        screen.blit(TimerText,(60,70))
      except:
        pass
  def TimesUp():
    screen.blit(menu,menu_rect)
    screen.blit(timesup_text,(365,110))
    screen.blit(play_again,play_again_rect)
    screen.blit(exit_button,exit2_rect)
    if game_flag:
      Lose_music.play(0)

  #List of images names
  PicNames_list=[image.split(".")[0] for image in os.listdir("assets/Hard Images/")]
  PicNames_list_copy=PicNames_list[:]
  for i in PicNames_list_copy:
    PicNames_list.append(i)
  random.shuffle(PicNames_list)

  #List of images & rect
  images = []
  images_rect=[]
  for item in PicNames_list:
    image = load_image(f"assets/Hard Images/{item}.png")
    image = pygame.transform.scale(image,(card_width,card_height))
    images.append(image)
    image_rect= image.get_rect()
    images_rect.append(image_rect)
    images_display.append(True)
    permission.append("permitted")

  for item in range(len(images)):
    images_rect[item].left = left_margin + (card_width+padding)*(item%columns)
    images_rect[item].top = top_margin + (card_height+padding)*(item%rows)
  check_display()

  ScoreText=font.render(f"Score: {score}",True,"dark cyan")
  screen.blit(ScoreText,(20,5))

  wait(2.5)

  #Hiding images
  for j in range(9):
    animation_vars = [animation(PicNames_list[k],True)[j] for k in range(20)]
    wait(0.005)
    screen.blit(background,(0,0))
    screen.blit(pause_button,pause_rect)
    screen.blit(ScoreText,(20,5))
    for i in range(len(animation_vars)):
      screen.blit(animation_vars[i],images_rect[i])

  for count in range(len(PicNames_list)):
    images_display[count]=False
  check_display()


  now=True
  pause=False
  win=False
  StartMoment = pygame.time.get_ticks()/1000
  while True:
    pygame.display.update()
    screen.blit(background,(0,0))
    #Mazen
    screen.blit(pause_button,pause_rect)#mazen
    #Images display
    check_display()
    #score text
    ScoreText=font.render(f"Score: {score}",True,"dark cyan")
    screen.blit(ScoreText,(20,5))

    #WIN
    if score==500 and game_flag:
      winning_music.play(0)
      win=True
      game_flag = False

    #Events
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        # GameLoop=False
        pygame.quit()
        sys.exit()
      elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
        if not pause or not win:
          for i in range(len(images_rect)):
            if images_rect[i].collidepoint(event.pos):
              # First card
              if not(clicked) and permission[i]=="permitted" and not pause:
                clicked = images_display[i]="2"###
                check_display()
                selection1 = PicNames_list[i]
                selection1_index=i
                ##mazen
                for j in range(0,9):
                  animation_var=animation(selection1)[j]
                  wait(0.005)
                  screen.blit(background,(0,0))
                  screen.blit(pause_button,pause_rect)
                  screen.blit(ScoreText,(20,5))
                  check_display()
                  screen.blit(animation_var,images_rect[i])
                images_display[i]=True

              #Second Card
              elif clicked and permission[i]=="permitted" and now and not pause:
                now=False
                images_display[i]="2"
                
                check_display()
                selection2 = PicNames_list[i]
                if selection1==selection2 and i!=selection1_index:
                  ###   Mazen   ###
                  for j in range(9):
                    animation_var=animation(selection2)[j]
                    wait(0.005)
                    screen.blit(background,(0,0))
                    screen.blit(pause_button,pause_rect)
                    screen.blit(ScoreText,(20,5))
                    check_display()
                    screen.blit(animation_var,images_rect[i])
                  images_display[i]=True

                  bonus_music.play(0)
                  score+=50
                  permission[i] = permission[selection1_index] ="not permitted"
                  now=True
                  clicked=False

                elif selection1==selection2 and i==selection1_index:
                  wrong_music.play(0)
                  wait(0.5)
                  images_display[i] = images_display[selection1_index] ="2"
                  check_display()
                  now=True
                  ###   Mazen   ###
                  for j in range(9):
                    animation_var0=animation(selection1,True)[j]
                    wait(0.005)
                    screen.blit(background,(0,0))
                    screen.blit(pause_button,pause_rect)
                    screen.blit(ScoreText,(20,5))
                    check_display()
                    screen.blit(animation_var0,images_rect[selection1_index])
                  clicked=False
                  images_display[i]=images_display[selection1_index]=False
                else:
                  ###   Mazen   ###
                  for j in range(9):
                    animation_var=animation(selection2)[j]
                    wait(0.005)
                    screen.blit(background,(0,0))
                    screen.blit(pause_button,pause_rect)
                    screen.blit(ScoreText,(20,5))
                    check_display()
                    screen.blit(animation_var,images_rect[i])
                  images_display[i]=True

                  wrong_music.play(0)
                  wait(0.5)
                  images_display[i] = images_display[selection1_index] ="2"
                  check_display()
                  now=True
                  ###   Mazen   ###
                  for j in range(9):
                    animation_var0=animation(selection1,True)[j]
                    animation_var1=animation(selection2,True)[j]
                    wait(0.005)
                    screen.blit(background,(0,0))
                    screen.blit(pause_button,pause_rect)
                    screen.blit(ScoreText,(20,5))
                    check_display()
                    screen.blit(animation_var0,images_rect[selection1_index])
                    screen.blit(animation_var1,images_rect[i])
                  clicked=False
                  images_display[i]=images_display[selection1_index] = False
        ###   Mazen   ###
        if pause_rect.collidepoint(event.pos) and not pause:
          pause=True
        elif continue_rect.collidepoint(event.pos) and pause:
          timer_start = timer
          StartMoment = pygame.time.get_ticks()/1000
          pause=False
        elif exit_rect.collidepoint(event.pos) and pause:
          pygame.quit()
          sys.exit()
        elif play_again_rect.collidepoint(event.pos) and (win or not game_flag):
          HardGame()
        elif exit2_rect.collidepoint(event.pos) and (win or not game_flag):
          pygame.quit()
          sys.exit()
    # Mazen
    if pause:
      screen.blit(menu,menu_rect)
      screen.blit(continue_button,continue_rect)
      screen.blit(exit_button,exit_rect)
    if win:
      screen.blit(menu,menu_rect)
      screen.blit(you_win,(365,110))
      screen.blit(play_again,play_again_rect)
      screen.blit(exit_button,exit2_rect)

    # timer
    if not pause:
      timer = (timer_start - int((pygame.time.get_ticks()/1000)-(StartMoment)))
    TimerText = timer_font.render(f"{max(0,timer)}",True,"dark green")
    screen.blit(TimerText,(60,70))
    if timer <= 0 and not win:
      TimesUp()
      game_flag = False
      images_display = [False]*20
      permission = ["not permitted"]*20