from enum import Enum
from shmup.entities.Projectiles.projectile_allied import ProjectileAllied
from shmup.entities.Projectiles.proyectile_enemy import ProjectileEnemy

class ProjectileType(Enum):
    AlliedProyectile = 0,
    EnemyProjectile = 1

class ProyectileFactory():

    @staticmethod
    def create_projectile(type, position):
        if type == ProjectileType.AlliedProyectile:
            return ProjectileAllied(position)
        elif type == ProjectileType.EnemyProjectile:
            return ProjectileEnemy(position)