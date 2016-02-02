# Jackson Singleton
# December_10_2015

import pygame
import os



pygame.init()

os.environ['SDL_VIDEODRIVER'] = 'windib'


class main(object):
    def __init__(self):
        """Initialize a new game."""

        self._running = True


        """  set screen size"""
        self._screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill((0, 0, 0))
        """ screen title"""
        pygame.display.set_caption('ULTIMATE PONG')
        self.bg = pygame.image.load("gamebg.png")
        self.background1y = 0
        self.background2y = -600
        self._title = pygame.image.load("pongtitle.png")
        self.ballBot = False
        self.botFollow = True
        self.ballPlayer = True
        self.ballDown = False
        self.ballUp = False
        self.collidePlayer = True
        self.collideBot = True
        self.botUp = True
        self.botDown = False
        self.ballPosY = 300
        self.rectbot = pygame.Rect((790, 290), (10, 50))

        self.rectPlayer = pygame.Rect((0, 290), (10, 50))

        self.rectPlayer2 = pygame.Rect((790, 290), (10, 50))

        self.rectBall = pygame.Rect((400, self.ballPosY), (15, 15))
        self.playerup = False
        self.playerdown = False
        self.playerup2 = False
        self.playerdown2 = False

        self.botmoveup = False
        self.botmovedown = False
        self.reset = False

        self.pong = pygame.mixer.Sound("pong.wav")
        pygame.mouse.set_visible(False)


        # GAME OBJECTS




        self.gameover = False
        self.title = True
        self._game1P = False
        self._game2P = False
        self.scoreBot = False
        self.scorePlayer = False

        self.playerScore = 0
        self.botScore = 0




        self._font = pygame.font.SysFont('ms comic sans', 30)
        self._font2 = pygame.font.SysFont('arial black', 180)
        pygame.mixer.music.load("gameSong.mp3")
        pygame.mixer.music.play(-1)


    def run(self):
        FPS = 144
        clock = pygame.time.Clock()

        pygame.display.init()
        while self._running:
            clock.tick(FPS)
            self.handle_input()

            if self._game1P:
                self.bgMethod2()

                self.playerMove()
                self.ballMovement()
                self.botMove()
                self.gameReset()
            if self._game2P:
                self.bgMethod2()

                self.playerMove()
                self.ballMovement()
                self.gameReset()
            if self.title:
                self.bgMethod()
                self.backgroundScroll()
            pygame.display.flip()

        pygame.quit()

    def handle_input(self):
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                self._running = False
            elif evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_ESCAPE:
                    if self.title:
                        self._running = False
                    if self._game1P or self._game2P:
                        self._game = False
                        self.title = True
                        self.__init__()
                if evt.key == pygame.K_1:
                    if self.title:
                        self._game1P = True
                        self.title = False
                    if self._game1P:
                        self.reset = False
                if evt.key == pygame.K_2:
                    if self.title:
                        self._game2P = True
                        self.title = False
                    if self._game2P:
                        self.reset = False

                    #PLAYER 1 CONTROLS
                if evt.key == pygame.K_w:
                    self.playerup = True
                if evt.key == pygame.K_s:
                    self.playerdown = True

                if evt.key == pygame.K_UP:
                    self.playerup2 = True
                if evt.key == pygame.K_DOWN:
                    self.playerdown2 = True

            elif evt.type == pygame.KEYUP:
                if evt.key == pygame.K_w:
                    self.playerup = False
                if evt.key == pygame.K_s:
                    self.playerdown = False


                    #PLAYER 2 Controls



                if evt.key == pygame.K_UP:
                    self.playerup2 = False
                if evt.key == pygame.K_DOWN:
                    self.playerdown2 = False


                if evt.key == pygame.K_SPACE:
                    self.backgroundScroll()
                    self.bgMethod()

    def backgroundScroll(self):
        if self.background2y >= 600:
            self.background2y = -600
        if self.background1y >= 600:
            self.background1y = -600

        if self.background1y <= 600:
            self.background1y += 4

        if self.background2y <= 600:
            self.background2y += 4

    def bgMethod(self):
        self._screen.blit(self._background, (0, 0))
        self._screen.blit(self.bg, (0, self.background1y))
        self._screen.blit(self.bg, (0, self.background2y))
        self._screen.blit(self._title, (0, 20))
        _esc = self._font.render('PRESS "1" for 1-Player, "2" for 2-Player', 1, (0, 0, 0))
        _esc2 = self._font.render('PRESS "1" for 1-Player, "2" for 2-Player', 1, (255, 255, 255))

        self._screen.blit(_esc, (300, 400))
        self._screen.blit(_esc2, (298, 400))

    # GAME

    def bgMethod2(self):
        self._screen.blit(self._background, (0, 0))
        score1 = self._font2.render(str(self.playerScore), 1, (65, 65, 65))
        score2 = self._font2.render(str(self.botScore), 1, (65, 65, 65))
        self._screen.blit(score1, (20, 150))
        self._screen.blit(score2, (680, 150))

        self._screen.fill((255, 255, 255), self.rectBall)
        self._screen.fill((255, 255, 255), self.rectPlayer)
        if self._game1P:
            self._screen.fill((255, 255, 255), self.rectbot)
        if self._game2P:
            self._screen.fill((255, 255, 255), self.rectPlayer2)

    def playerMove(self):

        if self.rectPlayer.y <= 550:
            if self.playerdown:
                self.rectPlayer.y += 3
        if self.rectPlayer.y >= 0:

            if self.playerup:
                self.rectPlayer.y -= 3

        if self.rectPlayer2.y <= 550:
            if self.playerdown2:
                self.rectPlayer2.y += 3
        if self.rectPlayer2.y >= 0:
            if self.playerup2:
                self.rectPlayer2.y -= 3

    def ballMovement(self):
        ballSpeed = 0.75
        self.ballY = 2
        self.followUp = False
        self.followDown = False
        if self.ballPlayer:
            self.rectBall.x -= float(ballSpeed)*1.5

        if self.ballDown:
            self.rectBall.y -= 0
            self.rectBall.y += self.ballY
            if self.rectbot.y <= 585:
                self.botDown = True

        if self.ballUp:
            self.rectBall.y += 0
            self.rectBall.y -= 2
            if self.rectbot.y >= 0:
                self.botUp = True

        if self.rectBall.y >= 585:
            self.ballUp = True
            self.ballDown = False
        if self.rectBall.y <= 0:
            self.ballDown = True
            self.ballUp = False





        if self.ballBot:
            self.rectBall.x += float(ballSpeed)*2
            self.ballPlayer = False


        if self.rectBall.colliderect(self.rectPlayer):
            self.ballPlayer = False
            self.ballBot = True

            if self.rectPlayer.y <=350:
                self.ballUp = True
                self.ballDown = False
            if self.rectPlayer.y >=350:
                self.ballUp = False
                self.ballDown = True

            pygame.mixer.Sound.play(self.pong)
        if self._game1P:
            if self.rectBall.colliderect(self.rectbot):
                self.ballPlayer = True
                self.ballBot = False

                if self.rectbot.y <=350:
                    self.ballUp = False
                    self.ballDown = True
                if self.rectbot.y >=350:
                    self.ballUp = True
                    self.ballDown = False
                pygame.mixer.Sound.play(self.pong)
        if self._game2P:
            if self.rectBall.colliderect(self.rectPlayer2):
                self.ballPlayer = True
                self.ballBot = False

                if self.rectPlayer2.y <=350:
                    self.ballUp = True
                    self.ballDown = False
                if self.rectPlayer2.y >=350:
                    self.ballUp = False
                    self.ballDown = True

                pygame.mixer.Sound.play(self.pong)


    def botMove(self):
          if self.botUp:
              self.botDown = False
              self.rectbot.y -= 1.9

          if self.botDown:
              self.botUp = False
              self.rectbot.y += 1.9

          if self.rectbot.y <= 0:

             self.botUp = False
          if self.rectbot.y >= 550:
             self.botDown = False







    def gameReset(self):
        self.reset = False
        if self.rectBall.x <= 0:
            self.scoreBot = True
            self.reset = True

        else:
            self.scoreBot = False
        if self.rectBall.x >= 800:
            self.scorePlayer = True
            self.reset = True
        else:
            self.scorePlayer = False
        if self.scoreBot:
            self.botScore = self.botScore + 1



        if self.scorePlayer:
            self.playerScore = self.playerScore + 1
            self.reset = True





        if self.reset:
            self.rectBall.x = 400
            self.rectBall.y = 300
            self.ballUp = False
            self.ballDown = False
            self.botUp = False
            self.botDown = False
            self.rectbot.y = 290




g= main()
g.run()
