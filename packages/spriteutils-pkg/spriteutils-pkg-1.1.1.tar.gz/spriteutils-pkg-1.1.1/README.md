#  Spriteutils
Spriteutils is small project to determine ***Sprites*** (specified by
there **unique label mask** and **bounding box**) in the given
***Sprite Sheet***.

A [**Sprite**](<https://en.wikipedia.org/wiki/Sprite_(computer_graphics)>)
is a small [**raster graphic**](https://en.wikipedia.org/wiki/Raster_graphics)
(a **bitmap**) that represents an object

It is not uncommon for games to have tens to hundreds of sprites.
Loading each of these as an individual image would consume a lot of
**memory** and **processing power**. To help manage sprites and avoid using so
many images, many games use
[**Sprite Sheets**](https://www.youtube.com/watch?v=crrFUYabm6E)

This project is a tool to determine sprites (specified by there unique
mask and bounding box) in the given Sprite Sheet.

# Installaltion:
## Prequisites: Python 3.7
```bash
$ pip install spriteutils-pkg
```

# Documentation
After install the package, open python (python version must be >= 3.7)
```bash
$ python
```

Import the package and using method help to read the document
```python
>>> from spriteutils import SpriteSheet
>>> help(SpriteSheet)
```

# Functional test
Replicate the following step in python
```python
# Import the package
>>> from spriteutils import SpriteSheet
# Specified the image file path name or create a PIL image
>>> image = "path/to/your/image"
# Create sprite sheet object
>>> sprite_sheet = SpriteSheet(image)
# Find all the sprites of the sprite sheet
>>> sprites ,label_map = sprite_sheet.find_sprites()
# Draw sprite masks for each sprite in the sprite sheet
>>> image = sprite_sheet.create_sprite_labels_image()
# Show the sprite masks image
>>> image.show()
```

# Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
# License
This project is licensed under the MIT License - see the LICENSE file for
details
