# coding: utf-8
#
# Djangoplicity
# Copyright 2008 ESA/Hubble & International Astronomical Union
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
import os
from PIL import Image as PILImage
from datetime import datetime, time
from django import forms
from django.conf.urls.defaults import *
from django.core.urlresolvers import NoReverseMatch, reverse
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from djangoplicity.archives import ArchiveOptions
from djangoplicity.archives.contrib import security
from djangoplicity.archives.contrib.browsers import *
from djangoplicity.archives.contrib.info import *
from djangoplicity.archives.contrib.queries import AllPublicQuery, UnpublishedQuery, YearQuery, EmbargoQuery, StagingQuery
from djangoplicity.archives.importer.forms import GenericImportForm
from djangoplicity.templatetags.djangoplicity_datetime import datetime as datetime_format
from djangoplicity.metadata.archives.info import *
from spacetelescope.archives.base import *
from models import *		
		

class CDROMOptions (StandardOptions):
	urlname_prefix = 'cdroms'

	info = ( 
		( _(u'About the CDROM'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium',  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', } } ),
		#( _(u'Files') TODO: include 'zip' resource? see model yes
		)
	

	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="CDROM Archive: View All" )
		
	

	
	
	
	
class BookOptions (StandardOptions):
	urlname_prefix = 'books'

	info = ( 
		( _(u'About the Book'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot' } } ),
		( _(u'File Formats'), {'resources' : ( 'pdf', ), 'icons' : { 'pdf' : 'pdf',  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="CDROM Archive: View All" )
		
	
class BrochureOptions (StandardOptions):
	urlname_prefix = 'brochures'

	info = ( 
		( _(u'About the Brochure'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot' } } ),
		( _(u'File Formats'), {'resources' : ( 'pdf', 'pdfsm' ), 'icons' : { 'pdf' : 'pdf',  'pdfsm' : 'pdf' } } ),
		)

	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Brochure Archive: View All" )
		


class MerchandiseOptions (StandardOptions):
	urlname_prefix = 'merchandise'

	info = ( 
		( _(u'About the Merchandise'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Merchandise Archive: View All" )

class NewsletterOptions (StandardOptions):
	urlname_prefix = 'newsletters'

	info = ( 
		( _(u'About the Newsletter'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Files'), {'resources' : ( 'pdf', 'doc', 'sciencepaper', 'text'  ), 'icons' : { 'pdf' : 'pdf', 'doc' : 'word', 'sciencepaper' : 'pdf', 'text' : 'txt'  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Newsletter Archive: View All" )
	
		
class PostCardOptions (StandardOptions):
	urlname_prefix = 'postcards'

	info = ( 
		( _(u'About the Postcard'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Postcard Archive: View All" )

class PosterOptions (StandardOptions):
	urlname_prefix = 'posters'

	info = ( 
		( _(u'About the Poster'), { 'fields' : ( 'id', release_date,  ), } ),
	)	

	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen' ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen': 'phot' } } ),
		#( _(u'Files') TODO: include 'zip' resource? see model
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Poster Archive: View All" )
		
	
class PressKitOptions (StandardOptions):
	urlname_prefix = 'presskits'

	info = ( 
		( _(u'About the Press Kit'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
		( _(u'File Formats'), {'resources' : ( 'pdf', ), 'icons' : { 'pdf' : 'pdf',  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Press Kit Archive: View All" )
	
	
class StickerOptions (StandardOptions):
	urlname_prefix = 'stickers'

	info = ( 
		( _(u'About the Sticker'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Sticker Archive: View All" )
	

