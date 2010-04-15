# coding: utf-8
#
# Djangoplicity
# Copyright 2008 ESA/Hubble & International Astronomical Union
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
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
from djangoplicity.archives.contrib.queries import AllPublicQuery, \
	UnpublishedQuery, YearQuery, EmbargoQuery, StagingQuery
from djangoplicity.archives.importer.forms import GenericImportForm
from djangoplicity.metadata.archives.info import *
from djangoplicity.templatetags.djangoplicity_datetime import \
	datetime as datetime_format
from models import *
from spacetelescope.archives.base import *
import os


def product_options( prefix, about_name, view_name, with_pages, extra_fields=() ):
	if with_pages:
		fields = ( 'id', release_date, paper_size, 'pages' ) + extra_fields
	else:
		fields = ( 'id', release_date, paper_size ) + extra_fields
	
	class Options( StandardOptions ):
		urlname_prefix = prefix
	
		info = ( 
			( _( u'About the %s' % about_name ), { 'links' : ( shop_link, ), 'fields' : fields, } ),
		)
		
		class Queries(object):
			default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name=view_name )
			
	return Options


def pixel_size(obj):
	""" Display helper - output the dimensions of an image. """
	if obj.x_size and obj.y_size:
		return '%s x %s px' % ( obj.x_size, obj.y_size )
	else:
		return None
pixel_size.short_description = _('Pixel Size')

BookOptions = product_options( "books", "Book", "Books", True )
BrochureOptions = product_options( "brochures", "Brochure", "Brochures", True )
EducationalMaterialOptions = product_options( "education", "Material", "Educational Material", True )
CDROMOptions = product_options( "cdroms", "DVD/CD", "DVDs/CDs", False )
PosterOptions = product_options( "posters", "Poster", "Posters", False, extra_fields=(pixel_size,'resolution') )
TechnicalDocumentOptions = product_options( "techdocs", "Document", "Technical Documents", True )
NewsletterOptions = product_options( "newsletters", "Newsletter", "Newsletter & Journals", True )
MerchandiseOptions = product_options( "merchandise", "Merchandise", "Merchandise", False )
StickerOptions = product_options( "stickers", "Sticker", "Stickers", False )
PostCardOptions = product_options( "postcards", "Postcard", "Postcards", False )

class KidsDrawingOptions ( StandardOptions ):
	   
	urlname_prefix = 'drawings'

	info = ( 
		( _(u'Author'), { 'fields' : ( 'author_name', 'author_age', 'author_city' ), } ),
		( _(u'About the Drawing'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Drawings: View All" )
				
	
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
	
	
class AnnouncementOptions (StandardOptions):
	urlname_prefix = 'announcements'

	info = ( 
		( _(u'About the Announcement'), { 'fields' : ( id, subject_name, subject_category, facility )  } ),
	)
	
	#TODO: add search fields?
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
		)
	

	class Queries( object ):
		default = AllPublicQuery( browsers = ( 'normal', 'viewall' ), verbose_name = "Updates" )
		embargo = EmbargoQuery( browsers = ( 'normal', 'viewall' ), verbose_name = "Embargoed Updates" )
		staging = StagingQuery( browsers = ( 'normal', 'viewall' ), verbose_name = "Updates (Staging)" )
		year = YearQuery( browsers = ( 'normal', 'viewall' ), verbose_name = "Announcements %d" )
		
	class Browsers( object ):
		normal = ListBrowser( index_template = 'archives/index_list.html' )
		viewall = ListBrowser( verbose_name = _( u'View All' ), paginate_by = 100, index_template = 'archives/index_list.html' )
		
	class ResourceProtection ( object ):
		#unpublished = ( UnpublishedQuery, security.UNPUBLISHED_PERMS )
		#staging = ( StagingQuery, security.STAGING_PERMS )
		embargo = ( EmbargoQuery, security.EMBARGO )	

class ConferencePosterOptions (StandardOptions):
	urlname_prefix = 'conference_posters'

	info = ( 
		( _(u'About the Poster'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen' ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen': 'phot' } } ),
		)

	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Conference Poster Archive: View All" )
			

class LogoOptions (StandardOptions):
	urlname_prefix = 'logos'

	info = ( 
		( _(u'About the Logo'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen' ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen': 'phot' } } ),
		( _(u'File Formats'), {'resources' : ( 'eps', 'illustrator', 'transparent', ), 'icons' : { 'eps' : 'phot', 'illustrator' : 'phot', 'transparent' : 'phot',  } } )
	)

	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Logo Archive: View All" )
	
		
