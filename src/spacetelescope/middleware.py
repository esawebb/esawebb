# -*- coding: utf-8 -*-
#
# spacetelescope
# Copyright (c) 2007-2015, European Southern Observatory (ESO)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the European Southern Observatory nor the names
#      of its contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY ESO ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL ESO BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE

from django.conf import settings

from netaddr import IPSet, IPNetwork


class DisableInternalCDN(object):
	'''
	The CDN for resources is set in
	djangoplicity.archives.resources.ResourceManager which doesn't have access
	to the session, so it's not possible to disable the CDN in the Intranet.
	Moreover we actually want to use the CDN from Chile, so we only check if
	the client IP is in the Garching's ranges
	This Middleware is a bit of a hack and replaces URLs pointing to the CDN
	by local URLs
	'''
	def process_response(self, request, response):
		try:
			internal_ips = settings.GARCHING_INTERNAL_IPS
		except AttributeError:
			return response

		if 'external' in request.GET:
			# We simulate an external request, no changes
			return response

		# If we use NGINX as proxy REMOTE_ADDR will be 127.0.0.1
		# so we use HTTP_X_REAL_IP if available, otherwise we default
		# to REMOTE_ADDR
		if 'HTTP_X_REAL_IP' in request.META:
			key = 'HTTP_X_REAL_IP'
		else:
			key = 'REMOTE_ADDR'

		ip = request.META[key]

		if response.status_code == 200 and not response.streaming:
			content_type = response.get('Content-Type', '')
			if 'text/' in content_type:
				internal_ips = IPSet([IPNetwork(i) for i in internal_ips])
				if ip in internal_ips:
					response.content = response.content.replace(
						'//cdn.spacetelescope.org/archives/',
						'//www.spacetelescope.org/static/archives/'
					).replace(
						'//cdn2.spacetelescope.org/archives/',
						'//www.spacetelescope.org/static/archives/'
					)

		return response
