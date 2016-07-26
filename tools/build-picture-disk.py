#!/usr/bin/env python

"""
Copyright (C) 2015 David Boddie <david@boddie.org.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import glob, os, stat, struct, sys
import makedfs

version = "1.0"

def system(command):

    if os.system(command):
        sys.exit(1)

if __name__ == "__main__":

    if len(sys.argv) < 3:
    
        sys.stderr.write("Usage: %s (<picture data file> <text file>) ... <new SSD file>\n" % sys.argv[0])
        sys.exit(1)
    
    args = sys.argv[:]
    
    out_file = args[-1]
    
    # Build the ROM image file.
    system("ophis src/sync.oph -o palette.rom")
    rom = open("palette.rom", "rb").read()
    rom += "\x00" * (16384 - len(rom))
    open("palette.rom", "wb").write(rom)
    print "Written palette.rom"
    
    # Collect the picture and text files in the data directory.
    data_files = args[1:-1]
    picture_files = []
    text_files = []
    
    for i in range(0, len(data_files), 2):
        picture_files.append(data_files[i])
        text_files.append(data_files[i + 1])
    
    boot_text = []
    boot_text.append("*LOAD DISPLAY")
    # Run the instructions viewer.
    boot_text.append("*/ INSTR")

    slides_list = []
    
    picture_data = []
    i = 1
    for name, text_name in zip(picture_files, text_files):
        picture_data.append(("PICT%i" % i, 0x3dc0, 0x3dc0, open(name, "rb").read()))
        picture_data.append(("TEXT%i" % i, 0x1900, 0x1900, open(text_name, "rb").read()))
        slides_list.append("?&FE08=&FF:?&FE09=&FF")
        slides_list.append("CLS")
        slides_list.append("*LOAD PICT%i" % i)
        slides_list.append("*LOAD TEXT%i" % i)
        slides_list.append("CALL &E00")
        slides_list.append("*SHOW")
        i += 1
    
    slides_list.append("*FX 3")
    #slides_list.append("VDU 26:CLS")
    
    try:
        image_license_text = open("LICENSE-images", "r").read().replace("\n", "\r")
    except IOError:
        image_license_text = "Include information about your images in a file called LICENSE-images."
    
    # Assemble the files.
    assemble = [("src/instructions.oph", "INSTR", 0x1900),
                ("src/display_text.oph", "DISPLAY", 0x0e00)]
    files = [("!BOOT", 0x0000, 0x0000, "\r".join(boot_text) + "\r"),
             ("LICENSE", 0x0000, 0x0000, image_license_text),
             ("COPYING", 0x0000, 0x0000, __doc__.replace("\n", "\r")),
             ("SLIDES", 0x0000, 0x0000, "\r".join(slides_list) + "\r")] + \
             picture_data
    
    for name, output, addr in assemble:
        if name.endswith(".oph"):
            if not os.path.exists(output) or (
                os.stat(name)[stat.ST_MTIME] > os.stat(output)[stat.ST_MTIME]):
                system("ophis " + name + " -o " + output)
            code = open(output).read()
        else:
            code = open(name).read().replace("\n", "\r")
            addr = 0x0000
        
        files.append((output, addr, addr, code))
    
    # Write the files to a disk image.
    disk = makedfs.Disk()
    disk.new()
    
    catalogue = disk.catalogue()
    catalogue.boot_option = 3
    
    disk_files = []
    for name, load, exec_, data in files:
        disk_files.append(makedfs.File("$." + name, data, load, exec_, len(data)))
    
    catalogue.write("Palette", disk_files)
    
    disk.file.seek(0, 0)
    disk_data = disk.file.read()
    open(out_file, "w").write(disk_data)
    
    print
    print "Written", out_file

    # Remove the object files.
    for name, output, addr in assemble:
        if name.endswith(".oph") and os.path.exists(output):
            os.remove(output)
    
    # Exit
    sys.exit()
