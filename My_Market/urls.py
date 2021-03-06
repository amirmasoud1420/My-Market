"""My_Market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
import My_Market.settings as settings
from product.views import *

urlpatterns = i18n_patterns(
    path('', HomeView.as_view(), name='home'),
    path('change-lang/', ChangeLanguageView.as_view(), name='change_lang'),
    path('admin/', admin.site.urls),
    path('product/', include('product.urls')),
    path('customer/', include('customer.urls')),
    path('order/', include('order.urls')),
    path('product-api/', include('product.api_urls')),
    path('customer-api/', include('customer.api_urls')),
    path('order-api/', include('order.api_urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    prefix_default_language=True,
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
