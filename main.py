import random
from modules import Engine
from modules.gameobject import GameObject
from modules.structs.vector import Vector2
from modules.utilities import Asset_Loader
from modules.sfx import SFX

from game.player import Player
from game.pipe_line import Pipe_Line, Pipe_Line_Manager
from game.background import Background
from game.score_display import Score_Display
from game.ui_screens import UI_Overlay

# * --- initialise engine
Engine.initialize()

# * --- Create Objects
# create backgrounds
level_background = Background("background-day.png", 0.1, Engine.screen_size.y)
Engine.objects.append(level_background)
# create pipes
pipeline_manager = Pipe_Line_Manager(3)
Engine.objects.append(pipeline_manager)
# create ground
ground_height = 100
ground = Background("base.png", 1.5, ground_height)
for i in range(len(ground.children)):
    obj = ground.children[i]
    obj.position.y = Engine.screen_size.y - ground_height
ground.can_be_collided = True
# make sure all ground rects can be collided with
for c in ground.children:
    c.can_be_collided = True
Engine.objects.append(ground)
# create player
player = Player()
player.size = Vector2(55, 50)
player.is_checking_for_collisions = True
player.render_image = True
player.render_rect = False
Engine.objects.append(player)
# create main score display
score_display = Score_Display()
score_display.position = Vector2(
    (Engine.screen_size.x/2) - (score_display.children[0].size.x * 1.5),
    100
)
Engine.objects.append(score_display)
# create ui
# start overlay
start_screen = UI_Overlay("message.png")
start_screen.visible = False
Engine.objects.append(start_screen)
# game over screen
game_over_screen = UI_Overlay("gameover.png")
Engine.objects.append(game_over_screen)
# score display in game over screen
gameover_score_display = Score_Display()
gameover_score_display.position = Vector2(
    (Engine.screen_size.x/2) - (score_display.children[0].size.x * 1.5),
    (Engine.screen_size.y/2) + 50
)
game_over_screen.children.append(gameover_score_display)


# * --- create game sfx
SFX("hit", "hit.wav")
SFX("point", "point.wav")
SFX("wing", "wing.wav")

# * --- track important game state
current_score = 0
def update_game_score(num):
    global current_score
    current_score = num
    gameover_score_display.display_number(num)
    score_display.display_number(num)

# * --- create events:
# player events
def on_player_collide_with_gap():
    SFX.play("point")
    update_game_score(current_score + 1)
def on_player_collide_with_env():
    SFX.play("hit")
    on_game_end()
player.on_player_collide_with_gap = on_player_collide_with_gap
player.on_player_collide_with_pipe = on_player_collide_with_env

# listening to ui input events
def on_application_start():
    # update currents core
    update_game_score(0)
    # turn off the game over screen
    game_over_screen.visible = False
    gameover_score_display.visible = False
    game_over_screen.active = False
    gameover_score_display.active = False
    # turn on the start screen
    start_screen.visible = True
    start_screen.active = True
    # disable the players
    player.active = False
    # disable the env
    pipeline_manager.active = False
def on_game_start():
    # clear player collision history
    player.previous_collided_id = None
    # turn on the start screen
    start_screen.visible = False
    start_screen.active = False
    # reest the envs
    pipeline_manager.active = True
    pipeline_manager.reset()
    # reset the player
    player.position.x = Engine.screen_size.x/2
    player.position.y = Engine.screen_size.y/2
    player.active = True
def on_game_end():
    # turn off the game over screen
    game_over_screen.visible = True
    gameover_score_display.visible = True
    game_over_screen.active = True
    gameover_score_display.active = True
    # disable the players
    player.active = False
    # disable the env
    pipeline_manager.active = False
# make ui screen listen to ui events
# start screen
start_screen.on_input_received = on_game_start
game_over_screen.on_input_received = on_application_start
# game over screen


# * --- start the game
on_application_start()
Engine.start()