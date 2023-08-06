from django.contrib import admin

from fragapy.currencies.models import Currency


class CurrencyAdmin(admin.ModelAdmin):
	list_display = ('is_default', 'code', 'name', 'symbol', 'factor')
	list_display_links = ('name',)
	
	def has_delete_permission(self, *args, **kwargs):
	    return False

admin.site.register(Currency, CurrencyAdmin)
