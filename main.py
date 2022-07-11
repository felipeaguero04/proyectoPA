#!/usr/bin/python3

'''
Sebastian Vargas Quesada
C18295
Luis Felipe Aguero Peralta
C10089
Este programa es una recreacion del juego "Space Invaders", el cual se utilizar
la extension de pygame para crearlo. El juego consiste en destruir naves
espaciales al lanzar un laser, ademas las naves enemigas tambien lazan lasers.
Por cada nave destruida se aumenta el puntaje en 1 y el programa posee un
"highscore" que guarda el puntaje mas alto. El juego termina cuando las naves
enemigas logran impactar varias veces en la nave del jugador.
'''
# Se importan las bibliotecas que se utilizaran en el programa.
import pygame
import os
import random
# Se incializa pygame.
pygame.init()
# Se inicia las fuentes de pygame .
pygame.font.init()
# Se define la altura y el ancho de la ventana de juego.
ancho = 750
altura = 750
# Se define la variable WIN como la ventana creada.
WIN = pygame.display.set_mode((ancho, altura))
# Se inserta el nombre de la ventana.
pygame.display.set_caption("Naves Espaciales")

# Se cargan las imagenes de las naves.
nave_roja = pygame.image.load(os.path.join("nave_roja.png"))
nave_verde = pygame.image.load(os.path.join("nave_verde.png"))
nave_azul = pygame.image.load(os.path.join("nave_azul.png"))

# Nave del jugador.
nave_amarilla = pygame.image.load(os.path.join("nave_amarilla.png"))

# Se cargan las imagenes de los lasers
laser_rojo = pygame.image.load(os.path.join("laser_rojo.png"))
laser_verde = pygame.image.load(os.path.join("laser_verde.png"))
laser_azul = pygame.image.load(os.path.join("laser_azul.png"))
laser_amarillo = pygame.image.load(os.path.join("laser_amarillo.png"))
# Se cargan los sonidos que se usaran.
laserSound = pygame.mixer.Sound('laser.wav')
explosionSound = pygame.mixer.Sound('explosion.wav')
gameoverSound = pygame.mixer.Sound('gameover.wav')
# Se carga el fondo de la pantalla.
BG = pygame.transform.scale(pygame.image.load(os.path.join("fondo.png")),
                            (ancho, altura))
# Se carga la musica que se va a utilizar y se guarda en la variable musica.
music = pygame.mixer.music.load("background.wav")
# Se reproduce la cancion en bucle.
pygame.mixer.music.play(-1)
# Se define la clase de Laser.


class Laser:
    # Se crea el metodo construcor con "x", "y" y "img" como parametros.
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    # Se crea la superficie del laser en las coordenadas dadas.

    def draw(self, ventana):
        ventana.blit(self.img, (self.x, self.y))
    # Se le da movimiento al laser al moverlo a una cierta velocidad en el ejey

    def move(self, vel):
        self.y += vel
    # Se verifica que el laser se encuentre dentro de la pantalla.

    def off_screen(self, altura):
        # El laser tiene que estar por arriba del 0 y abajo de la
        # altura maxima.
        return not(self.y <= altura and self.y >= 0)

    # Se llama la funcion de colision.
    def collision(self, obj):
        return collide(self, obj)

# Se crea la clase Ship, la cual se encarga de las naves.


class Ship:
    # Se define un enfriamiento de 30.
    COOLDOW = 30
    # Se crea el metodo constructor con "x", "y" y "salud = 100" como
    # parametros

    def __init__(self, x, y, salud=100):
        # Se definen nuevas variables como ship_img, laser_img, lasers y
        # contador_enfriamiento
        self.x = x
        self.y = y
        self.salud = salud
        # La imagen de la nave y la imagen del laser se definen luego
        # Ya que hay naves y lasers de diferentes colores.
        self.ship_img = None
        self.laser_img = None
        # Se crea una lista donde se guardaran los lasers creados.
        self.lasers = []
        self.contador_enfriamiento = 0
    # Se crea la superfice de la nave en las coordenadas dadas.

    def draw(self, ventana):
        ventana.blit(self.ship_img, (self.x, self.y))
        # Se pasan a la fucnion draw todos los lasers que esten en la lista.
        for laser in self.lasers:
            laser.draw(ventana)
    # Se le da movimiento al laser, se ocupa una velocidad y un obejto.

    def move_lasers(self, vel, obj):
        # Se llama la funcion enfriamiento.
        self.enfriamiento()
        # Para cada laser en lasers, se llama la funcion move.
        for laser in self.lasers:
            laser.move(vel)
            # Si el laser sale de la pantalla se remueve de la lista
            if laser.off_screen(altura):
                self.lasers.remove(laser)
            # Si el laser choca, se resta -10 a la salud y
            # Se remueve de la lista
            elif laser.collision(obj):
                obj.salud -= 10
                self.lasers.remove(laser)
    # Se crea la funcion enfriamiento para tener un tiempo entre tiro y tiro.

    def enfriamiento(self):
        # Si el contador_enfriamiento es mayor al COOLDOW el
        # contador_enfriamiento
        # Se reinicia
        if self.contador_enfriamiento >= self.COOLDOW:
            self.contador_enfriamiento = 0
        # Si el contador_enfriamiento es menor mayor a 0 aumenta en 1.
        elif self.contador_enfriamiento > 0:
            self.contador_enfriamiento += 1
    # Se crea la funcion de shoot.

    def shoot(self):
        # Si contador_enfriamiento es igual a 0
        if self.contador_enfriamiento == 0:
            # Se utiliza la clase Laser.
            laser = Laser(self.x, self.y, self.laser_img)
            # Se añade a la lista de lasers.
            self.lasers.append(laser)
            # El contador_enfriamiento se vuelve 1.
            self.contador_enfriamiento = 1
    # Con la funcion get_width se determina el ancho de las imagenes.

    def get_width(self):
        return self.ship_img.get_width()
    # Con la funcion get_height se determina la altura de las imagenes.

    def get_height(self):
        return self.ship_img.get_height()

# Se crea la clase Player la cual a su vez llama a la clase Ship.


class Player(Ship):
    # Se crea el metodo constructor con los mismos parametros.
    def __init__(self, x, y, salud=100):
        # La funcion super() hereda el __init__ de la clase Ship.
        super().__init__(x, y, salud)
        # La nave es la amarilla.
        self.ship_img = nave_amarilla
        # El laser es amarillo
        self.laser_img = laser_amarillo
        # Se crea una mascara del contorno de la imagen
        self.mask = pygame.mask.from_surface(self.ship_img)
        # Se define una salud maxima igual a la salud
        self.max_salud = salud
        # Se define el score como 0
        self.score = 0
    # Igual que en la clase Ship.

    def move_lasers(self, vel, objs):
        self.enfriamiento()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(altura):
                self.lasers.remove(laser)
            else:
                # Para cada objeto en objetos se verifica si el laser colisiona
                # Con una nave enemiga.
                for obj in objs:
                    if laser.collision(obj):
                        # Si el laser colisiona el score sube en 1 y
                        # Se remueve el objeto
                        self.score += 1
                        objs.remove(obj)
                        # Se remueve el laser de la lista.
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    # Se hereda la funcion draw de la clase Ship.
    # Se crea la superficie de la barra de salud

    def draw(self, ventana):
        super().draw(ventana)
        self.barra_salud(ventana)
    # Se crea una barra de salud al crear dos rectangulos: uno verde y uno
    # rojo.

    def barra_salud(self, ventana):
        pygame.draw.rect(ventana, (255, 0, 0), (self.x, self.y +
                                                self.ship_img.get_height() +
                                                10, self.ship_img.get_width(),
                                                10))
        pygame.draw.rect(ventana, (0, 138, 140), (self.x, self.y +
                                                  self.ship_img.get_height()
                                                  + 10,
                                                  self.ship_img.get_width()
                                                  *
                                                  (self.salud/self.max_salud),
                                                  10))

# Se crea la clase Enemy la cual llama a la clase Ship


class Enemy(Ship):
    # Se crea un diccionario con los colores de las naves.
    COLOR_MAP = {
                "red": (nave_roja, laser_rojo),
                "green": (nave_verde, laser_verde),
                "blue": (nave_azul, laser_azul)
                }
    # Se crea el metodo constructor con los mismos parametros mas el color.

    def __init__(self, x, y, color, salud=100):
        # Se hereda el __init__() de la clase Ship.
        super().__init__(x, y, salud)
        # Se define el color de la nave y del laser.
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        # Se crea una mascara en la imagen de la nave
        self.mask = pygame.mask.from_surface(self.ship_img)
    # Se le da movimiento a la nave con la velocidad en el eje y.

    def move(self, vel):
        self.y += vel
    # Se crea la funcion shoot para que la nave dispare los lasers.

    def shoot(self):
        # Si el contador_enfriamiento es igual a 0.
        if self.contador_enfriamiento == 0:
            # Se llama a la clase Laser para que lo cree.
            laser = Laser(self.x-20, self.y, self.laser_img)
            # Se añade el laser a la lista.
            self.lasers.append(laser)
            # El contador_enfriamiento se iguala a 1.
            self.contador_enfriamiento = 1

# Se define la funcio collide con dos objetos como parametros.


def collide(obj1, obj2):
    # Se obtiene la distancia entre los objetos en x y en y
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    # Si la ditancia de estos objetos se superpone entonces devuelve True.
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

# Se crea la funcion main.


def main():
    # Se define a run como True.
    run = True
    # Los cuadros por segundo se definen a 60.
    FPS = 60
    # El nivel inicia en 0
    nivel = 0
    # Se añaden las funtes de texto.
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    # Se crea una lista de enemigos.
    enemies = []
    # Se define la oleada como 5
    oleada = 5
    # Se define la velocidad del enemigo.
    enemy_vel = 3
    # Se define la velocidad del jugador.
    player_vel = 7
    # Se define la velocidad de los lasers.
    laser_vel = 7
    # Se crea al jugador llamando la clase Player
    player = Player(300, 630)
    # Se define un reloj para que siga el tie
    reloj = pygame.time.Clock()
    # Se define perder como False.
    perder = False
    # Se crea una variable tiempo_perder y se inicia en 0.
    tiempo_perder = 0
    # Se verifica si el archivo existe o no.
    if os.path.exists("highest score.txt"):
        # Se abre el archivo del highscore
        with open("highest score.txt", "r") as file:
            # Se lee el archivo y se asigna a high_score.
            high_score = int(file.read())
    # Si no encuentra ningun archivo se asigna un valor de 0 a high_score.
    else:
        high_score = 0
    # Se asigna un metodo para el menu de pausa.

    def pause():
        paused = True
        while paused:
            # Se pone un titulo para el usuario sepa que esta en el menu de
            # pausa
            title_sec = pygame.font.SysFont("comicsans", 50)
            WIN.blit(BG, (0, 0))
            title_label = title_sec.render("Presion C para continuar o Q"
                                           " para salir ", 1, (255, 255, 255))
            WIN.blit(title_label, (ancho/2 - title_label.get_width()/2, 350))
            pygame.display.update()
            for event in pygame.event.get():
                # Se define que se hara si se presiona la letra c o q.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
            # Se actualiza la pantalla
            pygame.display.update
            reloj.tick(5)

    # Se redibuja la ventana.
    def redraw_ventana():
        # Se crea la superficie del fondo en la ventana principal.
        WIN.blit(BG, (0, 0))
        # Se ponene los textos de la pantalla
        nivel_label = main_font.render(f"Nivel: {nivel}", 1,
                                       (255, 255, 255))
        score_label = main_font.render(f"Score: {player.score}", 1,
                                       (255, 255, 255))
        highscore_label = main_font.render(f"Highscore: {high_score}",
                                           1, (255, 255, 255))

        # Se ubican los textos en la pantalla.
        WIN.blit(nivel_label, (ancho - nivel_label.get_width() - 10, 10))
        WIN.blit(score_label, (10, 10))
        WIN.blit(highscore_label, (10, 60))

        # Se dibujan los enemigos de la oleada
        for enemy in enemies:
            enemy.draw(WIN)
        # Se dibuja al jugador
        player.draw(WIN)

        # Si se pierde se pone el texto de "Game Over"
        if perder:
            perder_label = lost_font.render("Game Over", 1, (255, 255, 255))
            WIN.blit(perder_label, (ancho/2 - perder_label.get_width()/2, 350))
            # Un segundo de perder suena el sonido game over.
            if tiempo_perder == FPS * 1:
                gameoverSound.play()

        # Se actualiza la pantalla
        pygame.display.update()

    # Se inicia el ciclo del juego.
    while run:
        # La pantalla se actualiza 60 segundos por segundo.
        reloj.tick(FPS)
        redraw_ventana()

        # Si la salud del jugador es igual o menor a 0 se pierde.
        if player.salud <= 0:
            perder = True
            # El tiempo contar se aumenta en 1.
            tiempo_perder += 1

        # Se espera 3 segundos para terminar el ciclo.
        if perder:
            if tiempo_perder > FPS * 3:
                run = False
            else:
                continue
        # Si los enemigos llegan a 0 el nivel aumenta en 1 y la oleada aumenta
        # En 5.
        if len(enemies) == 0:
            nivel += 1
            oleada += 5
            # Se crean los enenmigos que se encuentran en la oleada.
            # La ubicacion en "x", en "y" y el color de la nave son randoms.
            for i in range(oleada):
                enemy = Enemy(random.randrange(50, ancho-100),
                              random.randrange(-1500, -100),
                              random.choice(["red", "blue", "green"]))
                # Se añaden los enemigos a la lista de enemies.
                enemies.append(enemy)

        # Se define el comando de salir al presionar la X de la ventana.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        # Se obtienen todas las teclas y sus funciones
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:   # izquierda
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + \
                player.get_width() < ancho:   # derecha
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:   # arriba
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + \
                player.get_height() + 15 < altura:   # abajo
            player.y += player_vel
        if keys[pygame.K_SPACE]:  # disparar
            player.shoot()
            laserSound.play()
        if keys[pygame.K_p]:   # Pausa
            pause()
        # Cada enemigo se tiene que mover al igual que los lasers.
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            # Se define un tiempo aleatorio para que el enemigo dispare.
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            # Si el jugador chocha con una nave
            # Se restan 10 a la salud y se elimina la nave de la lista.
            if collide(enemy, player):
                player.salud -= 10
                # Suena el sonido explosion si dos naves chocan
                explosionSound.play()
                # Se elimina la nave de la lista.
                enemies.remove(enemy)

            # Si el enemigo se sale de la pantalla se elimina de la lista.
            elif enemy.y + enemy.get_height() > altura:
                enemies.remove(enemy)

        # El laser del jugador se mueve hacia arriba.
        player.move_lasers(-laser_vel, enemies)

        # Si el score es mayor al highscore
        # Se le da el valor de score.
        if player.score > high_score:
            high_score = player.score
            # Se abre el archivo y se escribe el valor.
            with open("highest score.txt", "w") as file:
                file.write(str(high_score))

# Se define la funcion de main_menu.


def main_menu():
    # Se define la fuente del titulo.
    fuente_titulo = pygame.font.SysFont("comicsans", 60)
    # Se define el run como True.
    run = True
    # Se inicia el ciclo.
    while run:
        # Se crea la venana con el fondo.
        WIN.blit(BG, (0, 0))
        # Se crea el titulo.
        texto_titulo = fuente_titulo.render("Presiona el mouse para empezar",
                                            1, (255, 255, 255))
        # Se ubica el titulo.
        WIN.blit(texto_titulo, (ancho/2 - texto_titulo.get_width()/2, 350))
        # Se actualiza la pantalla.
        pygame.display.update()
        # Se crea el evento para cerrar el juego.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Si se pulsa el boton del mouse inicia el programa.
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    # Se cierra pygame.
    pygame.quit()

# Se inicia el main_menu


main_menu()
