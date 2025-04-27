from .models import Gallery, GalleryImage
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin, TabularInline


# Unregister default User and Group models
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    """
    Custom User admin using Unfold.
    """
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """
    Custom Group admin using Unfold.
    """
    pass


# Register your models with Unfold

class GalleryImageInline(TabularInline):
    """
    Inline for GalleryImage using Unfold.
    """
    model = GalleryImage
    extra = 1


@admin.register(Gallery)
class GalleryAdmin(ModelAdmin):
    """
    Admin for Gallery using Unfold.
    """
    list_display = ('title', 'description', 'slug', 'created_at')
    inlines = [GalleryImageInline]


@admin.register(GalleryImage)
class GalleryImageAdmin(ModelAdmin):
    """
    Admin for GalleryImage using Unfold.
    """
    list_display = ('id', 'gallery', 'image', 'created_at')