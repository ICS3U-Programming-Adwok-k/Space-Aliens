#!/usr/bin/env python3
# Created by: Adwok Adiebo
# Date: June 6th, 2025
#
# This program creates a basic space aliens game scene.

import ugame    # Imports the ugame library for game functionalities
import stage    # Imports the stage library for sprite and background management
import constants  # Imports custom constants for game settings


def game_scene():
    """
    Main function for the game's core gameplay scene.
    Initializes game elements, handles input, and updates display.
    """

    # Load background and sprite images into memory banks
    image_bank_background = stage.Bank.from_bmp16(
        "space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # Initialize button state variables for tracking presses
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # Load sound effect and configure audio
    pew_sound = open("pew.wav", 'rb')  # Opens the laser sound file
    sound = ugame.audio             # Gets the ugame audio object
    sound.stop()                    # Stops any current audio playback
    sound.mute(False)               # Unmutes the audio

    # Create the scrolling background grid
    background = stage.Grid(image_bank_background, 10, 8)

    # Initialize the player's spaceship sprite
    ship = stage.Sprite(image_bank_sprites, 5, 75,
                        constants.SCREEN_Y - (2 * constants.SPRITE_SIZE))

    # Initialize a single alien sprite
    alien = stage.Sprite(image_bank_sprites, 9, int(
        constants.SCREEN_X / 2 - constants.SPRITE_SIZE / 2), 16)

    # Create the game stage and set the frame rate
    game = stage.Stage(ugame.display, constants.FPS)

    # Define the drawing order of game layers (ship, alien, then background)
    game.layers = [ship] + [alien] + [background]

    # Render the initial game state (background and sprites)
    game.render_block()

    # Main game loop
    while True:
        # Get current button input states
        keys = ugame.buttons.get_pressed()

        # Handle A button (ugame.K_X) state transitions for single presses
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

        # Handle B button (ugame.K_O) - currently no action
        if keys & ugame.K_O != 0:
            pass
        # Handle START button - prints to console
        if keys & ugame.K_START != 0:
            print("Start")

        # Handle SELECT button - prints to console
        if keys & ugame.K_SELECT != 0:
            print("Select")

        # Ship movement to the right
        if keys & ugame.K_RIGHT != 0:
            if ship.x < (constants.SCREEN_X - constants.SPRITE_SIZE):
                ship.move((ship.x + constants.SPRITE_MOVEMENT_SPEED), ship.y)
            else:
                ship.move((constants.SCREEN_X - constants.SPRITE_SIZE), ship.y)

        # Ship movement to the left
        if keys & ugame.K_LEFT != 0:
            if ship.x >= 0:
                ship.move((ship.x - constants.SPRITE_MOVEMENT_SPEED), ship.y)
            else:
                ship.move(0, ship.y)

        # Up button
        if keys & ugame.K_UP != 0:
            pass

        # Down button 
        if keys & ugame.K_DOWN != 0:
            pass

        # Play laser sound if A button was just pressed
        if a_button == constants.button_state["button_just_pressed"]:
            sound.play(pew_sound)

        # Render/redraw ship and alien sprites
        game.render_sprites([ship] + [alien])
        # Update display and maintain frame rate
        game.tick()


# Program entry point: starts the game scene
if __name__ == "__main__":
    game_scene()
