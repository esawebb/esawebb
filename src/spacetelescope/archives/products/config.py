from django.utils.translation import ugettext_lazy as _
from livesettings import *

PRODUCT_TYPES = config_get('PRODUCT', 'PRODUCT_TYPES')
PRODUCT_TYPES.add_choice(('spacetelescope.archives.products::Book', _('Book Product')))