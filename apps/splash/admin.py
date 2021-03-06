from django.contrib import admin

from apps.splash.models import SplashYear, SplashEvent

from reversion.admin import VersionAdmin


class SplashYearAdmin(VersionAdmin):
    list_display = ('title', 'start_date',)

class SplashEventAdmin(VersionAdmin):
    exclude = ('',)


admin.site.register(SplashYear, SplashYearAdmin)
admin.site.register(SplashEvent, SplashEventAdmin)