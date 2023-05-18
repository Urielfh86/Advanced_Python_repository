import pygame
import random
from shmup.fps_stats import FPSStats
from shmup.config import cfg_item
from importlib import resources
from shmup.entities.avion import Avion
from shmup.entities.rendergroup import RenderGroup
from shmup.entities.enemy import Enemy
from shmup.entities.Projectiles.projectile_factory import ProjectileType, ProyectileFactory

class Game:
    def __init__(self):
        pygame.init()

        # Creo mi ventana de visualización 
        # En el "0" van los FLAGS para la creación de una ventana (FULLSCREEN, etc) y el "32" es la profundiad de color de la ventana, en este caso son 32 bits.
        self.__screen = pygame.display.set_mode(cfg_item("game", "screen_size"), 0, 32)

        with resources.path(cfg_item("font", "font_file")[0], cfg_item("font", "font_file")[1]) as font_file:
            # Cargo mi fuente de letra. El * es para desempaquetar los argumentos de la ruta.
            font = pygame.font.Font(font_file, cfg_item("font", "font_size"))
        
        self.__fps_stats = FPSStats(font)
        self.__players = RenderGroup()
        self.__players.add(Avion(self.__screen, self.spawn_projectile))
        self.__enemies = RenderGroup()
        self.__allies_projectiles = RenderGroup()
        self.__enemies_projectiles = RenderGroup()

        self.__running = False


    def run(self):
        print("\nRunning ShMUp game.")
        pygame.display.set_caption(cfg_item("game", "title"))

        # Bucle principal del juego
        self.__running = True

        last_time = pygame.time.get_ticks()
        time_since_last_update = 0
        while self.__running:
            delta_time, last_time = self.__calc_delta_time(last_time) 
            time_since_last_update += delta_time
            
            while time_since_last_update > cfg_item("timing", "time_per_frame"):
                time_since_last_update -= cfg_item("timing", "time_per_frame")
                self.__process_inputs()
                self.__update(cfg_item("timing", "time_per_frame"))
            
            self.__render()

        self.__quit()
    
    def __process_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            if event.type == pygame.KEYDOWN:
                self.__players.input(event.key, True)
            if event.type == pygame.KEYUP:
                self.__players.input(event.key, False)

    def __update(self, delta_time):
        self.__players.update(delta_time)
        self.__enemies.update(delta_time)
        self.__allies_projectiles.update(delta_time)
        self.__enemies_projectiles.update(delta_time)
        self.__fps_stats.update(delta_time)

        self.__spawn_enemy()
        self.__check_collisions()

    def __render(self):
        # Pinto la pantalla con el color que le indique (borra lo que había)
        self.__screen.fill(cfg_item("game", "background_color"))
        self.__players.draw(self.__screen)
        self.__enemies.draw(self.__screen)
        self.__allies_projectiles.draw(self.__screen)
        self.__enemies_projectiles.draw(self.__screen)
        self.__fps_stats.render(self.__screen)

        # Actualizo la pantalla con toda la nueva información recolectada en la iteración del bucle for
        pygame.display.update() 

    # Método de clase, privado "__". No se accede desde fuera de la clase. 
    def __quit(self):
        self.__players.empty()
        self.__enemies.empty()
        self.__allies_projectiles.empty()
        self.__enemies_projectiles.empty()
        pygame.quit()
    
    def __calc_delta_time(self, last_time):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_time
        return delta_time, current_time
        
    def __spawn_enemy(self):
        if random.random() <= cfg_item("entities", "enemy", "spawn_prob"):
            self.__enemies.add(Enemy(self.spawn_projectile))

    def __check_collisions(self):
        for player, enemies in pygame.sprite.groupcollide(self.__players, self.__enemies, False, True).items():
            print(f"Crash")
        
        for player, enemy_proyectile in pygame.sprite.groupcollide(self.__players, self.__enemies_projectiles, False, True).items():
            print("Enemy bullet impact")

        for enemy, allies_projectile in pygame.sprite.groupcollide(self.__enemies, self.__allies_projectiles, True, True).items():
            print(f"Enemy killed")

    def spawn_projectile(self, type, position):
        if type == ProjectileType.AlliedProyectile:
            new_projectile = ProyectileFactory.create_projectile(type, position)
            self.__allies_projectiles.add(new_projectile)
        elif type == ProjectileType.EnemyProjectile:
            new_projectile = ProyectileFactory.create_projectile(type, position)
            self.__enemies_projectiles.add(new_projectile)