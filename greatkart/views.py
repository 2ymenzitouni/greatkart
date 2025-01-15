from django.shortcuts import render
from store.models import Product
# Create your views here.
def home(request):
    products = Product.objects.all()
    context = {
        'products' : products
    }
    return render(request,'home.html' , context)