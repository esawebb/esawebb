from django.utils.translation import ugettext_lazy as _
from livesettings import *

PRODUCT_TYPES = config_get('PRODUCT', 'PRODUCT_TYPES')
PRODUCT_TYPES.add_choice(('spacetelescope.archives::Book', _('Book Product')))
PRODUCT_TYPES.add_choice(('spacetelescope.archives::Brochure', _('Brochure Product')))
PRODUCT_TYPES.add_choice(('spacetelescope.archives::EducationalMaterial', _('Educational Material Product')))
PRODUCT_TYPES.add_choice(('spacetelescope.archives::CDROM', _('CD-ROM/DVD Product')))
PRODUCT_TYPES.add_choice(('spacetelescope.archives::Poster', _('Poster Product')))
PRODUCT_TYPES.add_choice(('spacetelescope.archives::TechnicalDocument', _('Technical Document Product')))
PRODUCT_TYPES.add_choice(('spacetelescope.archives::Newsletter', _('Newsletter Product')))
PRODUCT_TYPES.add_choice(('spacetelescope.archives::Merchandise', _('Merchandise Product')))
PRODUCT_TYPES.add_choice(('spacetelescope.archives::Sticker', _('Sticker Product')))