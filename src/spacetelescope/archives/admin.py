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
	

#
#
#
def StandardAdminFactory( prefix, remove=['release_date', 'embargo_date','links','contacts'] ):
	filter_fields = lambda field_list: filter( lambda x: x not in remove, field_list )
	
	class StandardArchiveAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
		thumbnail_resource = 'thumb' 
		list_display = filter_fields( ( 'id', 'list_link_thumbnail', 'title', 'published', 'priority', 'release_date', 'embargo_date', 'last_modified', view_link( prefix ), ) )
		list_filter = filter_fields( ( 'published', 'last_modified', 'release_date', 'embargo_date', ) )
		list_editable = filter_fields( ( 'title', 'priority') )
		search_fields = filter_fields( ( 'id', 'title', 'description', 'credit' ) )
		date_hierarchy = 'last_modified'
		ordering = filter_fields( ( '-release_date', '-last_modified', ) )
		richtext_fields = filter_fields( ( 'description', 'credit', 'contacts', 'links' ) )
		actions = ['action_toggle_published', ]
		fieldsets = ( 
						( None, {'fields': ( 'id', ) } ),
						( 'Publishing', {'fields': filter_fields( ( 'published', 'priority', 'release_date', 'embargo_date' ) ), } ),
						( 'Archive', {'fields': filter_fields( ( 'title', 'description', 'credit', 'links', 'contacts' ) ), } ),
					)
	return StandardArchiveAdmin
	

#
#
#
class AnnouncementAdmin( StandardAdminFactory( 'announcements', remove = [ 'priority','credit' ] ) ):
	date_hierarchy = 'release_date'
	

class KidsDrawingAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', view_link('drawings') )
	list_filter = ( 'title', 'published', 'last_modified',  )
	list_editable = ( 'title', 'published', 'priority' )
	search_fields = ( 'id', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id',) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'credit', ), } ),
					( 'Author', {'fields': ( 'name', 'city', 'age' ), } ),
				)
	ordering = ('id', )
	richtext_fields = ('description',)
	actions = ['action_toggle_published',]
	links = ()
	
	#class Media:
	#	css = { 'all' : (settings.MEDIA_URL + settings.SUBJECT_CATEGORY_CSS,) } # Extra widget for subject category field


	

class LogoAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', view_link('logos') )
	list_filter = ( 'title', 'published', 'last_modified', )
	list_editable = ( 'title', 'published', 'resolution',)
	search_fields = ( 'id', 'title', 'description', 'credit','priority' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'credit', ), } ),
				)
	ordering = ('id', )
	richtext_fields = ('description',)
	actions = ['action_toggle_published',]

	links = ()

class ConferencePosterAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified',  'resolution','x_size','y_size', view_link('conference_posters') )
	list_filter = ( 'title', 'published', 'last_modified',  'resolution','x_size','y_size')
	list_editable = ( 'title', 'published',  'resolution','x_size','y_size','priority')
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
	actions = ['action_toggle_published',]
	links = ()
	
	
class CalendarAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'year', 'month','priority','last_modified', 'published',view_link('calendars') )
	list_filter = ( 'year', 'month', 'published', 'last_modified',  )
	list_editable = ( 'published', 'priority')
	search_fields = ( 'id', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', 'title' ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'year', 'month', 'description', 'credit', ), } ),
				)
	ordering = ('id', )
	richtext_fields = ('description',)
	actions = ['action_toggle_published',]
	links = ()
	

def artist (obj):
	return 	obj.artist.name.encode('ascii')

class OnlineArtAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', view_link('art') )
	list_filter = ( 'title', 'published', 'last_modified', )
	list_editable = ( 'title', 'published', 'priority' )
	search_fields = ( 'id', 'title', 'description', 'artist', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'credit', 'artist'), } ),
				)
	ordering = ('id', )
	#raw_id_fields = ('artist', )
	richtext_fields = ('description',)
	actions = ['action_toggle_published',]

	links = ()
	
class OnlineArtAuthorAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'name', 'city', 'country', 'email', 'published','priority','last_modified', view_link('artists') ) 
	list_filter = ( 'city', 'country',)
	list_editable = ( 'name', 'priority' )
	search_fields = ( 'name', 'city', 'country', 'email',)
	date_hierarchy = 'last_modified'
	search_fields = ( 'id', 'name', 'priority' )
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'name', 'description', 'credit', 'city', 'country', 'link'), } ),
				)
	ordering = ('name', )
	richtext_fields = ('description',)
	actions = ['action_toggle_published',]
	links = ()

#TODO printlayouts remain?
#class PrintLayoutAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
#	list_display = ( 'id', 'title', 'published','priority','last_modified', view_link('printlayouts') )
#	list_filter = ( 'title', 'published', 'last_modified', )
#	list_editable = ( 'title', 'published', )
#	search_fields = ( 'id', 'title', 'description', 'credit' )
#	date_hierarchy = 'last_modified'
#	fieldsets = (
#					( None, {'fields': ( 'id', ) } ),
#					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
#					( 'Archive', {'fields': ( 'title', 'description', 'credit', ), } ),
#				)
#	ordering = ('id', )
#	richtext_fields = ('description',)
#
#	links = ()


class SlideShowAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	thumbnail_resource = 'thumb' 
	list_display = ( 'id', 'title', 'published','priority','last_modified', 'resolution','x_size','y_size', view_link('slideshows') )
	list_filter = ( 'title', 'published', 'last_modified', 'resolution','x_size','y_size')
	list_editable = ( 'title', 'published', 'resolution','x_size','y_size' ,'priority')
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
	actions = ['action_toggle_published',]

	links = ()
	


class ExhibitionAdmin (DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', view_link('announcements') )
	list_filter = ( 'title', 'published', 'last_modified',  )
	list_editable = ( 'title', 'published','priority' )
	search_fields = ( 'id', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'credit',), } ),
				)	
	
	ordering = ('id', )
	richtext_fields = ('description',)
	actions = ['action_toggle_published',]
	links = ()

class FITSImageAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', view_link('announcements') )
	list_filter = ( 'title', 'published', 'last_modified',  )
	list_editable = ( 'title', 'published','priority' )
	search_fields = ( 'id', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'credit', 'country','city' ), } ),
				)	
	
	ordering = ('id', )
	richtext_fields = ('description',)
	actions = ['action_toggle_published',]
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
	admin_site.register( Announcement, AnnouncementAdmin )

	admin_site.register( Calendar, CalendarAdmin )
	admin_site.register( OnlineArt, OnlineArtAdmin )
	admin_site.register( OnlineArtAuthor, OnlineArtAuthorAdmin )
	#admin_site.register( PrintLayout, PrintLayoutAdmin )
	admin_site.register( SlideShow, SlideShowAdmin )
	
	admin_site.register( Exhibition, ExhibitionAdmin )
	admin_site.register( FITSImage, FITSImageAdmin )
	
	
# Register with default admin site	
register_with_admin( admin.site )