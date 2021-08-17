# Base View Sets
from rest_framework import viewsets, status, permissions
from .serializers import *
from .models import *


class BaseApiViewSets(viewsets.ModelViewSet):
    def perform_destroy(self, instance):
        instance.my_delete()


# Order Api View Sets
class OrderApiViewSets(BaseApiViewSets):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        if serializer.validated_data['status']:
            order: Order = self.get_object()

            if serializer.validated_data['status'] == 'c':
                for i in order.ordermenuitem_set.all():
                    i.menu_item_variant.count += i.quantity
                    i.menu_item_variant.save()

        serializer.save()


# Order Short Api View Sets
class OrderShortApiViewSets(BaseApiViewSets):
    serializer_class = OrderShortSerializer
    queryset = Order.objects.all()


# Order MenuItem Api View Sets
class OrderMenuItemApiViewSets(BaseApiViewSets):
    serializer_class = OrderMenuItemSerializer
    queryset = OrderMenuItem.objects.all()

    def perform_update(self, serializer):
        if serializer.validated_data['quantity']:
            order_item: OrderMenuItem = self.get_object()

            if serializer.validated_data['quantity'] < order_item.quantity:
                count = order_item.quantity - serializer.validated_data['quantity']
                order_item.menu_item_variant.count += count

            else:
                count = serializer.validated_data['quantity'] - order_item.quantity
                order_item.menu_item_variant.count -= count

            order_item.menu_item_variant.save()

        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance: OrderMenuItem = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['quantity'] > instance.quantity:
            count = serializer.validated_data['quantity'] - instance.quantity
            if count > instance.menu_item_variant.count:
                my_errors = {
                    "quantity": [
                        "The number requested is more than the number of inventories."
                    ]
                }

                return Response(my_errors, status=400)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.menu_item_variant.count += instance.quantity
        instance.menu_item_variant.save()


# Order MenuItem Short Api View Sets
class OrderMenuItemShortApiViewSets(BaseApiViewSets):
    serializer_class = OrderMenuItemShortSerializer
    queryset = OrderMenuItem.objects.all()

    def perform_create(self, serializer: OrderMenuItemShortSerializer):
        serializer.validated_data['menu_item_variant'].count -= serializer.validated_data['quantity']
        serializer.validated_data['menu_item_variant'].save()
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['quantity'] > serializer.validated_data['menu_item_variant'].count:
            my_errors = {
                "quantity": [
                    "The number requested is more than the number of inventories."
                ]
            }

            return Response(my_errors, status=400)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderMenuItemShortApiViewSets(OrderMenuItemAdminApiViewSets):
    serializer_class = OrderMenuItemShortSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return OrderMenuItem.objects.filter(order__customer=customer)
