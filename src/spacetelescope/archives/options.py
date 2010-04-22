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
from django.http import Http404
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from djangoplicity.archives import ArchiveOptions
from djangoplicity.archives.contrib import security
from djangoplicity.archives.contrib.browsers import *
from djangoplicity.archives.contrib.info import *
from djangoplicity.archives.contrib.queries import AllPublicQuery, \
	UnpublishedQuery, YearQuery, EmbargoQuery, StagingQuery, param_extra_templates
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


def resolution(obj):
	""" Display helper - output the dimensions of an image. """
	if obj.resolution:
		return '%s dpi' % obj.resolution 
	else:
		return None
resolution.short_description = _('Resolution')

BookOptions = product_options( "books", "Book", "Books", True )
BrochureOptions = product_options( "brochures", "Brochure", "Brochures", True )
EducationalMaterialOptions = product_options( "education", "Material", "Educational Material", True )
CDROMOptions = product_options( "cdroms", "DVD/CD", "DVDs/CDs", False )
PosterOptions = product_options( "posters", "Poster", "Posters", False, extra_fields=(pixel_size,resolution) )
TechnicalDocumentOptions = product_options( "techdocs", "Document", "Technical Documents", True )
NewsletterOptions = product_options( "newsletters", "Newsletter", "Newsletter & Journals", True )
MerchandiseOptions = product_options( "merchandise", "Merchandise", "Merchandise", False )
StickerOptions = product_options( "stickers", "Sticker", "Stickers", False )
PostCardOptions = product_options( "postcards", "Postcard", "Postcards", False )

class KidsDrawingOptions ( StandardOptions ):
	   
	urlname_prefix = 'drawings'

	info = ( 
		( _(u'Author'), { 'fields' : ( 'name', 'age', 'city', 'country' ), } ),
		( _(u'About the Drawing'), { 'fields' : ( 'id', ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Drawings" )
				
	
class PressKitOptions (StandardOptions):
	urlname_prefix = 'presskits'

	info = ( 
		( _(u'About the Press Kit'), { 'fields' : ( 'id', paper_size, 'pages'  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
		( _(u'File Formats'), {'resources' : ( 'pdf', ), 'icons' : { 'pdf' : 'doc',  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Press Kit Archive: View All" )
	
	
class AnnouncementOptions( ArchiveOptions ):
	urlname_prefix = 'announcements'
	
	admin = (
		( _(u'Admin'), { 'links' : ( admin_edit_for_site('admin_site'),  ), 'fields' : ( published, 'release_date', 'last_modified', 'created' ), }  ),
	)

	info = ( 
		( _(u'About the Announcement'), { 'fields' : ( 'id',)  } ),
	)
	
	search_fields = ( 'id', 'title', 'description', 'contacts', 'links', )
	
	downloads = ( image_downloads, file_downloads )
	
	class Queries( object ):
		default = AllPublicQuery( browsers = ( 'normal', 'viewall' ), verbose_name = "Announcements" )
		embargo = EmbargoQuery( browsers = ( 'normal', 'viewall' ), verbose_name = "Embargoed Announcements" )
		staging = StagingQuery( browsers = ( 'normal', 'viewall' ), verbose_name = "Announcements (Staging)" )
		year = YearQuery( browsers = ( 'normal', 'viewall' ), verbose_name = "Announcements %d" )
		
	class Browsers( object ):
		normal = ListBrowser( index_template = 'archives/announcement/index_list.html' )
		viewall = ListBrowser( verbose_name = _( u'View All' ), paginate_by = 100, index_template = 'archives/announcement/index_list.html' )
		
	class ResourceProtection ( object ):
		unpublished = ( UnpublishedQuery, security.UNPUBLISHED_PERMS )
		staging = ( StagingQuery, security.STAGING_PERMS )
		embargo = ( EmbargoQuery, security.EMBARGO )	


class ConferencePosterOptions (StandardOptions):
	urlname_prefix = 'conference_posters'

	info = ( 
		( _( u'About the Poster' ), { 'fields' : ( 'id', paper_size, pixel_size, resolution ), } ), 
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'screen' ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen': 'phot' } } ),
		)

	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Conference Poster Archive: View All" )
			

class LogoOptions (StandardOptions):
	urlname_prefix = 'logos'

	info = ( 
		( _(u'About the Logo'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'screen' ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen': 'phot' } } ),
		( _(u'File Formats'), {'resources' : ( 'eps', 'illustrator', 'transparent', ), 'icons' : { 'eps' : 'phot', 'illustrator' : 'phot', 'transparent' : 'phot',  } } )
	)

	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Logo Archive: View All" )
	
		



class CalendarYearQuery( YearQuery ):		
	def queryset( self, model, options, request, stringparam=None, **kwargs ):
		if not stringparam:
			raise Http404
		
		now = datetime.now()
		
		# Convert to year   
		try:
			year = int( stringparam )
			
			# TOOD: Are these constraints really appropriate?
			if year < 1900 or year > now.year+1:
				raise Http404
		except TypeError:
			raise Http404
		except ValueError:
			raise Http404	
		
		(qs, args) = super( YearQuery,self ).queryset( model, options, request, **kwargs )
		qs = qs.filter( year=year )
		return ( qs , { 'year' : year } ) 


class ArtistQuery( AllPublicQuery ):
	"""
	Query for displaying all entries for a certain Artist
	
	May be defined in an Options class as:
	
	class Queries(object):
		artist = ArtistQuery(
						  browsers=( ... ), 
						  verbose_name="..." )
								  

	
	Keyword argument "use_year_title" determines if the year should be
	substituted into verbose name. 
	"""
	
	def __init__(self, **kwargs):
		
		defaults = { 'include_in_urlpatterns' : True, 'url_template' : 'djangoplicity.archives.contrib.queries.urls.simple', 'extra_templates' :  param_extra_templates( param='artist' ), 'searchable' : False }
		defaults.update( kwargs )
		super(ArtistQuery,self).__init__( **defaults )
			
	def queryset( self, model, options, request, stringparam=None, **kwargs ):
		if not stringparam:
			(qs, args) = super( ArtistQuery,self ).queryset( model, options, request, **kwargs )
			return ( qs , { 'artist' : 'Online Art' } ) 
		

	
		try:
			artist = OnlineArtAuthor.objects.get(id=stringparam)	
		except OnlineArtAuthor.DoesNotExist:
			raise Http404
		(qs, args) = super( ArtistQuery,self ).queryset( model, options, request, **kwargs )
		
		try:
			qs = qs.filter(artist = artist)
			return ( qs , { 'artist' : artist } ) 
		except FieldError:
			raise ImproperlyConfigured( 'The specified artist field is not available for the current archive.' )

	
	def url_args(self, model, options, request, stringparam=None, **kwargs ):
		"""
		Hook for query to specify extra reverse URL lookup arguments.
		"""
		return [ stringparam ]
	
	def verbose_name(self, artist=None, **kwargs ):
		"""
		Method that can be overwritten to customize the archive title.
		"""
		try:
			if artist :
				return self._verbose_name % artist
		except TypeError:
			raise ImproperlyConfigured( 'Title for ArtistQuery does not include substitution string - set "use_year_title" to False or include one and only one %d in the verbose_name.')


# TODO: display according to year, then month		
class CalendarOptions (StandardOptions):
	urlname_prefix = 'calendars'

	info = ( 
		( _(u'About the Calendar'), { 'fields' : ( 'id', 'year', 'month',  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium',  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot',  } } ),
		( _(u'File Formats'), {'resources' : ( 'pdf', 'pdfsm' ), 'icons' : { 'pdf' : 'doc',  'pdfsm' : 'doc' } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Calendar Archive: View All" )
		year = CalendarYearQuery( browsers = ( 'normal', 'viewall' ), verbose_name = "Calendar: %d")
		
class OnlineArtOptions ( StandardOptions ):
	   
	urlname_prefix = 'art'

	info = ( 
		( _(u'About the Piece'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
		)
	
	class Queries(object):
		#default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Art: View All" )
		default = ArtistQuery ( browsers=( 'normal', 'viewall' ),  verbose_name="%s" )
		

class OnlineArtAuthorOptions ( StandardOptions ):
	   
	urlname_prefix = 'artists'

	info = ( 
		( _(u'About the Piece'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'screen'  ), 'icons' : { 'original' : 'phot', 'screen' : 'phot'  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Artists: View All" )
		
		
## Print
#class PrintLayoutOptions ( StandardOptions ):
#	   
#	urlname_prefix = 'printlayouts'
#
#	info = ( 
#		( _(u'About the Print Layout'), { 'fields' : ( 'id', release_date,  ), } ),
#	)
#	
#	downloads = ( 
#		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
#		)
#	
#	class Queries(object):
#		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Print Layouts: View All" )
	


class SlideShowOptions (StandardOptions):
	urlname_prefix = 'slideshows'

	info = ( 
		( _(u'About the Slideshow'), { 'fields' : ( 'id', 'x_size','y_size', ), } ),
	)
	
	downloads = ( 
		( _(u'File Formats'), {'resources' : ( 'flash', ), 'icons' : { 'flash' : 'movie'  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Slideshow Archive: View All" )


class ExhibitionOptions ( StandardOptions ):
	   
	urlname_prefix = 'exhibitions'

	info = ( 
		( _(u'About the Exhibition'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Exhibitions: View All" )
	

	
class FITSImageOptions ( StandardOptions ):
	   
	urlname_prefix = 'fitsimages'

	#TODO add author entries to info?
	info = ( 
		( _(u'About the FITS Image'), { 'fields' : ( 'id', 'name', 'city', 'country', ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="FITS Liberator Images" )
		
		
class UserVideoOptions ( StandardOptions ):
	   
	urlname_prefix = 'uservideos'

	#TODO add author entries to info?
	info = ( 
		( _(u'About the Video'), { 'fields' : ( 'id', 'name', 'city', 'country', 'email', 'link' ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="User Videos" )


class PresentationOptions ( StandardOptions ):
	   
	urlname_prefix = 'presentations'

	#TODO add author entries to info?
	info = ( 
		( _(u'About the Presentation'), { 'fields' : ( 'id', ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Presentations" )
	