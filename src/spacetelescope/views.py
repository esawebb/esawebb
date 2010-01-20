# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponsePermanentRedirect, Http404, HttpResponseNotFound
from django.template import Context, RequestContext, loader
from django.views import defaults as default_views 

#from djangoplicity.media.models import Image
#from libavm.utils import avm_from_file


def main_page( request ):
	""" Main Page view """
	
	#im = Image.objects.get(pk='heic0515a')
	#file_path = im.resource_original.path
	#avm = avm_from_file(str(file_path))
		
	return render_to_response('base.html', {}, context_instance=RequestContext(request) )


#def page_not_found( request, template_name='404_site.html' ):
#	"""
#	Default 404 handler.
#
#	Templates: `404.html`
#	Context:
#		request_path
#			The path of the requested URL (e.g., '/app/pages/bad_page/')
#	"""
#	path = request.path
#	
#	if path.startswith("/gallery/") or path.startswith("/public/outreach/press-rel/"):
#		t = loader.select_template(["404_new_archive.html","404.html"]) 
#		return HttpResponseNotFound(t.render(RequestContext(request, {'request_path': request.path})))
#	else:
#		return default_views.page_not_found( request, template_name='404.html' )		
#		