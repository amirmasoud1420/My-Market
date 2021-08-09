from rest_framework import generics
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from django.http import JsonResponse


class ProductListApiView(generics.ListCreateAPIView):
    queryset = MenuItemVariant.objects.all()
    serializer_class = MenuItemVariantSerializer


class ProductDetailView(
    generics.mixins.RetrieveModelMixin,
    generics.mixins.UpdateModelMixin,
    generics.mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = MenuItemVariant.objects.all()
    serializer_class = MenuItemVariantSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.my_delete()


@csrf_exempt
def ProductApiView(request):
    if request.method == 'GET':
        m = MenuItemVariant.objects.all()
        s = MenuItemVariantSerializer(m, many=True)
        print(s.data)
        return JsonResponse({'products': s.data})

    elif request.method == 'POST':
        s = MenuItemVariantSerializer(data=request.POST)
        if s.is_valid():
            s.save()
            return JsonResponse({"Product : ": s.data})
        else:
            return JsonResponse({"errors : ": s.errors})
