PictureBook
===========

This repository contains source code and tools for creating simple picture
books with text for the Acorn Electron, and could be used as the basis for a
graphical adventure game engine. The graphics are stored in MODE 1 format with
additional palette information for each scanline, allowing 4 unique colours to
be used per scanline. The text is shown in MODE 4 format at the bottom of the
screen below a border eight scanlines deep.

Building
--------

The source code needs to be compiled to a ROM image and a set of files in a
disk image. This is done using the tools/build-picture-disk.py file, which
requires both Python and the Ophis 6502 assembler to be installed.

Before the picture disk can be built, the pictures that you want to show need
to be converted into screen data using the tools/make_picture.py tool. The
pictures need to be 320 pixels wide by 160 high and already reduced in colour
depth to 3 bits per pixel. Each scanline of the image should only contain 4
unique colours. Run the tool from the root directory of the repository, as in
the following example:

  ./tools/make_picture.py pictures/dsc01290s-cropped.png

The text to go with each picture should be encoded using carriage return and
newline pairs ("\r\n") to separate each line of text, and must be terminated
with a null byte.

Update the LICENSE-images file to reflect the license of the images you are
including in the disk image.

Run the tool with the set of encoded images and text files that you want to
include in the disk image, as in the following example:

  ./tools/build-picture-disk.py data/dsc01290s-cropped.dat \
                                data/dsc01290s-cropped.txt \
                                data/dsc01323-cropped.dat \
                                data/dsc01323-cropped.txt \
                                data/dsc01325-cropped.dat \
                                data/dsc01325-cropped.txt temp.ssd

It should now be possible to use the palette.rom and disk image (temp.ssd in
the example above) with Elkulator or another Electron emulator. The palette.rom
file can also be written to an EEPROM and used in a real Electron.

Licenses
--------

The source code is licensed under the GNU General Public License version 3 or
later.

The pictures included in this collection are licensed under the Creative
Commons Attribution-NonCommercial-ShareAlike 4.0 International license.
