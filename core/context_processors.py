from My_Market.settings import LANGUAGE_CODE
from product.models import Category
from django.utils.translation import activate, get_language


def my_contexts(request):
    category = Category.objects.filter(is_sub_category=False)
    return {
        'category': category,
        'language': get_language(),
    }
