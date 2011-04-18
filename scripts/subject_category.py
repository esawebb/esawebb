#
# eso.org
# Copyright 2011 ESO
#
# -*- coding: utf-8 -*-
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Dirk Neumayer <dirk.neumayer@gmail.com>
#
#
# Mantis ESO 3065
# Tag all images with subject category and remove temporary taxonomy items.
#
#*************************************************************************************************************

from djangoplicity.media.models import Image

if __name__ == '__main__':
    Images = Image.objects.all()
    for Img in Images:
        print Img.id