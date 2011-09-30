from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django_auth_ldap.backend import populate_user
from django_auth_ldap.backend import LDAPBackend

def user_create_handler( sender=None, instance=None, created=None, raw=False, **kwargs ):
	"""
	When creating a user via the admin. Populate the user from ldap if possible.
	"""
	if created and not raw:
		try:
			backend = LDAPBackend()
			u = backend.populate_user( instance.username )
			u.set_unusable_password()
			u.save()
		except Exception:
			pass
		
#def populate_user_handler( sender=None, user=None, ldap_user=None, **kwargs ):
#	print ldap_user.attrs

post_save.connect( user_create_handler, User )
#populate_user.connect( populate_user_handler, LDAPBackend )