from django.contrib import admin
from emp.apps.profiles.models  import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
	"""
	list_display   = ('',)
	list_filter    = ('',)
	search_fields  = ('',)
	"""
	date_hierarchy = 'join_date'

admin.site.register(UserProfile)
