
#!/usr/bin/env python3
# Created by: Adwok Adiebo
# Date: June 6th, 2025
#
# This program creates a menu scene and a game scene for a CircuitPython game.

import ugame
import stage
import constants


def menu_scene():
    # This function defines the main menu scene of the game.

    # Image bank for the background, loaded from a BMP file.
    image_bank_background = stage.Bank.from_bmp16(
        "mt_game_studio.bmp")

    # List to hold text objects.
    text = []

    # Create the first text object for the game title.
    # Set its width, height, font (None for default), palette, and buffer.
    text1 = stage.Text(width=29, height=12, font=None,
                       palette=constants.RED_PALETTE, buffer=None)

    # Set the x and y coordinates for the first text.
    text1.move(20, 10)
    # Set the text content.
    text1.text("MT Game Studios")
    # Add the text object to the list.
    text.append(text1)

    # Create the second text object for the "PRESS START" message.
    # Set its width, height, font (None for default), palette, and buffer.
    text2 = stage.Text(width=29, height=12, font=None,
                       palette=constants.RED_PALETTE, buffer=None)
    # Set the x and y coordinates for the second text.
    text2.move(40, 110)
    # Set the text content.
    text2.text("PRESS START")
    # Add the text object to the list.
    text.append(text2)

    # Create the background grid using the image bank and screen grid dimensions.
    background = stage.Grid(image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_X)

    # Initialize the game stage with the display and frames per second.
    game = stage.Stage(ugame.display, constants.FPS)

    # Set the layers for rendering: text on top of the background.
    game.layers = text + [background]

    # Render the initial block of layers.
    game.render_block()

    # Main loop for the menu scene.
    while True:
        # Get the current state of user input buttons.
        keys = ugame.buttons.get_pressed()

        # Check if the START button is pressed.
        if keys & ugame.K_START != 0:
            game_scene() 
            # Call the game scene function

        # Update the game display by ticking the stage.
        game.tick()


def game_scene():
    # This function defines the main game scene.

    # Image bank for the game background.
    image_bank_background = stage.Bank.from_bmp16(
        "space_aliens_background.bmp")
    # Image bank for sprites (e.g., ship, aliens).
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # Initialize button states.
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # Load and prepare sound effect.
    pew_sound = open("pew.wav", 'rb')
    sound = ugame.audio
    sound.stop()  # Stop any currently playing sound.
    sound.mute(False)  # Ensure sound is not muted.

    # Create the background grid.
    background = stage.Grid(image_bank_background, 10, 8)

    # Create the player's ship sprite.
    # Set its image bank, frame, initial x and y coordinates.
    ship = stage.Sprite(image_bank_sprites, 5, 75,
                        constants.SCREEN_Y - (2 * constants.SPRITE_SIZE))

    # Create an alien sprite.
    # Set its image bank, frame, initial x (centered), and y coordinates.
    alien = stage.Sprite(image_bank_sprites, 9, int(
        constants.SCREEN_X / 2 - constants.SPRITE_SIZE / 2), 16)

    # Initialize the game stage.
    game = stage.Stage(ugame.display, constants.FPS)

    # Set the rendering layers: ship and alien on top of the background.
    game.layers = [ship] + [alien] + [background]

    # Render the initial block of layers.
    game.render_block()

    # Main loop for the game scene.
    while True:
        # Get the current state of user input buttons.
        keys = ugame.buttons.get_pressed()

        # A button scenarios
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

        # B button
        if keys & ugame.K_O != 0:
            pass  

        # START button 
        if keys & ugame.K_START != 0:
            print("START")  

        # Select button 
        if keys & ugame.K_SELECT != 0:
            print("SELECT") 

        # right button movement
        if keys & ugame.K_RIGHT != 0:
            # Check if ship is within screen bounds before moving right.
            if ship.x < (constants.SCREEN_X - constants.SPRITE_SIZE):
                ship.move((ship.x + constants.SPRITE_MOVEMENT_SPEED), ship.y)
            else:
                # If at the right edge, keep it at the edge.
                ship.move((constants.SCREEN_X - constants.SPRITE_SIZE), ship.y)

        # Left button movement
        if keys & ugame.K_LEFT != 0:
            # Check if ship is within screen bounds before moving left.
            if ship.x >= 0:
                ship.move((ship.x - constants.SPRITE_MOVEMENT_SPEED), ship.y)
            else:
                # If at the left edge, keep it at the edge.
                ship.move(0, ship.y)

        # Handle UP arrow key input (currently does nothing).
        if keys & ugame.K_UP != 0:
            pass  

        # Handle DOWN arrow key input (currently does nothing).
        if keys & ugame.K_DOWN != 0:
            pass  

        # Play "pew" sound when A button is just pressed.
        if a_button == constants.button_state["button_just_pressed"]:
            sound.play(pew_sound)

        # Render the sprites.
        game.render_sprites([ship] + [alien])
        # Update the game display.
        game.tick()



if __name__ == "__main__":
    menu_scene()  