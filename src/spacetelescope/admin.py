# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from django.contrib.admin.sites import AdminSite
from djangoplicity.authtkt.utils import authtkt_decorator
from djangoplicity.contrib.admin.discover import autoregister

# Import all admin interfaces we need
import django.contrib.auth.admin
import django.contrib.redirects.admin
import django.contrib.sites.admin
import djangodblog.admin
import djangoplicity.contrib.statistics.admin
import djangoplicity.cron.admin
import djangoplicity.menus.admin
import djangoplicity.pages.admin
import djangoplicity.search.admin
import djangoplicity.media.admin
import djangoplicity.releases.admin
import djangoplicity.metadata.admin
import djangoplicity.contrib.redirects.admin
import djangoplicity.authtkt.admin



# Register each applications admin interfaces with
# an admin site.
admin_site = authtkt_decorator( AdminSite( name="admin_site" ) )
adminlogs_site = authtkt_decorator( AdminSite( name="adminlogs_site" ) )

autoregister( admin_site, django.contrib.auth.admin )
autoregister( admin_site, django.contrib.sites.admin )
autoregister( admin_site, djangoplicity.menus.admin )
autoregister( admin_site, djangoplicity.pages.admin )
autoregister( admin_site, djangoplicity.media.admin )
autoregister( admin_site, djangoplicity.releases.admin )
autoregister( admin_site, djangoplicity.metadata.admin )

autoregister ( adminlogs_site, djangoplicity.contrib.redirects.admin )
autoregister( adminlogs_site, djangoplicity.search.admin )
autoregister( adminlogs_site, djangodblog.admin )
autoregister( adminlogs_site, djangoplicity.cron.admin )
autoregister( adminlogs_site, djangoplicity.authtkt.admin )



# 
# Applications that does not support above method.
#
#adminlogs_site.register(django.contrib.redirects.models.Redirect, 
#                        django.contrib.redirects.admin.RedirectAdmin) 
                    
adminlogs_site.register(django.contrib.sites.models.Site, 
                        django.contrib.sites.admin.SiteAdmin)

admin_site.register(django.contrib.auth.models.User, 
                        django.contrib.auth.admin.UserAdmin)

admin_site.register(django.contrib.auth.models.Group, 
                        django.contrib.auth.admin.GroupAdmin)
