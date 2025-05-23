from django import forms
from .models import product , product_image , review

class productForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ('name', 'price', 'description' , 'discount_parcentage' , 'stock' , 'available' , 'unit' , 'rating' , 'category')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = review
        fields = ['rating', 'reviews' , 'is_approved']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1, 'max': 5,
                'class': 'w-full border border-gray-300 p-2 rounded',
                'placeholder': 'Rate 1-5'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 p-2 rounded',
                'placeholder': 'Write your review here...',
                'rows': 4
            }),
        }