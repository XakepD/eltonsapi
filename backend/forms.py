from django import forms
from .models import Gallery, GalleryImage

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['gallery', 'image']
        widgets = {
            'gallery': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class GalleryImageInlineFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = self.queryset.filter(gallery=self.instance)  # Filter images by the gallery instance

    def clean(self):
        super().clean()
        if not self.cleaned_data:
            raise forms.ValidationError("At least one image is required.")
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('image'):
                raise forms.ValidationError("Image is required for each form.")
            