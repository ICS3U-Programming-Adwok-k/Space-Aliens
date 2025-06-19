#!/usr/bin/env python3
# Created by: Adwok Adiebo
# Date: June 6th, 2025
#
# This program creates a space aliens game.

import ugame
import stage
import time
import constants
import random


def splash_scene():
    # This function is the splash scene that displays the game studio logo and plays a sound.

    # An image bank for CircuitPython, loading the background image for the splash scene.
    image_bank_mt_background = stage.Bank.from_bmp16(
        "mt_game_studio.bmp")

    # Get sound ready: open the coin sound file, stop any current audio, unmute, and play the sound.
    coin_sound = open("coin.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    sound.play(coin_sound)

    # Set the background to image 0 in the bank, creating a grid for the splash screen background.
    background = stage.Grid(image_bank_mt_background,
                            constants.SCREEN_X, constants.SCREEN_Y)

    # These lines tile the background image to form the MT Game Studio logo, utilizing a sprite cutter program.
    background.tile(2, 2, 0)  # blank white
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)  # blank white

    background.tile(2, 3, 0)  # blank white
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)  # blank white

    background.tile(2, 4, 0)  # blank white
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)  # blank white

    background.tile(2, 5, 0)  # blank white
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)  # blank white

    # Create the game stage with the display and set the frame rate.
    game = stage.Stage(ugame.display, constants.FPS)

    # Set the layers for the game, with the background at the bottom.
    game.layers = [background]

    # Render the initial block (background).
    game.render_block()

    # Repeat forever in the game loop.
    while True:
        # Wait for 2 seconds.
        time.sleep(2.0)
        # Transition to the menu scene.
        menu_scene()


def menu_scene():
    # This function is the menu scene where the player can choose to start the game.

    # Image bank for CircuitPython, loading the background image for the menu.
    image_bank_background = stage.Bank.from_bmp16(
        "mt_game_studio.bmp")

    # Initialize an empty list to hold text objects.
    text = []
    # Create the first text object for the game studio title.
    text1 = stage.Text(width=29, height=12, font=None,
                       palette=constants.RED_PALETTE, buffer=None)
    text1.move(20, 10)  # Position the text.
    text1.text("MT Game Studios")  # Set the text content.
    text.append(text1)  # Add text1 to the list.

    # Create the second text object for the "PRESS START" prompt.
    text2 = stage.Text(width=29, height=12, font=None,
                       palette=constants.RED_PALETTE, buffer=None)
    text2.move(40, 110)  # Position the text.
    text2.text("PRESS START")  # Set the text content.
    text.append(text2)  # Add text2 to the list.

    # Create the background grid for the menu scene.
    background = stage.Grid(image_bank_background,
                            constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    # Create the game stage with the display and set the frame rate.
    game = stage.Stage(ugame.display, constants.FPS)

    # Set the layers for the game, with text on top of the background.
    game.layers = text + [background]

    # Render the initial block (background and text).
    game.render_block()

    # Game loop for the menu scene.
    while True:
        # Get the user input from the buttons.
        keys = ugame.buttons.get_pressed()

        # Check if the START button is pressed.
        if keys & ugame.K_START != 0:
            game_scene()  # Call the game scene function to start the game.

        # Redraw sprites.
        game.tick()  # Update the display based on the defined FPS.


def game_scene():
    # This function is the main game scene where the actual gameplay occurs.

    # Initialize the score for the game.
    score = 0

    def show_alien():
        # This function takes an alien from off screen and moves it on screen.
        # Iterate through the list of aliens.
        for alien_number in range(len(aliens)):
            # If an alien is off-screen to the left (x < 0), it's available to be moved.
            if aliens[alien_number].x < 0:
                # Move the alien to a random X position on screen and off-screen at the top, making it appear to fall.
                aliens[alien_number].move(random.randint(0 + constants.SPRITE_SIZE,
                                                         constants.SCREEN_X - constants.SPRITE_SIZE),
                                          constants.OFF_TOP_SCREEN)
                break  # Exit the loop after finding and moving one alien.

    # Load image banks for the game background and sprites.
    image_bank_background = stage.Bank.from_bmp16(
        "space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # Initialize the state of all relevant buttons to "button_up".
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # Get sound ready: open the "pew" sound file for laser, stop any current audio, and unmute.
    pew_sound = open("pew.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # Create the background grid using the loaded background image bank.
    background = stage.Grid(image_bank_background,
                            constants.SCREEN_GRID_X, constants.SCREEN_GRID_X)

    # Populate the background with randomly chosen tiles to create a varied environment.
    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_Y):
            # Pick a random tile from 1 to 3.
            tile_picked = random.randint(1, 3)
            background.tile(x_location, y_location, tile_picked)

    # Create the player's ship sprite, setting its initial image, X position, and Y position.
    ship = stage.Sprite(image_bank_sprites, 5, 75,
                        constants.SCREEN_Y - (2 * constants.SPRITE_SIZE))

    # Create a list to hold alien sprites.
    aliens = []
    # Loop to create and initialize the total number of aliens.
    for alien_number in range(constants.TOTAL_NUMBER_OF_ALIENS):
        # Create each alien sprite, using image 9 from the sprite bank, and place it off-screen initially.
        a_single_alien = stage.Sprite(image_bank_sprites, 9,
                                      constants.OFF_SCREEN_X,
                                      constants.OFF_SCREEN_Y)

        # Add the newly created alien to the list.
        aliens.append(a_single_alien)
    # Place 1 alien on the screen to start the game.
    show_alien()

    # Create a list to hold laser sprites.
    lasers = []
    # Loop to create and initialize the total number of lasers.
    for laser_number in range(constants.TOTAL_NUMBER_OF_LASERS):
        # Create each laser sprite, using image 10 from the sprite bank, and place it off-screen initially.
        a_single_laser = stage.Sprite(image_bank_sprites, 10,
                                      constants.OFF_SCREEN_X,
                                      constants.OFF_SCREEN_Y)

        # Add the newly created laser to the list.
        lasers.append(a_single_laser)

    # Create the game stage with the display and set the frame rate.
    game = stage.Stage(ugame.display, constants.FPS)

    # Set the layers for the game. Sprites are rendered in the order they appear in this list (from back to front).
    game.layers = lasers + [ship] + aliens + [background]

    # Render the background and the initial location of all sprites.
    game.render_block()

    # Main game loop for continuous gameplay.
    while True:
        # Get the current state of all buttons pressed by the user.
        keys = ugame.buttons.get_pressed()
        # Handle the state transitions for the A button (ugame.K_X).
        if keys & ugame.K_X != 0:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
            elif a_button == constants.button_state["button_just_pressed"]:
                a_button = constants.button_state["button_still_pressed"]
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]
        # Handle the B button (ugame.K_O) - currently does nothing.
        if keys & ugame.K_O != 0:
            pass
        # Handle the START button - prints "Start" to the console.
        if keys & ugame.K_START != 0:
            print("Start")

        # Handle the SELECT button - prints "Select" to the console.
        if keys & ugame.K_SELECT != 0:
            print("Select")

        # Handle moving the ship to the right.
        if keys & ugame.K_RIGHT != 0:
            # Check if the ship is within the screen bounds before moving.
            if ship.x < (constants.SCREEN_X - constants.SPRITE_SIZE):
                ship.move((ship.x + constants.SPRITE_MOVEMENT_SPEED), ship.y)
            else:
                # If at the edge, keep the ship at the rightmost position.
                ship.move((constants.SCREEN_X - constants.SPRITE_SIZE), ship.y)

        # Handle moving the ship to the left.
        if keys & ugame.K_LEFT != 0:
            # Check if the ship is within the screen bounds before moving.
            if ship.x >= 0:
                ship.move((ship.x - constants.SPRITE_MOVEMENT_SPEED), ship.y)
            else:
                # If at the edge, keep the ship at the leftmost position.
                ship.move(0, ship.y)

        # Handle the UP button - currently does nothing.
        if keys & ugame.K_UP != 0:
            pass

        # Handle the DOWN button - currently does nothing.
        if keys & ugame.K_DOWN != 0:
            pass

        # Update game logic:
        # Play sound and fire a laser if the A button was just pressed.
        if a_button == constants.button_state["button_just_pressed"]:
            # Iterate through the lasers to find an available one (off-screen).
            for laser_number in range(len(lasers)):
                if lasers[laser_number].x < 0:  # If a laser is off-screen.
                    # Move it to the ship's position to fire.
                    lasers[laser_number].move(ship.x, ship.y)
                    sound.play(pew_sound)  # Play the laser sound.
                    break  # Fire only one laser at a time.

        # Each frame, move the lasers that have been fired upwards.
        for laser_number in range(len(lasers)):
            # If a laser is currently on-screen.
            if lasers[laser_number].x > 0:
                lasers[laser_number].move(lasers[laser_number].x,
                                          lasers[laser_number].y -
                                          # Move it up by the laser speed.
                                          constants.LASER_SPEED)

                # If the laser goes off the top of the screen, move it back off-screen to be reused.
                if lasers[laser_number].y < constants.OFF_TOP_SCREEN:
                    lasers[laser_number].move(constants.OFF_SCREEN_X,
                                              constants.OFF_SCREEN_Y)

        # Each frame, move the aliens downwards if they are on the screen.
        for alien_number in range(len(aliens)):
            # If an alien is currently on-screen.
            if aliens[alien_number].x > 0:
                aliens[alien_number].move(aliens[alien_number].x,
                                          aliens[alien_number].y +
                                          # Move it down by the alien speed.
                                          constants.ALIEN_SPEED)

                # If the alien goes off the bottom of the screen, move it back off-screen and show a new one.
                if aliens[alien_number].y > constants.SCREEN_Y:
                    aliens[alien_number].move(constants.OFF_SCREEN_X,
                                              constants.OFF_SCREEN_Y)
                    show_alien()  # Bring a new alien on screen.

        # Each frame, check for collisions between lasers and aliens.
        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:  # Only check active lasers.
                for alien_number in range(len(aliens)):
                    if aliens[alien_number].x > 0:  # Only check active aliens.
                        # Perform collision detection using adjusted sprite boundaries.
                        if stage.collide(lasers[laser_number].x + 6, lasers[laser_number].y + 2,
                                         lasers[laser_number].x +
                                         11, lasers[laser_number].y + 12,
                                         aliens[alien_number].x +
                                         1, aliens[alien_number].y,
                                         aliens[alien_number].x + 15, aliens[alien_number].y + 15):
                            # If a collision occurs, it means "you hit an alien".
                            # Move both the alien and the laser off-screen.
                            aliens[alien_number].move(
                                constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                            lasers[laser_number].move(
                                constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                            # Stop any current sound and play a "boom" sound effect.
                            sound.stop()
                            # Assumes 'boom_sound' is defined and loaded similarly to 'pew_sound'.
                            # If 'boom_sound' is not defined, this line will cause an error.
                            # boom_sound = open("boom.wav", 'rb') # This line might be needed if boom_sound isn't loaded elsewhere.
                            # sound.play(boom_sound)
                            show_alien()  # Bring a new alien on screen.
                            show_alien()  # Bring another new alien on screen.
                            score = score + 1  # Increment the player's score.

        # Render all sprites on the screen for the current frame.
        game.render_sprites(lasers + [ship] + aliens)
        # Update the display based on the frame rate and wait if necessary.
        game.tick()


if __name__ == "__main__":
    # Start the game by calling the splash scene function when the script is executed.
    splash_scene()
