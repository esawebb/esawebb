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
from spacetelescope.archives.products.models import *
from djangoplicity.archives.contrib.admin import ArchiveAdmin, RenameAdmin, view_link
from django.forms import ModelForm
from django.core.urlresolvers import NoReverseMatch, reverse
from django.utils.safestring import mark_safe

#TODO SLIDER FOR PRIO

def _getDefaultShopAdmin(prefix,with_pages=False):
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
		list_display = ( 'id', 'title', 'published','priority','last_modified', view_link(prefix) )
		list_filter = ( 'title', 'published', 'last_modified',  )
		list_editable = ( 'title', 'published', )
		search_fields = ( 'id', 'old_ids', 'title', 'description', 'credit' )
		date_hierarchy = 'last_modified'
		fieldsets = (
						( None, {'fields': ( 'id', ) } ),
						( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
						( 'Archive', {'fields': ( 'title', 'description', 'width', 'height', 'weight', 'credit', ), } ),
						( 'Shop', {'fields': ( 'sale', 'price', 'delivery', ), }),
						( 'Compatibility', {'fields': ('old_ids', ), }),
					)
		ordering = ('id', )
		richtext_fields = ('description',)
		links = ()

	class DefaultShopAdminWithPages (DefaultShopAdmin):
		"""
		Derived from DefaultShopAdmin, adding pages to fieldsets
		"""
		fieldsets = (
						( None, {'fields': ( 'id', ) } ),
						( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
						( 'Archive', {'fields': ( 'title', 'description', 'pages', 'width', 'height', 'weight', 'credit', ), } ),
						( 'Shop', {'fields': ( 'sale', 'price', 'delivery', ), }),
						( 'Compatibility', {'fields': ('old_ids', ), }),
					)	
		
	if with_pages:
		return DefaultShopAdminWithPages
	else:
		return DefaultShopAdmin

BookAdmin = _getDefaultShopAdmin('books',with_pages=True)
BookAdmin.fieldsets = (
						( None, {'fields': ( 'id', ) } ),
						( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
						( 'Archive', {'fields': ( 'title', 'description', 'pages', 'width', 'height', 'weight', 'credit', ), } ),
						( 'Shop', {'fields': ( 'sale', 'price', ), }),
						( 'Compatibility', {'fields': ('old_ids', ), }),
					)

def register_with_admin( admin_site ):
	admin_site.register( CDROM, _getDefaultShopAdmin('cdroms',with_pages=False) )
	admin_site.register( Book, BookAdmin )
	admin_site.register( Brochure, _getDefaultShopAdmin('brochures',with_pages=True) )
	admin_site.register( Merchandise, _getDefaultShopAdmin('merchandise',with_pages=False) )
	admin_site.register( Newsletter, _getDefaultShopAdmin('newsletters',with_pages=True) )
	admin_site.register( PostCard, _getDefaultShopAdmin('postcards',with_pages=False) )
	admin_site.register( Poster, _getDefaultShopAdmin('posters',with_pages=False) )
	admin_site.register( PressKit, _getDefaultShopAdmin('presskits',with_pages=True) )
	admin_site.register( Sticker, _getDefaultShopAdmin('stickers',with_pages=False) )
	
	
# Register with default admin site	
register_with_admin( admin.site )