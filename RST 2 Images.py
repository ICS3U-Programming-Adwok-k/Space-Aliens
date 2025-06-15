import ugame
import stage


def game_scene():
    # This is the main function game scene

    # Import the image and assign to a variable
    image_bank_background = stage.Bank.from_bmp16(
        "space_aliens_background.bmp")

    background = stage.Grid(image_bank_background, 10, 8)

    game = stage.Stage(ugame.display, 60)

    # Our image is going to be refreshed 60 times
    game.layers = [background]

    game.render_block()

    while True:
        # This repeats forever
        pass


if __name__ == "__main__":
    game_scene()
