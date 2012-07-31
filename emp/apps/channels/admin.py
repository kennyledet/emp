from django.contrib import admin
from emp.apps.channels.models  import UserChannel

class UserChannelAdmin(admin.ModelAdmin):
    """
    list_display   = ('',)
    list_filter    = ('',)
    search_fields  = ('',)
    """

admin.site.register(UserChannel)
