from figure_class import Asteroid, Spaceship, Planet
import pygame as pg
import random
from record_syst import TextBox
pg.init()

WIDTH, HEIGHT = 1024, 600  # Screen dimensions
main_screen = pg.display.set_mode((WIDTH, HEIGHT))  # Initialize display

# Set up the images
backgroundImage = pg.transform.scale(pg.image.load("images/universe_bg_01.png").convert_alpha(), (1024, 600))
backgroundImage2 = pg.transform.scale(pg.image.load("images/universe_bg_04.png").convert_alpha(), (1024, 600))
backgroundImage3 = pg.transform.scale(pg.image.load("images/universe_bg_03.png").convert_alpha(), (1024, 600))
menuImage = pg.transform.scale(pg.image.load("images/universe_bg_02.png").convert_alpha(), (1024, 600))

pg.display.set_caption("Scape from Home")

# Set up the fonts used
game_font = pg.font.Font('sofachrome rg.otf', 18)
menu_font = pg.font.Font('sofachrome rg.otf', 26)

# Method to draw text on the screen
def text(x: int, y: int, col: str, text: str, surface, font):
    img = font.render(text, True, col)
    surface.blit(img, (x, y))


# Set the FPS
crono = pg.time.Clock()

# Create the list of asteroids in this level
asteroidCluster = pg.sprite.Group()
spaceship = Spaceship(100, 300)  # the spaceship
landing_planet = pg.sprite.Group(Planet(WIDTH, HEIGHT//2))  # the planet

# Set up the conditions
game_over = False
start_game = False
spawn_timer = 0
running = True
show_menu = True
show_top_scores = False
show_instructions = False
completed = False
enter_name = True
level = 1

# Main loop of the game
while running:
    # Set the FPS
    fps = crono.tick(60)

    # If the timer is not the max and the player is alive, increase the timer
    if spawn_timer < 3000 and spaceship.lives > 0:
        spawn_timer += 1
    keys = pg.key.get_pressed()

    # Control to catch the end of the game
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Control the start of the game
    if start_game:
        # Control the lives of the spaceship
        if spaceship.lives == 0:
            game_over = True

        # Draw the elements
        main_screen.blit(pg.transform.scale(pg.image.load(f"images/universe_bg_0{level}.png").convert_alpha(), (1024, 600)), (0, 0))
        spaceship.draw(main_screen)  # Draw the SpaceShip
        spaceship.update(asteroidCluster)  # Move the SpaceShip
        for a in asteroidCluster:  # Draw the asteroids
            if spawn_timer < 3000:
                a.draw(main_screen)
                a.update(spaceship)

        # Set the text
        text(50, 50, 'red',
             f'LIVES LEFT: {spaceship.lives}', main_screen, game_font)
        text(50, 70, 'yellow',
             f'POINTS: {spaceship.points}', main_screen, game_font)
        text(50, 90, 'white', f'Level {level}', main_screen, game_font)
        text(50, 110, 'light blue',
             f'ETA : {int((3000-spawn_timer)/60)}', main_screen, game_font)

        # Control de spawning of the asteroids
        # More asteroids are added and drawn on screen with the increase of level
        if spawn_timer % int(60/level) == 0 and spawn_timer < 3000:
            asteroid = Asteroid(1024, random.randint(20, 550))
            asteroid.rect.left = 1024
            asteroidCluster.add(asteroid)

        # End of the game game and level progression control
        # Control of the completition of the level
        if spawn_timer >= 3000:
            # Clears the remaining asteroids on screen
            asteroidCluster = pg.sprite.Group()
            landing_planet.draw(main_screen)  # Draw the planet
            landing_planet.update(spaceship)  # Lands on the planet
            spaceship.control_ship = False  # Takes out the control of the spaceship
            if pg.sprite.spritecollide(spaceship, landing_planet, False, pg.sprite.collide_mask):
                spaceship.flip = True  # Flip the spaceship to land on the planet

                # Controls if it's the last level. If it's not, offers to go to the next level
                if level < 3:
                    text(WIDTH*0.33, HEIGHT*0.65, 'yellow',
                         'LEVEL COMPLETE!', main_screen, menu_font)
                    text(WIDTH*0.26, HEIGHT*0.75, 'red',
                         'PRESS N TO GO TO THE NEXT LEVEL', main_screen, game_font)                    
                    if keys[pg.K_n]:
                        # Reset the variables to preppare the next level
                        spawn_timer = 0
                        level += 1
                        spaceship.points += 50  # Bonus points for finishing the level
                        spaceship.lives = 3
                        landing_planet = pg.sprite.Group(Planet(WIDTH, HEIGHT//2))
                        spaceship.flip = False
                        spaceship.control_ship = True
                        spaceship.rect.x = 100
                else:
                    completed = True
            else:
                spaceship.rect.x += 3  # Moves the spaceship towards the planet

    # Menu
    if show_menu:
        main_screen.blit(menuImage, (0, 0))  # Set up the image for the menu
        # Print prompts
        text(WIDTH*0.12, HEIGHT*0.4, 'yellow',
             'THE SEARCH FOR ANOTHER PLANET', main_screen, menu_font)
        text(WIDTH*0.23, HEIGHT*0.55, 'red',
             'PRESS SPACE TO START THE GAME...', main_screen, game_font)
        text(WIDTH*0.27, HEIGHT*0.65, 'white',
             'PRESS S FOR THE TOP SCORES', main_screen, game_font)
        # Show instructions when space is pressed
        if keys[pg.K_SPACE]:
            show_instructions = True
            show_menu = False
        # Show high scores when s in pressed
        elif keys[pg.K_s]:
            show_top_scores = True
            show_menu = False

    if show_instructions:
        main_screen.blit(menuImage, (0, 0))
        text(WIDTH*0.08, HEIGHT*0.4, 'yellow',
             'Move up and down using arrows', main_screen, menu_font)
        text(WIDTH*0.25, HEIGHT*0.5, 'yellow',
             'Avoid all asteroids!', main_screen, menu_font)
        text(WIDTH*0.33, HEIGHT*0.6, 'red',
             'PRESS C TO CONTINUE...', main_screen, game_font)
        if keys[pg.K_c]:  # Start the game
            show_instructions = False
            start_game = True

    if show_top_scores:
        get_information = TextBox(0)  # Used to get the high scores
        high_scores = get_information.records.get_scores()  # Get scores from the database
        main_screen.blit(backgroundImage3, (0, 0))
        text(WIDTH*0.38, HEIGHT*0.1, 'yellow', 'HIGHSCORES', main_screen, menu_font)
        text(WIDTH*0.3, HEIGHT*0.9, 'red', 'PRESS ESCAPE TO GO BACK...', main_screen, game_font)
        # Sort the list of previous records recived from the database by the score
        for x, score in enumerate(sorted(high_scores, key=get_information.takeSecond, reverse=True)):
            text(WIDTH*0.3, HEIGHT*(0.08*(x+1))+70, 'white', f'{score[0]}', main_screen, menu_font)
            text(WIDTH*0.65, HEIGHT*(0.08*(x+1))+70, 'white', f'{score[1]}', main_screen, menu_font)
        if keys[pg.K_ESCAPE]:  # Goes back to menu
            show_top_scores = False
            show_menu = True

    # Game over
    if game_over:
        start_game = False  # Ends the game
        # Display the message
        main_screen.fill('black')
        text(WIDTH*0.33, HEIGHT*0.4, 'red', 'MISSION FAILED!', main_screen, menu_font)
        text(WIDTH*0.34, HEIGHT*0.5, 'white', 'PRESS C TO CONTINUE...', main_screen, game_font)
        if keys[pg.K_c]:
            enter_information = TextBox(spaceship.points)  # Prompt to enter the name
            if enter_name:
                enter_information.enter_info()  # Sets the name and score into the database
                enter_name = False
            # Reset variables
            asteroidCluster = pg.sprite.Group()
            spaceship = Spaceship(100, 300)
            show_menu = True
            level = 1
            enter_name = True
            game_over = False
            spawn_timer = 0

    # When the game is completed
    if completed:
        start_game = False
        main_screen.fill('black')
        text(WIDTH*0.28, HEIGHT*0.4, 'yellow', 'MISSION SUCCESSFUL!', main_screen, menu_font)
        text(WIDTH*0.34, HEIGHT*0.5, 'white', 'PRESS C TO CONTINUE...', main_screen, game_font)
        if keys[pg.K_c]:
            enter_information = TextBox(spaceship.points)
            if enter_name:
                enter_information.enter_info()
                enter_name = False
            asteroidCluster = pg.sprite.Group()
            spaceship = Spaceship(100, 300)
            show_menu = True
            level = 1
            enter_name = True
            completed = False
            spawn_timer = 0

    pg.display.flip()
