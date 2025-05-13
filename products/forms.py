from django import forms
from .models import product , product_image

class productForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ('name', 'price', 'description' , 'discount_parcentage' , 'stock' , 'available' , 'unit' , 'rating' , 'category')