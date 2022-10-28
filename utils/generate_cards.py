from PIL import Image, ImageFont, ImageDraw
import pathlib

"""
Utility for creating playing cards based on template .pngs
"""

# Note: words in template files for trees should be separated with spaces (i.e. blue spruce_template
# instead of blue_spruce_template) the naming of the template affects the name of the output.png,
# which is referenced in the .html templates

# Config
BASE_URL = "../arboretum/static/css"
INPUT_FOLDER = "other"
OUTPUT_FOLDER = "playing_cards"
BLANK_CARD_PNGS = ["blue spruce_template.png",
                   "cassia_template.png",
                   "oak_template.png",
                   "jacaranda_template.png",
                   "royal poinciana_template.png",
                   "tulip popular_template.png",
                   "dogwood_template.png",
                   "cherry blossom_template.png"]

CARDS_TO_CREATE = 8
TITLE_FONT = ImageFont.truetype("calibri.ttf", 100)
TOP_LEFT_XY = (20, 5)
TEXT_COLOR = (50, 50, 50)

base_path = pathlib.Path(BASE_URL)

for blank_card in BLANK_CARD_PNGS:
    file_path = base_path / INPUT_FOLDER / blank_card
    card_name = blank_card.split(".")[0]
    card_name = card_name.replace("_template", "")

    for i in range(1, CARDS_TO_CREATE + 1):
        my_image = Image.open(file_path).convert('RGB')
        image_editable = ImageDraw.Draw(my_image)

        card_val = str(i)

        image_editable.text(
            xy=TOP_LEFT_XY,
            text=card_val,
            fill=TEXT_COLOR,
            font=TITLE_FONT,
        )

        file_name = f"{card_name} {i}.png"

        my_image.save(base_path / OUTPUT_FOLDER / file_name)
