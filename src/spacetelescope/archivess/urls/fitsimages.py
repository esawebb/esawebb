# Djangoplicity
# Copyright 2007-2008 ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from djangoplicity.archives import urlpatterns_for_options
from spacetelescope.archives.options import *


urlpatterns = urlpatterns_for_options( FITSImageOptions )