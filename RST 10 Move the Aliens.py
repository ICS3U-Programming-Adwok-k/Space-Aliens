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
    # this function is the splash scene

    # an image bank for CircuitPython
    # Load the background image for the splash scene
    image_bank_mt_background = stage.Bank.from_bmp16(
        "mt_game_studio.bmp")

    # get sound ready
    # Open the coin sound file
    coin_sound = open("coin.wav", 'rb')
    sound = ugame.audio
    sound.stop()  # Stop any currently playing sound
    sound.mute(False)  # Unmute the audio
    sound.play(coin_sound)  # Play the coin sound

    # sets the background to image 0 in the bank
    # Create a grid for the background using the image bank
    background = stage.Grid(image_bank_mt_background,
                            constants.SCREEN_X, constants.SCREEN_Y)

    # used this program to split the image into tile:
    # https://ezgif.com/sprite-cutter/ezgif-5-818cdbcc3f66.png
    # These lines tile the background image to form the MT Game Studio logo
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

    # Create the game stage
    game = stage.Stage(ugame.display, constants.FPS)

    # Set the layers for the game, with background at the bottom
    game.layers = [background]

    # Render the initial block (background)
    game.render_block()

    # repeat forever, game loop
    while True:
        # wait for 2 seconds
        time.sleep(2.0)
        # Transition to the menu scene
        menu_scene()


def menu_scene():
    # this function is the main game scene

    # image banks for CircuitPython
    # Load the background image for the menu scene
    image_bank_background = stage.Bank.from_bmp16(
        "mt_game_studio.bmp")

    # add text objects
    text = []  # Initialize an empty list for text objects
    # Create the first text object
    text1 = stage.Text(width=29, height=12, font=None,
                       palette=constants.RED_PALETTE, buffer=None)
    text1.move(20, 10)  # Position the text
    text1.text("MT Game Studios")  # Set the text content
    text.append(text1)  # Add text1 to the list

    # Create the second text object
    text2 = stage.Text(width=29, height=12, font=None,
                       palette=constants.RED_PALETTE, buffer=None)
    text2.move(40, 110)  # Position the text
    text2.text("PRESS START")  # Set the text content
    text.append(text2)  # Add text2 to the list

    # Create the background grid
    background = stage.Grid(image_bank_background,
                            constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    # Create the game stage
    game = stage.Stage(ugame.display, constants.FPS)

    # Set the layers for the game, with text on top of the background
    game.layers = text + [background]

    # Render the initial block (background and text)
    game.render_block()

    # Game loop for the menu scene
    while True:
        # gets the user input
        keys = ugame.buttons.get_pressed()

        # Check if the START button is pressed
        if keys & ugame.K_START != 0:
            # Call the game scene function to start the game
            game_scene()

        # redraw sprites
        game.tick()  # Update the display based on FPS


def game_scene():
    # this function is the main game scene

    def show_alien():
        # this function takes an alien from off screen and moves it on screen
        # Iterate through the aliens list
        for alien_number in range(len(aliens)):
            # If an alien is off-screen to the left (x < 0)
            if aliens[alien_number].x < 0:
                # Move the alien to a random X position on screen and off-screen at the top
                aliens[alien_number].move(random.randint(0 + constants.SPRITE_SIZE,
                                                         constants.SCREEN_X - constants.SPRITE_SIZE),
                                          constants.OFF_TOP_SCREEN)
                break  # Exit the loop after finding and moving one alien

    # Load image banks for background and sprites
    image_bank_background = stage.Bank.from_bmp16(
        "space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # Initialize button states
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # Get sound ready for shooting
    pew_sound = open("pew.wav", 'rb')
    sound = ugame.audio
    sound.stop()  # Stop any current sound
    sound.mute(False)  # Unmute audio

    # Create the background grid
    background = stage.Grid(image_bank_background,
                            constants.SCREEN_GRID_X, constants.SCREEN_GRID_X)

    # Populate the background with random tiles
    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_Y):
            # Pick a random tile from 1 to 3
            tile_picked = random.randint(1, 3)
            background.tile(x_location, y_location, tile_picked)

    # Create the player's ship sprite
    ship = stage.Sprite(image_bank_sprites, 5, 75,
                        constants.SCREEN_Y - (2 * constants.SPRITE_SIZE))

    # create list of aliens
    aliens = []  # Initialize an empty list for aliens
    for alien_number in range(constants.TOTAL_NUMBER_OF_ALIENS):
        # Create each alien sprite and place it off-screen initially
        a_single_alien = stage.Sprite(image_bank_sprites, 9,
                                      constants.OFF_SCREEN_X,
                                      constants.OFF_SCREEN_Y)

        aliens.append(a_single_alien)  # Add the alien to the list
    # place 1 alien on the screen
    show_alien()  # Call the function to display one alien

    # create list of lasers for when we shoot
    lasers = []  # Initialize an empty list for lasers
    for laser_number in range(constants.TOTAL_NUMBER_OF_LASERS):
        # Create each laser sprite and place it off-screen initially
        a_single_laser = stage.Sprite(image_bank_sprites, 10,
                                      constants.OFF_SCREEN_X,
                                      constants.OFF_SCREEN_Y)

        lasers.append(a_single_laser)  # Add the laser to the list

    # Create the game stage
    game = stage.Stage(ugame.display, constants.FPS)

    # set the layers, items show up in order (from back to front)
    game.layers = lasers + [ship] + aliens + [background]

    # render the background and initial location of sprite list
    game.render_block()  # Render the initial display

    # Game loop for the main game scene
    while True:
        # gets the user input
        keys = ugame.buttons.get_pressed()
        # A button pressed states
        if keys & ugame.K_X != 0:  # Check if A button is pressed
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
            elif a_button == constants.button_state["button_just_pressed"]:
                a_button = constants.button_state["button_still_pressed"]
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]
        # B button pressed (currently does nothing)
        if keys & ugame.K_O != 0:
            pass
        # Start button pressed (prints "Start")
        if keys & ugame.K_START != 0:
            print("Start")

        # Select button pressed (prints "Select")
        if keys & ugame.K_SELECT != 0:
            print("Select")

        # Move ship right
        if keys & ugame.K_RIGHT != 0:
            # Check if ship is within screen bounds
            if ship.x < (constants.SCREEN_X - constants.SPRITE_SIZE):
                ship.move((ship.x + constants.SPRITE_MOVEMENT_SPEED), ship.y)
            else:
                # Keep ship at the right edge
                ship.move((constants.SCREEN_X - constants.SPRITE_SIZE), ship.y)

        # Move ship left
        if keys & ugame.K_LEFT != 0:
            # Check if ship is within screen bounds
            if ship.x >= 0:
                ship.move((ship.x - constants.SPRITE_MOVEMENT_SPEED), ship.y)
            else:
                # Keep ship at the left edge
                ship.move(0, ship.y)

        # Up button pressed (currently does nothing)
        if keys & ugame.K_UP != 0:
            pass

        # Down button pressed (currently does nothing)
        if keys & ugame.K_DOWN != 0:
            pass

        # update game logic
        # play sound if A was just button_just_pressed
        if a_button == constants.button_state["button_just_pressed"]:
            # fire a laser, if we have enough power (have not used up all the lasers)
            for laser_number in range(len(lasers)):
                if lasers[laser_number].x < 0:  # If a laser is off-screen
                    # Move it to the ship's position
                    lasers[laser_number].move(ship.x, ship.y)
                    sound.play(pew_sound)  # Play the laser sound
                    break  # Fire only one laser at a time

        # each frame move the lasers, that have been fired up
        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:  # If a laser is on-screen
                lasers[laser_number].move(lasers[laser_number].x,
                                          lasers[laser_number].y -
                                          constants.LASER_SPEED)  # Move it up

                # If laser goes off the top of the screen
                if lasers[laser_number].y < constants.OFF_TOP_SCREEN:
                    lasers[laser_number].move(constants.OFF_SCREEN_X,
                                              constants.OFF_SCREEN_Y)  # Move it off-screen

        # each frame move the aliens down, that are on the screen
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0:  # If an alien is on-screen
                aliens[alien_number].move(aliens[alien_number].x,
                                          aliens[alien_number].y +
                                          constants.ALIEN_SPEED)  # Move it down

                # If alien goes off the bottom of the screen
                if aliens[alien_number].y > constants.SCREEN_Y:
                    aliens[alien_number].move(constants.OFF_SCREEN_X,
                                              constants.OFF_SCREEN_Y)  # Move it off-screen
                    show_alien()  # Bring a new alien on screen

        # render sprites
        game.render_sprites(lasers + [ship] + aliens)  # Render all sprites
        game.tick()  # Update the display based on FPS


if __name__ == "__main__":
    splash_scene()  # Start the game with the splash scene
