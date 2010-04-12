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
from django.http import Http404
from djangoplicity.archives import ArchiveOptions
from djangoplicity.archives.contrib import security
from djangoplicity.archives.contrib.browsers import *
from djangoplicity.archives.contrib.info import *
from djangoplicity.archives.contrib.queries import AllPublicQuery, UnpublishedQuery, YearQuery, EmbargoQuery, StagingQuery,  param_extra_templates
from djangoplicity.archives.importer.forms import GenericImportForm
from djangoplicity.templatetags.djangoplicity_datetime import datetime as datetime_format
from djangoplicity.metadata.archives.info import *
from spacetelescope.archives.base import *
from models import *		
		
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
		( _(u'About the Calendar'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium',  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot',  } } ),
		( _(u'File Formats'), {'resources' : ( 'pdf', 'pdfsm' ), 'icons' : { 'pdf' : 'pdf',  'pdfsm' : 'pdf' } } ),
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
#	


class SlideShowOptions (StandardOptions):
	urlname_prefix = 'slideshows'

	info = ( 
		( _(u'About the Slideshow'), { 'fields' : ( 'id', release_date, 'x_size','y_size','resolution' ), } ),
	)
	
	downloads = ( 
		( _(u'File Formats'), {'resources' : ( 'flash', ), 'icons' : { 'flash' : 'movie'  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Slideshow Archive: View All" )

