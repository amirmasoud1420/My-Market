from My_Market.settings import LANGUAGE_CODE
from product.models import Category


def my_contexts(request):
    category = Category.objects.filter(is_sub_category=False)
    return {
        'category': category,
        'language': LANGUAGE_CODE,
    }
