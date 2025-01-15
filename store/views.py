from django.shortcuts import render,get_object_or_404
from .models import Product
from django.http import HttpResponse
from django.db.models import Q
from category.models import Category
from carts.models import Cart , CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage , PageNotAnInteger , Paginator
# Create your views here.

def store (request , category_slug = None):
    categories = None
    products = None

    if category_slug != None:
        categories =get_object_or_404(Category,slug = category_slug)
        products = Product.objects.filter(category = categories ,is_available = True)
        paginator = Paginator(products , 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
            products = Product.objects.all().filter(is_available = True)
            paginator = Paginator(products , 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
    context={
        'products' : paged_products,
        'product_count' : products.count(),
    }
    return render(request,'store.html',context)

def product_detail(request, category_slug , product_slug):
    single_product = get_object_or_404(Product,category__slug = category_slug , slug = product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request) , product = single_product).exists()
    context = {
        'single_product' : single_product,
        'in_cart' : in_cart,
    }
    return render(request , 'product-detail.html' , context)

def search(request):
    if 'keyword' in request.GET :
        keyword = request.GET['keyword']
        if keyword : # input search which is named keyword has a value
            products = Product.objects.order_by('-created_date').filter(Q (description__icontains = keyword) | Q (product_name__icontains = keyword))
    context = {
        'products' : products,
        'product_count' : products.count(),
    }
    return render(request,'store.html' , context)