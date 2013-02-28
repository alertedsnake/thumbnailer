#!/usr/bin/python
# Copyright 2010-2013 Michael Stella

import logging, os, stat
from PIL import Image

thumbsizeH  = 100, 80
thumbsizeV  = 65, 100
picsizeH    = 1024, 768
picsizeV    = 768, 1024

perms = stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH

def thumbnailDirectory(dir):

    os.chmod(dir, perms | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    for file in os.listdir(dir):
        if not os.path.isfile(file): continue
        if file.startswith('thumb'): continue

        im = Image.open(file)

        picsize = picsizeH
        thumbsize = thumbsizeH

        Y = int(picsizeH[0] / (float(im.size[0]) / float(im.size[1])))
        picsize = (picsizeH[0], Y)
        thumbsize = thumbsizeH

        if im.size[0] < im.size[1]:
            X = int(picsizeV[1] / (float(im.size[1]) / float(im.size[0])))
            picsize = (X, picsizeV[1])
            thumbsize = thumbsizeV


        # create the thumbnail file
        thumb = 'thumb.' + file
        if not os.path.exists(thumb):
            print "Making thumbnail %s size %s" % (thumb, thumbsize)

            tim = im.resize(thumbsize, Image.ANTIALIAS)
            tim.save(thumb, "JPEG")


        # resize the original
        if im.size[0] > picsize[0] or im.size[1] > picsize[1]:
            print "resizing original: %s -> %s" % (im.size, picsize)
            nim = im.resize(picsize)
            nim.save(file, "JPEG")

        # set permissions
        os.chmod(thumb, perms)
        os.chmod(file, perms)


if __name__ == '__main__':
    thumbnailDirectory('.')
