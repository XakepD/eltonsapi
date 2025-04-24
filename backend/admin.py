from django.contrib import admin
from .models import Gallery, GalleryImage



# Register your models here.

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    inlines = [GalleryImageInline]

admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryImage)