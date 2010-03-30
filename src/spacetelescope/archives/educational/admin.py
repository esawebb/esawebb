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
from spacetelescope.archives.educational.models import EducationalMaterial, KidsDrawing
from djangoplicity.archives.contrib.admin import ArchiveAdmin, RenameAdmin, view_link
from django.forms import ModelForm
from django.core.urlresolvers import NoReverseMatch, reverse
from django.utils.safestring import mark_safe



class EducationalMaterialAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', view_link('education') )
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
	
	#class Media:
	#	css = { 'all' : (settings.MEDIA_URL + settings.SUBJECT_CATEGORY_CSS,) } # Extra widget for subject category field



class KidsDrawingAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', view_link('drawings') )
	list_filter = ( 'title', 'published', 'last_modified',  )
	list_editable = ( 'title', 'published', )
	search_fields = ( 'id', 'old_ids', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id',) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'credit', ), } ),
					( 'Author', {'fields': ( 'author_name', 'author_city', 'author_age' ), } ),
					( 'Compatibility', {'fields': ('old_ids', ), }),
				)
	ordering = ('id', )
	richtext_fields = ('description',)
	links = ()
	
	#class Media:
	#	css = { 'all' : (settings.MEDIA_URL + settings.SUBJECT_CATEGORY_CSS,) } # Extra widget for subject category field


#class KidsDrawingAuthorAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
#	list_display = ( 'name', 'age','city', )
#	list_filter = ( 'city', 'age',  )
#	list_editable = ( 'age', 'city' )
#	search_fields = ( 'name', 'city', )
#	fieldsets = (
#					( 'Information', {'fields':  ( 'name', 'age', 'city' ), } ),
#				)


def register_with_admin( admin_site ):
	admin_site.register( EducationalMaterial, EducationalMaterialAdmin )
	#admin_site.register( KidsDrawingAuthor, KidsDrawingAuthorAdmin )	
	admin_site.register( KidsDrawing, KidsDrawingAdmin )
	
	
# Register with default admin site	
register_with_admin( admin.site )