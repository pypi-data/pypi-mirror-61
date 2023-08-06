'''
Created on 30.9.2010

@author: xaralis
'''

from django.contrib import admin

from reversion.admin import VersionAdmin

class SystemModelAdmin(admin.ModelAdmin):
    """
    Abstract admin class to enable better handling of SystemModel subclasses
    """
    change_form_template = "system_models/change_form.html"
    uneditable_fields = ()
    
    def get_readonly_fields(self, request, obj=None):
        if obj and not obj.deleteable: # when editing an object
            return self.readonly_fields + self.uneditable_fields
        return self.readonly_fields
    
    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return obj.deleteable
        return super(SystemModelAdmin, self).has_delete_permission(request, obj)
    
class VersionedSystemModelAdmin(VersionAdmin, SystemModelAdmin):
    """
    Abstract admin class to enable better handling of SystemModel subclasses
    which use versioning
    """
    pass