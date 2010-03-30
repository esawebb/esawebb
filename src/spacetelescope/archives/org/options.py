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
		
#TODO: embargo? yes
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
		#( _(u'Files') TODO: include 'zip' resource? see model CDROM !!
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
	
		
class TechnicalDocumentOptions (StandardOptions):
	urlname_prefix = 'techdocs'

	info = ( 
		( _(u'About the Technical Document'), { 'fields' : ( 'id', release_date,  ), } ),
	)
	
	downloads = ( 
		( _(u'Images'), {'resources' : ( 'original', 'large', 'medium', 'screen'  ), 'icons' : { 'original' : 'phot', 'large' : 'phot', 'medium' : 'phot', 'screen' : 'phot'  } } ),
		( _(u'File Formats'), {'resources' : ( 'pdf', ), 'icons' : { 'pdf' : 'pdf',  } } ),
		)
	
	class Queries(object):
		default = AllPublicQuery( browsers=( 'normal', 'viewall' ), verbose_name="Technical Document Archive: View All" )
	


		
		

