from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Gallery, GalleryImage
from .serializers import GallerySerializer, GalleryImageSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
import random
from django.db.models import Q

class GalleryImageViewSet(APIView):
    def get(self, request, slug):
        gallery = get_object_or_404(Gallery, slug=slug)
        images = GalleryImage.objects.filter(gallery=gallery)
        data = {
            "gallery_title": gallery.title,
            "gallery_description": gallery.description,
            "images": [
                {
                    "id": image.id,
                    "image": image.image.url,
                    "gallery": {"name": gallery.title},
                }
                for image in images
            ],
        }
        return Response(data)
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


class GalleryImagesViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on all GalleryImage objects.
    """
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer



class RandomGalleryImageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving random images from the GalleryImage model,
    excluding images from the Portraits gallery.
    """
    serializer_class = GalleryImageSerializer

    def get_queryset(self):
        # Get all images that are not in the Portraits gallery
        ex = Gallery.objects.get(title='Portraits')
        non_portrait_images = GalleryImage.objects.filter(
            ~Q(gallery=ex)
        )
        
        # Convert to list and select random samples
        image_list = list(non_portrait_images)
        return random.sample(image_list, min(len(image_list), 12))