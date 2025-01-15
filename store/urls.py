from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('' , views.store , name = 'store'),
    path('category/<slug:category_slug>/' , views.store , name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/' , views.product_detail , name='product_detail'),
    path('search/' , views.search , name = 'search'),
]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
