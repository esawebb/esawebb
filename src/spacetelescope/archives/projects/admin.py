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
from spacetelescope.archives.projects.models import *
from djangoplicity.archives.contrib.admin import ArchiveAdmin, RenameAdmin, view_link
from django.forms import ModelForm
from django.core.urlresolvers import NoReverseMatch, reverse
from django.utils.safestring import mark_safe



class ExhibitionAdmin (DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
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

class FITSImageAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', view_link('announcements') )
	list_filter = ( 'title', 'published', 'last_modified',  )
	list_editable = ( 'title', 'published', )
	search_fields = ( 'id', 'old_ids', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'credit', 'country','city', 'links','contacts'), } ),
					( 'Metadata', {'fields': ( 'subject_category', 'subject_name', 'facility', ), } ),
					( 'Compatibility', {'fields': ('old_ids', ), }),
				)	
	
	ordering = ('id', )
	richtext_fields = ('description',)
	links = ()



def register_with_admin( admin_site ):
	admin_site.register( Exhibition, ExhibitionAdmin )
	admin_site.register( FITSImage, FITSImageAdmin )

	
# Register with default admin site	
register_with_admin( admin.site )