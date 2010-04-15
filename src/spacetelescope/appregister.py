# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

# ========================   
# Register global page key
# ========================
from djangoplicity.pages.models import register_page_key
from django.utils.translation import ugettext as _

PAGE_KEYS = { 
			  "login" : 'spacetelescope.login',
			  "logout" : 'spacetelescope.logout',
			  "access_denied" : "spacetelescope.access_denied",
			  "shop_right_column" : "spacetelescope.shop_right_column",
			}

register_page_key( 'spacetelescope', PAGE_KEYS["login"], _('Login page'), _('Displayed above the login form.') )
register_page_key( 'spacetelescope', PAGE_KEYS["logout"], _('Logout page'), _('Displayed on the logout page.') )
register_page_key( 'spacetelescope', PAGE_KEYS["access_denied"], _('Access Denied'), _('Displayed when users are denied access to embargoed/staging resources.') )
register_page_key( 'spacetelescope', PAGE_KEYS["shop_right_column"], _('Shop Right Column'), _('Displayed on shop frontpage in right column.') )