from .serializers import *

from rest_framework import viewsets
from rest_framework import permissions
from .my_permissions import *


# Base View Sets
class BaseApiViewSets(viewsets.ModelViewSet):
    def perform_destroy(self, instance):
        instance.my_delete()


# User Api View Sets
class UserApiViewSets(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsUser | ISStaffObj]


# User Short Api View Sets
class UserShortApiViewSets(viewsets.ModelViewSet):
    serializer_class = UserShortSerializer
    queryset = User.objects.all()
    permission_classes = [UserListPermission]


# Customer Api View Sets
class CustomerApiViewSets(BaseApiViewSets):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsCustomer | ISStaffObj]


# Customer Short Api View Sets
class CustomerListAdminApiViewSets(BaseApiViewSets):
    serializer_class = CustomerShortSerializer
    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAuthenticated, ISStaffListPermission]


# Customer Short Api View Sets
class CustomerShortApiViewSets(BaseApiViewSets):
    serializer_class = CustomerShortSerializer

    # queryset = Customer.objects.all()

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    permission_classes = [permissions.IsAuthenticated, IsCustomer | ISStaffListPermission]


# Address Api View Sets
class AddressApiViewSets(BaseApiViewSets):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | ISStaffObj]


# Address Short Api View Sets
class AddressShortApiViewSets(BaseApiViewSets):
    serializer_class = AddressShortSerializer
    queryset = Address.objects.all()
    permission_classes = [permissions.IsAuthenticated, ISStaffListPermission]


class AddressListForCustomerApiViewSets(BaseApiViewSets):
    serializer_class = AddressShortSerializer

    # queryset = Address.objects.all()

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return Address.objects.filter(owner=customer)

    permission_classes = [permissions.IsAuthenticated]
