#!/usr/bin/env python3
import argparse
parser = argparse.ArgumentParser(
    prog="ttxrenderer",
    description="Converts teletext pages to images")
parser.add_argument("pages_dir")
parser.add_argument("out_dir")
args = parser.parse_args()

import logging
from datetime import datetime, timezone
import os
import pygame
import glob
from PIL import Image

from .ViewtextRenderer import ViewtextRenderer
from .testpages import CeefaxEngtest, LoadRaw


# Set to True to force rescaling of the image regardless of screen size.
# TODO - allow scaling to be set to NONE, FIT or STRETCH.
force_scale = False

# Font size.
font_size = 30
# Antialiasing -- needs to be on or MODE7 will screw up.
font_aa = False

# Display timing -- flash on in seconds.
t_flash_on = 1.0
# Display timing -- flash off in seconds.
t_flash_off = 0.3

# Fullscreen.
fullscreen = False

# Hold pages up for this many seconds.
page_delay = 1

# Get directory of this script.
script_dir = os.path.dirname(os.path.realpath(__file__))
working_dir = os.path.curdir
output_dir = os.path.join(working_dir, args.out_dir or "output")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get a list of files from the pages directory.
pages_dir = os.path.join(working_dir, args.pages_dir or "pages")
page_filenames = os.listdir(pages_dir)

# Page list.
pages = [
    [899, CeefaxEngtest()],
]
for page_filename in page_filenames:
    page_number = int(page_filename[1:4])
    pages.append([page_number, LoadRaw(os.path.normpath(f"{pages_dir}/{page_filename}"))])

# Initialise the display.
logging.info("displayInit")
pygame.display.init()
pygame.display.set_caption('Viewtext renderer')

# Hide the mouse cursor.
# pygame.mouse.set_visible(False)

# Open the screen.
if fullscreen:
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    logging.info("Framebuffer size: %d x %d" % (size[0], size[1]))
    lcd = pygame.display.set_mode(size, pygame.FULLSCREEN)
else:
    size = (720, 576)
    # size = (1280,768)
    lcd = pygame.display.set_mode(size, 0)

logging.info("modeset done")

# TODO background image.
lcd.fill((0, 0, 0))

# Initialise fonts.
logging.info("fontInit")
pygame.font.init()

# Initialise Viewdata/Teletext renderer.
logging.info("viewtextInit")
# vtr = ViewtextRenderer(font="fonts/MODE7GX0.TTF", fontsize=FONT_SIZE, antialias=FONT_AA)
vtr = ViewtextRenderer(font="bedstead", fontsize=font_size, antialias=font_aa, fontpath=os.path.join(script_dir, "fonts/"))

# --- Set up transform rectangle ---

# Do an initial render.
pagenumber, page = pages[0]
main, flash = vtr.render(page)

# Rescale the Teletext image if it's too large for the screen.
r = main.get_rect()
lr = lcd.get_rect()
if (lr[0] < r[0]) or (lr[1] < r[1]) or force_scale:
    # Resize (scale down) to fit the screen.
    r = main.get_rect().fit(lcd.get_rect())
    main = pygame.transform.smoothscale(main, (r.width, r.height))
    flash = pygame.transform.smoothscale(flash, (r.width, r.height))
else:
    # No resize required.
    r = main.get_rect()

# Centre the Teletext image on the screen.
r.center = (size[0] / 2, size[1] / 2)

# Set up 100ms tick.
evt_tick = pygame.USEREVENT + 1
ticks_per_sec = 10
pygame.time.set_timer(evt_tick, (1000 // ticks_per_sec))

# Main display loop.
quit = False
tick = 0
pageidx = 0
lasttick = 0
while not quit:
    lasttick = tick
    newpage = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quit (usually X11 only).
            quit = True

        elif event.type == pygame.KEYDOWN:
            # Keypress.
            if event.key == pygame.K_ESCAPE:
                quit = True

        elif event.type == evt_tick:
            # User defined event: timer tick.
            tick += 1

    # If the tick hasn't incremented, don't bother doing anything.
    if tick <= lasttick:
        continue

    #if (tick % (page_delay * ticks_per_sec)) == 0:
    if True:
        # Pick the next page.
        pagenumber, page = pages[pageidx]
        pageidx += 1
        if pageidx >= len(pages):
            pageidx = 0
            quit = True
        newpage = True

    if (tick % ticks_per_sec) == 0 or newpage:
        # Top of second. Update the header row and force a display update.
        now = datetime.now()

        page[0] = b'  P%03d  ' % pagenumber  # Decoder reserved (8 chars).
        page[0] += b'TELETEXT '  # Header bar.
        page[0] += b'%03d ' % pagenumber

        #page[24] = b'\x03Dial the number in yellow to view page.'
        # page[24] = b'\x03Dial yellow number to see, P100 is home'
        #page[24] = b'\x03Dial yellow numbers (P100) to view page'

        page[0] += bytes(
            datetime.now(timezone.utc)
                .isoformat()
                .replace("T", " ")
                .replace("Z", ""),
            'ascii',
        )

        main, flash = vtr.render(page)
        lcd.blit(main, r)
        pygame.display.update()
        done_page_path = os.path.join(output_dir, f"{pagenumber}.png")
        pygame.image.save(main, done_page_path)

pygame.quit()

# Combine the images into a tiled image.
def combine_images(output_dir):
    image_paths = sorted(glob.glob(os.path.join(output_dir, "*.png")))
    images = [Image.open(image_path) for image_path in image_paths]

    if not images:
        return

    # Assuming all images are the same size
    img_width, img_height = images[0].size
    grid_width = int(len(images) ** 0.5)
    grid_height = (len(images) + grid_width - 1) // grid_width

    combined_image = Image.new('RGB', (grid_width * img_width, grid_height * img_height))

    for idx, image in enumerate(images):
        x = (idx % grid_width) * img_width
        y = (idx // grid_width) * img_height
        combined_image.paste(image, (x, y))

    combined_image.save(os.path.join(output_dir, "combined_image.png"))

combine_images(output_dir)
