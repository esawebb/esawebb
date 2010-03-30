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
from djangoplicity.archives.contrib.queries import AllPublicQuery, UnpublishedQuery, YearQuery, EmbargoQuery, StagingQuery
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
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Art: View All" )
		#artist = ArtistQuery ( browsers=( 'normal', 'viewall' ),  verbose_name="Art by %s: View All" )
		
		
# TODO: how to model? Current Release model is not generic enough to support this
# Print
class PrintLayoutOptions ( StandardOptions ):
	   
	urlname_prefix = 'printlayouts'

	info = ( 
		( _(u'About the Print Layout'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Print Layouts: View All" )
	


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

