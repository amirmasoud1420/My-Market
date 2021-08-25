from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, SuccessURLAllowedHostsMixin
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import generic, View
from .forms import *
from core.models import User
from .models import *
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout, forms, update_session_auth_hash
from django.contrib import messages
from django.core.paginator import Paginator
from product.models import *

# Create your views here.

class CustomerRegisterView(generic.FormView):
    template_name = 'customer/register.html'
    form_class = CustomerRegisterForm
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, _('Registration failed'), 'danger')
        return super().form_invalid(form)

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(
            phone=data['phone'],
            email=data['email'],
        )
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.set_password(data['password_2'])
        user.is_staff = False
        user.save()
        customer = Customer.objects.create(
            user=user
        )
        login(self.request, user)
        messages.success(self.request, _('Registration completed successfully'), 'success')
        return super().form_valid(form)


# class CustomerLoginView(generic.FormView):
# """
# login with phone and email
# problem : next redirect
# """
#     template_name = 'customer/login.html'
#     form_class = CustomerLoginForm
#     success_url = reverse_lazy('home')
#
#     def form_valid(self, form):
#         data = form.cleaned_data
#         try:
#             user = authenticate(request=self.request, phone=User.objects.get(email=data['username']).phone,
#                                 password=data['password'])
#         except:
#             user = authenticate(request=self.request, phone=data['username'], password=data['password'])
#         if user:
#             login(self.request, user)
#             messages.success(self.request, _('Welcome to RoshanMarket'), 'success')
#         else:
#             messages.error(self.request, _('Login failed'), 'danger')
#             return redirect('customer:customer_login')
#         return super().form_valid(form)


class CustomerLoginView(LoginView):
    template_name = 'customer/login.html'

    def form_invalid(self, form):
        messages.error(self.request, _('Login failed'), 'danger')
        return super().form_invalid(form)

    def form_valid(self, form):
        data = form.cleaned_data
        user = authenticate(request=self.request, phone=data['username'], password=data['password'])
        if user:
            login(self.request, user)
            messages.success(self.request, _('Welcome to RoshanMarket'), 'success')
        else:
            messages.error(self.request, _('Login failed'), 'danger')
            return redirect('customer:customer_login')
        return super().form_valid(form)


class CustomerLogoutView(generic.View):

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, _('You have successfully logged out'), 'success')
        print('logout!!!!!!!!!!!!!!')
        return redirect('home')


class CustomerProfileView(LoginRequiredMixin, generic.ListView):
    template_name = 'customer/profile.html'
    context_object_name = 'customer'

    def get_queryset(self):
        return Customer.objects.get(user=self.request.user)


class CustomerProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        customer_form = CustomerUpdateForm(instance=Customer.objects.get(user=request.user))
        category = Category.objects.filter(is_sub_category=False)
        context = {'user_form': user_form, 'customer_form': customer_form, 'category': category}
        return render(request, 'customer/update.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        customer_form = CustomerUpdateForm(request.POST, request.FILES,
                                           instance=Customer.objects.get(user=request.user))
        if user_form.is_valid() and customer_form.is_valid():
            customer_form.save()
            user_form.save()
            messages.success(self.request, _('Update was successful'), 'success')
            return redirect('customer:customer_profile')
        else:
            messages.error(self.request, _('Update failed'), 'danger')
            return redirect('customer:customer_profile_update')


class AddressCreateView(LoginRequiredMixin, generic.FormView):
    template_name = 'customer/address_create.html'
    form_class = AddressFormModel
    success_url = reverse_lazy('customer:customer_profile')

    def form_valid(self, form):
        messages.success(self.request, _('Add address was successful'), 'success')
        owner = Customer.objects.get(user=self.request.user)
        form.instance.owner = owner
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('Add address failed'), 'danger')
        return super().form_invalid(form)


class AddressUpdateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        address = Address.objects.get(id=kwargs['pk'])
        if address not in request.user.customer.address_set.all():
            messages.error(self.request, _('No Permission'), 'danger')
            return redirect('customer:customer_profile')
        address_form = AddressFormModel(instance=address)
        context = {'form': address_form}
        return render(request, 'customer/update_address.html', context)

    def post(self, request, *args, **kwargs):
        address = Address.objects.get(id=kwargs['pk'])
        form = AddressFormModel(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(self.request, _('Update was successful'), 'success')
            return redirect('customer:customer_profile')
        else:
            messages.error(self.request, _('Update failed'), 'danger')
            return redirect('customer:update_address')


class AddressDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        address = Address.objects.get(id=kwargs['pk'])
        if address not in request.user.customer.address_set.all():
            messages.error(self.request, _('No Permission'), 'danger')
            return redirect('customer:customer_profile')
        address.my_delete()
        messages.success(self.request, _(f'Address {address.state}-{address.city} Deleted!'), 'success')
        return redirect('customer:customer_profile')


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = forms.PasswordChangeForm(request.user)
        return render(request, 'customer/change_password.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(self.request, _('Password Changed'), 'success')
            return redirect('customer:customer_profile')
        else:
            messages.error(self.request, _('Password Change failed'), 'danger')
            return redirect('customer:change_password')


class FavoritesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer, user=request.user)
        favorites = customer.favorites.all()
        paginator = Paginator(favorites, 12)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        return render(request, 'customer/favorites.html', {'favorites': page_obj})
