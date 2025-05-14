from django.contrib import admin
from Unibites.models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","__str__","description")
    list_display_links = ()
    list_filter = ("name",)
    list_select_related = False
    list_per_page = 100
    list_max_show_all = 200
    list_editable = ("description",)
    search_fields = ("name",)

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name","email","number","status",)
    list_display_links = ()
    list_filter = ("status",)
    list_select_related = False
    list_per_page = 100
    list_max_show_all = 200
    list_editable = ("status",)
    search_fields = ("name","email","number",)

class CanteenAdmin(admin.ModelAdmin):
    list_display = ("id", "name","email","number", "location", "image", "status",)
    list_display_links = ()
    list_filter = ("status",)
    list_select_related = False
    list_per_page = 100
    list_max_show_all = 200
    list_editable = ("status",)
    search_fields = ("name","email","location",)


admin.site.site_header = "UniBites Administration Panel"
admin.site.site_title = "UniBites Admin Portal"
admin.site.index_title = "Welcome to the UniBites Administration"

admin.site.register(Canteen, CanteenAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
