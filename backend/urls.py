from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GalleryViewSet, GalleryImageViewSet, GalleryImagesViewSet, RandomGalleryImageViewSet, AdminLoginView
from django.conf import settings
from django.conf.urls.static import static

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'images', GalleryImagesViewSet, basename='gallery-images-all')
router.register(r'random-images', RandomGalleryImageViewSet, basename='random-gallery-images')

urlpatterns = [
    path("", include(router.urls)),
    
    path("image/<slug:slug>/", GalleryImageViewSet.as_view(), name="gallery-images"),


    path("admin-login/", AdminLoginView.as_view(), name="admin-login"),
    
    

]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)