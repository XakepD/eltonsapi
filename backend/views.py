from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Gallery, GalleryImage
from .serializers import GallerySerializer, GalleryImageSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

class AdminLoginView(ObtainAuthToken):
    """
    ViewSet for admin login to generate an authentication token.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token_key = response.data.get('token')  # Safely get the token key
        if not token_key:
            return Response({'error': 'Token not found in response.'}, status=400)

        try:
            token = Token.objects.get(key=token_key)  # Correctly retrieve the token object
            user = token.user
            if user.is_staff:  # Ensure the user is an admin
                return Response({
                    'token': token.key,
                    'username': user.username,
                    'email': user.email,
                })
            else:
                token.delete()  # Delete the token if the user is not an admin
                return Response({'error': 'Only admins can log in.'}, status=403)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token.'}, status=400)

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to provide information about the login endpoint.
        """
        return Response({
            'message': 'This endpoint is for admin login. Please use POST with username and password.'
        }, status=200)

class GalleryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Gallery.
    """
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

class GalleryImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on GalleryImage.
    Filters images based on the Gallery slug.
    """
    serializer_class = GalleryImageSerializer

    def get_queryset(self):
        gallery_slug = self.kwargs.get('slug')  # Retrieve the slug from the URL
        gallery = get_object_or_404(Gallery, slug=gallery_slug)  # Get the Gallery object
        return GalleryImage.objects.filter(gallery=gallery)  # Filter images by the gallery

class GalleryImagesViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on all GalleryImage objects.
    """
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
import random

class RandomGalleryImageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving 5 random images from the GalleryImage model.
    """
    serializer_class = GalleryImageSerializer

    def get_queryset(self):
        all_images = list(GalleryImage.objects.all())  # Get all images as a list
        return random.sample(all_images, min(len(all_images), 5))  # Select up to 5 random images