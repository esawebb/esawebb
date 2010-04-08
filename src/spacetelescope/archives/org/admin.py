# Djangoplicity
# Copyright 2007-2008 ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
from django.conf import settings
from django.contrib import admin
from djangoplicity.contrib.admin import DjangoplicityModelAdmin
from spacetelescope.archives.org.models import *
from djangoplicity.archives.contrib.admin import ArchiveAdmin, RenameAdmin, view_link
from django.forms import ModelForm
from django.core.urlresolvers import NoReverseMatch, reverse
from django.utils.safestring import mark_safe




class AnnouncementAdmin (DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', view_link('announcements') )
	list_filter = ( 'title', 'published', 'last_modified',  )
	list_editable = ( 'title', 'published', )
	search_fields = ( 'id', 'old_ids', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'credit', 'links','contacts'), } ),
					( 'Metadata', {'fields': ( 'subject_category', 'subject_name', 'facility', ), } ),
					( 'Compatibility', {'fields': ('old_ids', ), }),
				)	
	
	ordering = ('id', )
	richtext_fields = ('description',)
	links = ()

class LogoAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', 'resolution','x_size','y_size', view_link('logos') )
	list_filter = ( 'title', 'published', 'last_modified', 'resolution','x_size','y_size')
	list_editable = ( 'title', 'published', 'resolution','x_size','y_size' )
	search_fields = ( 'id', 'old_ids', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'credit', ), } ),
					( 'Screen', {'fields': ( 'resolution', 'x_size', 'y_size'), } ),
					( 'Compatibility', {'fields': ('old_ids', ), }),
				)
	ordering = ('id', )
	richtext_fields = ('description',)

	links = ()

class ConferencePosterAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified',  'resolution','x_size','y_size', view_link('conference_posters') )
	list_filter = ( 'title', 'published', 'last_modified',  'resolution','x_size','y_size')
	list_editable = ( 'title', 'published',  'resolution','x_size','y_size')
	search_fields = ( 'id', 'old_ids', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'width', 'height', 'weight', 'credit', ), } ),
					( 'Screen', {'fields': ( 'resolution', 'x_size', 'y_size'), } ),
					( 'Compatibility', {'fields': ('old_ids', ), }),
				)
	ordering = ('id', )
	richtext_fields = ('description',)
	links = ()

class TechnicalDocumentAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', view_link('techdocs') )
	list_filter = ( 'title', 'published', 'last_modified',  )
	list_editable = ( 'title', 'published', )
	search_fields = ( 'id', 'old_ids', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'pages', 'width', 'height', 'weight', 'credit', ), } ),
					( 'Shop', {'fields': ( 'sale', 'price', 'delivery', ), }),
					( 'Compatibility', {'fields': ('old_ids', ), }),
				)	
	ordering = ('id', )
	richtext_fields = ('description',)
	links = ()


#TODO: why don't we create a nice py decorator for this ? 
def register_with_admin( admin_site ):
	admin_site.register( Logo, LogoAdmin )
	admin_site.register( ConferencePoster, ConferencePosterAdmin )
	admin_site.register( TechnicalDocument, TechnicalDocumentAdmin )
	admin_site.register( Announcement, AnnouncementAdmin )

	
# Register with default admin site	
register_with_admin( admin.site )