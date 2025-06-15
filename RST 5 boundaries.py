import ugame
import stage
import constants  # Assuming this file exists and contains necessary constants


def game_scene():
    """
    This is the main function of the game scene where the actual gameplay occurs.
    """

    # Load image banks for the game background and sprites.
    # The image bank is used to grab the image
    image_bank_background = stage.Bank.from_bmp16(
        "space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # Create the background grid using the loaded background image bank.
    # Set the background to image 0 in the image bank and
    # size (10x8 tiles of size 16x16)
    background = stage.Grid(image_bank_background,
                            constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    # Create the player's ship sprite. A sprite that will be updated every frame.
    ship = stage.Sprite(image_bank_sprites, 5, 75,
                        constants.SCREEN_Y - (2 * constants.SPRITE_SIZE))

    # Create a stage for the background to show up on and set the frame rate to 60fps.
    game = stage.Stage(ugame.display, constants.FPS)

    # Set the layers of all sprites, items show up in order from bottom to top.
    # Note: This order might need adjustment based on how things should layer in front/behind each other. Typically background is last.
    game.layers = [ship] + [background]

    # Render all sprites and the background.
    game.render_block()

    # Repeat forever, game loop
    while True:
        # Get user input from the buttons.
        keys = ugame.buttons.get_pressed()

        # Handle the A button (ugame.K_X)
        # This will print A if the A button is being pressed
        if keys & ugame.K_X != 0:
            pass  # Placeholder for A button action (e.g., firing a laser)

        # Handle the B button (ugame.K_O)
        # This will print B if the B button is being pressed
        if keys & ugame.K_O != 0:
            pass  # Placeholder for B button action

        # Handle the START button
        # This will print Start if the Start button is being pressed
        if keys & ugame.K_START != 0:
            pass  # Placeholder for START button action

        # Handle the SELECT button
        # This will print Select if the Select button is being pressed
        if keys & ugame.K_SELECT != 0:
            pass  # Placeholder for SELECT button action

        # Handle moving the ship to the right.
        if keys & ugame.K_RIGHT != 0:
            # If the right button on the D pad is pressed, the ship will move 1
            # pixel in the X direction to the right, we take the ship's current position and add 1.
            # The Y value will stay the same.
            # Ensure ship stays within bounds
            if ship.x < (constants.SCREEN_X - constants.SPRITE_SIZE):
                ship.move(ship.x + 1, ship.y)
            else:
                # If at the edge, keep the ship at the rightmost position.
                ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)

        # Handle moving the ship to the left.
        if keys & ugame.K_LEFT != 0:
            # If the left button on the D pad is pressed, the ship will move 1
            # pixel in the X direction to the left, we take the ship's current position and add 1 to it.
            # The Y value will stay the same.
            if ship.x >= 0:  # Ensure ship stays within bounds
                ship.move(ship.x - 1, ship.y)
            else:
                # If at the edge, keep the ship at the leftmost position.
                ship.move(0, ship.y)

        # Handle the UP button
        # The ship will move up, the y value will decrease by 1, and the x value will stay the same.
        if keys & ugame.K_UP != 0:
            pass  # Placeholder for UP button action

        # Handle the DOWN button
        # The ship will move down, the y value will increase by 1, and the x value will stay the same.
        if keys & ugame.K_DOWN != 0:
            pass  # Placeholder for DOWN button action

        # Update game logic:
        # Redraw Sprites:
        game.render_sprites([ship])
        # Wait until refresh rate finishes:
        game.tick()


if __name__ == "__main__":
    game_scene()
