# Djangoplicity
# Copyright 2007-2008 ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch, reverse
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from djangoplicity.archives.contrib.admin import ArchiveAdmin, RenameAdmin, \
	view_link, product_link
from djangoplicity.contrib.admin import DjangoplicityModelAdmin
from spacetelescope.archives.models import *


def _getDefaultShopAdmin(prefix,with_pages=False, extra_fields=()):
	"""
	Returns the DefaultShopAdmin classes.
	The only customization they need is the view_link,
	since it's based on the prefix of the archive
	"""
	class DefaultShopAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
		"""
		All Shop Products have the same fields, thus admin.
		Except for products with pages (see DefaultShopAdminWithPages)
		"""
		thumbnail_resource = 'thumb' 
		list_display = ( 'id', 'list_link_thumbnail', 'title', 'published','priority','last_modified', view_link(prefix), 'sale', 'price', product_link('adminshop_site') )
		list_filter = ( 'published', 'sale', 'last_modified',  )
		list_editable = ( 'title', 'priority' )
		search_fields = ( 'id', 'title', 'description', 'credit' )
		date_hierarchy = 'last_modified'
		fieldsets = (
						( None, {'fields': ( 'id', ) } ),
						( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
						( 'Archive', {'fields': ( 'title', 'description', 'width', 'height', 'weight', 'credit', ) + extra_fields, } ),
						( 'Shop', {'fields': ( 'sale', 'price', 'job', 'jsp' ), }),
					)
		ordering = ('-last_modified', )
		richtext_fields = ('description','credit',)
		actions = ['action_toggle_published','action_toggle_sale']
		#links = ()

	class DefaultShopAdminWithPages (DefaultShopAdmin):
		"""
		Derived from DefaultShopAdmin, adding pages to fieldsets
		"""
		fieldsets = (
						( None, {'fields': ( 'id', ) } ),
						( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
						( 'Archive', {'fields': ( 'title', 'description', 'pages', 'width', 'height', 'weight', 'credit', ), } ),
						( 'Shop', {'fields': ( 'sale', 'price', 'job', 'jsp' ), }),
					)	
		
	if with_pages:
		return DefaultShopAdminWithPages
	else:
		return DefaultShopAdmin
	



class KidsDrawingAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', view_link('drawings') )
	list_filter = ( 'title', 'published', 'last_modified',  )
	list_editable = ( 'title', 'published', )
	search_fields = ( 'id', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id',) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'credit', ), } ),
					( 'Author', {'fields': ( 'author_name', 'author_city', 'author_age' ), } ),
				)
	ordering = ('id', )
	richtext_fields = ('description',)
	links = ()
	
	#class Media:
	#	css = { 'all' : (settings.MEDIA_URL + settings.SUBJECT_CATEGORY_CSS,) } # Extra widget for subject category field


class AnnouncementAdmin (DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', view_link('announcements') )
	list_filter = ( 'title', 'published', 'last_modified',  )
	list_editable = ( 'title', 'published', )
	search_fields = ( 'id', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'credit', 'links','contacts'), } ),
					( 'Metadata', {'fields': ( 'subject_category', 'subject_name', 'facility', ), } ),
				)	
	
	ordering = ('id', )
	richtext_fields = ('description',)
	links = ()

class LogoAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', 'resolution','x_size','y_size', view_link('logos') )
	list_filter = ( 'title', 'published', 'last_modified', 'resolution','x_size','y_size')
	list_editable = ( 'title', 'published', 'resolution','x_size','y_size' )
	search_fields = ( 'id', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'credit', ), } ),
					( 'Screen', {'fields': ( 'resolution', 'x_size', 'y_size'), } ),
				)
	ordering = ('id', )
	richtext_fields = ('description',)

	links = ()

class ConferencePosterAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified',  'resolution','x_size','y_size', view_link('conference_posters') )
	list_filter = ( 'title', 'published', 'last_modified',  'resolution','x_size','y_size')
	list_editable = ( 'title', 'published',  'resolution','x_size','y_size')
	search_fields = ( 'id', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'width', 'height', 'weight', 'credit', ), } ),
					( 'Screen', {'fields': ( 'resolution', 'x_size', 'y_size'), } ),
				)
	ordering = ('id', )
	richtext_fields = ('description',)
	links = ()
	

def register_with_admin( admin_site ):
	admin_site.register( EducationalMaterial, _getDefaultShopAdmin( 'education', with_pages = True ) )
	#admin_site.register( KidsDrawingAuthor, KidsDrawingAuthorAdmin )	
	admin_site.register( KidsDrawing, KidsDrawingAdmin )
	
	admin_site.register( CDROM, _getDefaultShopAdmin('cdroms',with_pages=False) )
	admin_site.register( Book, _getDefaultShopAdmin( 'books', with_pages = True ) )
	admin_site.register( Brochure, _getDefaultShopAdmin( 'brochures', with_pages = True ) )
	admin_site.register( Merchandise, _getDefaultShopAdmin( 'merchandise', with_pages = False ) )
	admin_site.register( Newsletter, _getDefaultShopAdmin( 'newsletters', with_pages = True ) )
	admin_site.register( PostCard, _getDefaultShopAdmin( 'postcards', with_pages = False ) )
	admin_site.register( Poster, _getDefaultShopAdmin('posters',extra_fields=('x_size','y_size','resolution'),with_pages=False) )
	#admin_site.register( PressKit, _getDefaultShopAdmin('presskits',with_pages=True) )
	admin_site.register( Sticker, _getDefaultShopAdmin( 'stickers', with_pages = False ) )
	
	
#	admin_site.register( Logo, LogoAdmin )
#	admin_site.register( ConferencePoster, ConferencePosterAdmin )
	admin_site.register( TechnicalDocument, _getDefaultShopAdmin( 'techdocs', with_pages = True ) )
#	admin_site.register( Announcement, AnnouncementAdmin )
	
	
# Register with default admin site	
register_with_admin( admin.site )