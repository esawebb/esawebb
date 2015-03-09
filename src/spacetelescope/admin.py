# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from djangoplicity.contrib.admin.sites import AdminSite
from djangoplicity.contrib.admin.discover import autoregister

# Import all admin interfaces we need
import django.contrib.auth.admin
import django.contrib.redirects.admin
import django.contrib.sites.admin
import djangoplicity.announcements.admin
import djangoplicity.contrib.statistics.admin
import djangoplicity.menus.admin
import djangoplicity.pages.admin
import djangoplicity.media.admin
import djangoplicity.products.admin
import djangoplicity.releases.admin
import djangoplicity.metadata.admin
import djangoplicity.archives.contrib.satchmo.freeorder.admin
#import djangoplicity.events.admin
import djangoplicity.mailinglists.admin
import djangoplicity.newsletters.admin
#import djangoplicity.contacts.admin
import djangoplicity.customsearch.admin
#import djangoplicity.eventcalendar.admin
import djangoplicity.actions.admin
import djangoplicity.imgvote.admin
import djangoplicity.science.admin
import djangoplicity.crawler.admin

# Register each applications admin interfaces with
# an admin site.
admin_site = AdminSite( name="admin_site" )
adminlogs_site = AdminSite( name="adminlogs_site" )
adminshop_site = AdminSite( name="adminshop_site" )

autoregister( admin_site, djangoplicity.announcements.admin )
autoregister( admin_site, django.contrib.auth.admin )
autoregister( admin_site, django.contrib.sites.admin )
autoregister( admin_site, djangoplicity.menus.admin )
autoregister( admin_site, djangoplicity.pages.admin )
autoregister( admin_site, djangoplicity.media.admin )
autoregister( admin_site, djangoplicity.releases.admin )
autoregister( admin_site, djangoplicity.metadata.admin )
autoregister( admin_site, djangoplicity.products.admin )
#autoregister( admin_site, djangoplicity.events.admin )
autoregister( admin_site, djangoplicity.mailinglists.admin )
autoregister( admin_site, djangoplicity.newsletters.admin )
#autoregister( admin_site, djangoplicity.contacts.admin )
autoregister( admin_site, djangoplicity.customsearch.admin )
#autoregister( admin_site, djangoplicity.eventcalendar.admin )
autoregister( admin_site, djangoplicity.science.admin )
autoregister( admin_site, djangoplicity.crawler.admin )


autoregister( adminlogs_site, djangoplicity.actions.admin )


#
# Applications that does not support above method.
#
adminlogs_site.register(django.contrib.redirects.models.Redirect,
                        django.contrib.redirects.admin.RedirectAdmin)

adminlogs_site.register(django.contrib.sites.models.Site,
                        django.contrib.sites.admin.SiteAdmin)

admin_site.register(django.contrib.auth.models.User,
                        django.contrib.auth.admin.UserAdmin)

admin_site.register(django.contrib.auth.models.Group,
                        django.contrib.auth.admin.GroupAdmin)


from djangoplicity.archives.contrib.satchmo.admin import satchmo_admin
adminshop_site = satchmo_admin( adminshop_site )

autoregister( adminshop_site, djangoplicity.archives.contrib.satchmo.freeorder.admin )

autoregister( admin_site, djangoplicity.imgvote.admin )
