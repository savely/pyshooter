import pygame
from engine.map.map_manager import MapManager
from configs.config import Config 
from engine.collision.collision_resolver import CollisionResolver
from engine.entities.player import Player
from engine.entities.projectile import Projectile
from engine.entities.enemy import Enemy

class Game:
    """
    Owns the map manager and other global game state.
    """

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.config = Config()
        
        self.is_running = False
        self._init_map()
        self._init_groups()
        self._init_entities()
        self.is_running = True
        

    
    def _init_map(self) -> None:
        self._screen_size = self.config.screen_size
        self.map_manager = MapManager(self._screen_size)        
        self.game_map = self.map_manager.load(self.config.starting_map)
        self.camera = self.map_manager.camera
        self.walls = self.game_map.get_layer_rects(self.config.wall_layer_name)
    
    def _init_groups(self) -> None:
        self.player_group      = pygame.sprite.GroupSingle()
        self.enemy_group       = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.enemy_projectiles  = pygame.sprite.Group()
    
    def _init_entities(self) -> None:
        
        enemy_image = pygame.Surface((32, 32))
        enemy_image.fill('blue')
        
        player_image = pygame.Surface((32, 32))
        player_image.fill('red')
        
        self.bullet_image = pygame.Surface((8, 8))
        self.bullet_image.fill('yellow') 
        
        enemy = Enemy(
                position = self.game_map.get_spawn_point(self.config.enemy_spawn_point_name),
                image = enemy_image,
            )

        self.enemy_group.add(enemy)     
        self.camera.add(enemy)
        
        
        self.player = Player(
            position = self.game_map.get_spawn_point(self.config.player_spawn_point_name),
            image = player_image,   # replace with real asset
        )
        
        self.camera.add(self.player)
        self.player_group.add(self.player)

    def run(self) -> None:
        while self.is_running:
            dt = min(0.05, self.clock.tick(self.config.fps) / 1000.0)   # clamp: prevents tunnelling on lag spikes
            self._handle_events()
            self._update(dt)
            self._draw()
    
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False 
    
    def _update(self, dt: float) -> None:
        keys    = pygame.key.get_pressed()
        buttons = pygame.mouse.get_pressed()
        mouse_screen = pygame.Vector2(pygame.mouse.get_pos())
        mouse_world  = self.camera.screen_to_world(mouse_screen)

        # 1. Gather input → intent (no movement yet)
        self.player.handle_input(keys)
        self.player.handle_mouse(mouse_world, buttons)
        self.player.update(dt)
        
        # 2. Shooting Logic 
        if self.player.can_shoot():
            # Create the bullet at the player's position, firing in their facing direction
            new_bullet = Projectile(
                position=self.player.position.copy(),
                direction=self.player.facing,
                image=self.bullet_image,
                speed=self.config.bullet_speed,     
                damage=self.config.bullet_damage,
                owner_tag='player',
                lifetime=self.config.bullet_lifetime,      # Disappear after 2 seconds
            )
            
            # Add to the camera (for drawing) and the logic group (for collisions)
            self.camera.add(new_bullet)
            self.player_projectiles.add(new_bullet)
            
            # Tell the player they fired so the cooldown resets
            self.player.consume_shoot()

        # 3. Projectile Updates & Collisions 
        # Tick the lifetime countdown for all active projectiles
        for proj in self.player_projectiles:
            proj.update(dt)
            
        # Move projectiles and check for wall/enemy hits
        CollisionResolver.resolve_projectiles(
            projectiles=self.player_projectiles, 
            walls=self.walls, 
            target_groups=[self.enemy_group], # Will damage entities in this group
            dt=dt
        ) 
        for enemy in self.enemy_group:
            # 1. Check if this enemy can see the player
            can_see_player = CollisionResolver.has_line_of_sight(
                observer=enemy,
                target=self.player,
                walls=self.walls,
                max_distance=enemy.AGGRO_RANGE
            )
            
            # 2. Tell the enemy what to do
            if can_see_player:
                enemy.chase_target(self.player.position)
            else:
                enemy.cooldown(dt)  
                
            # 3. Tick enemy animation/cooldowns
            enemy.update(dt)

            # 4. Resolve Enemy Wall Collisions!
            CollisionResolver.resolve_entity(enemy, self.walls, dt)
            
             
        
        CollisionResolver.resolve_entity(self.player, self.walls, dt)
        self.camera.center_on(self.player)
    
    def _draw(self) -> None:
        self.screen.fill(self.config.bg_color)
        self.camera.draw(self.screen)
        pygame.display.flip()
        
        
if __name__ == "__main__":
    pygame.init()
    game = Game(pygame.display.set_mode(Config().screen_size))
    game.run()
    pygame.quit()
    exit()