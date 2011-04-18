# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from __future__ import with_statement
from djangoplicity.fabplicity.deploy import *
from djangoplicity.fabplicity.services import *
from djangoplicity.fabplicity.environment import *
from djangoplicity.fabric1.celery import *
from djangoplicity.fabric1.django import *
from djangoplicity.fabric1.mercurial import *
from djangoplicity.fabric1.rabbitmq import *
from djangoplicity.fabric1.python import *
from djangoplicity.fabric1.mysql import *
from fabric.api import env

env.ENVIRONMENTS = [prod,int,loc]