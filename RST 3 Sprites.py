import ugame
import stage


def game_scene():
    # This is the main function game scene

    # Import the image and assign to a variable:
    image_bank_background = stage.Bank.from_bmp16(
        "space_aliens_background.bmp")

    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    background = stage.Grid(image_bank_background, 10, 8)

    ship = stage.Sprite(image_bank_sprites, 5, 75, 66)

    game = stage.Stage(ugame.display, 60)
    # Our image is going to be refreshed 60 times

    game.layers = [ship] + [background]

    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input
        # update game logic
        # redraw Sprites

        game.render_sprites([ship])
        game.tick()


if __name__ == "__main__":
    game_scene()
