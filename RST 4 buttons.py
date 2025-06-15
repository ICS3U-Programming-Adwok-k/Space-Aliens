#!/usr/bin/env python3
# Created by: Adwok Adiebo
# Date: June 6th, 2025
#

import ugame
import stage
import constants


def game_scene():
    # This function is the main game_scene

    # image banks for CircuitPython
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # set the boundaries to image 0 in the image bank
    # and the size (10x8 tiles of size 16x16)
    background = stage.Grid(image_bank_background, 10, 8)

    # a sprite that will be updated every frame
    ship = stage.Sprite(image_bank_sprites, 5, 75, 66)

    # create a stage for the background to show up on and set the frame rate to 60fps
    game = stage.Stage(ugame.display, 60)

    #game.layers = [ship] + [background]

    # render all sprites
    game.render_block()

    while True:
        # get user input

        # update game logic

        # redraw Sprite
        game.render_sprites([ship])

        # wait until refresh rate finishes
        game.tick()

if __name__ == "__main__":
    game_scene()