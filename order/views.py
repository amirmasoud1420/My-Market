from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View, generic

from customer.forms import AddressFormModel
from .models import *
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


# Create your views here.


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(customer__user=request.user)
        if order.exists():
            empty = True
            order_during = order.filter(status='d')

            if order_during.exists():
                order_during = order.get(status='d')
                order_during = order_during.ordermenuitem_set.order_by('id')
                empty = False
            context = {
                'order_during': order_during,

                'empty': empty,
            }
        else:
            empty = True
            context = {
                'empty': empty,
            }
        category = Category.objects.filter(is_sub_category=False)
        context['category'] = category
        return render(request, 'order/order.html', context)


class CanceledOrderDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(customer__user=request.user)
        if order.exists():
            empty = True
            order_canceled = order.filter(status='c')
            if order_canceled.exists():
                order_canceled = order.filter(status='c')

                empty = False
            context = {

                'order_canceled': order_canceled,

                'empty': empty,
            }
        else:
            empty = True
            context = {
                'empty': empty,
            }
        category = Category.objects.filter(is_sub_category=False)
        context['category'] = category
        return render(request, 'order/canceled_detail.html', context)


class PaidOrderDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(customer__user=request.user)
        if order.exists():
            empty = True

            order_paid = order.filter(status='p')
            if order_paid.exists():
                order_paid = order.filter(status='p')

                empty = False
            context = {

                'order_paid': order_paid,
                'empty': empty,
            }
        else:
            empty = True
            context = {
                'empty': empty,
            }
        category = Category.objects.filter(is_sub_category=False)
        context['category'] = category
        return render(request, 'order/paid_detail.html', context)


class OrderAddView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.customer.order_set.filter(status='d').exists():
            order = Order.objects.filter(status='d')
            order = order.get(customer__user=request.user)
        else:
            order = Order.objects.create(
                customer=request.user.customer,
            )

        menu_item_variant = get_object_or_404(MenuItemVariant, id=kwargs['pk'])
        # if menu_item_variant in order.menu_item_variants.all():
        if order.ordermenuitem_set.filter(menu_item_variant=menu_item_variant):
            order.ordermenuitem_set.filter(menu_item_variant=menu_item_variant)
            order_item = OrderMenuItem.objects.get(order=order, menu_item_variant=menu_item_variant)
            order_item.quantity += 1
            order_item.save()
            messages.success(self.request, _('The product is already in your cart! A number was added to it.'),
                             'success')
        else:
            OrderMenuItem.objects.create(
                order=order,
                menu_item_variant=menu_item_variant,
                quantity=1,
            )
            messages.success(self.request, _('Added to cart'), 'success')
        menu_item_variant.count -= 1
        menu_item_variant.save()
        return redirect('order:order_detail')


class OffCodeAddView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        code = request.POST['off_code']
        order = get_object_or_404(Order, id=request.POST['order_id'])
        if OffCode.objects.filter(code=code).exists():
            for i in OffCode.objects.filter(code=code):
                if not i.is_expired():
                    order.off_code = i
                    order.save()
                    messages.success(self.request, _('The off code is applied'), 'success')
                    break
            else:
                messages.error(self.request, _('The off code is expired!'), 'danger')
        else:
            messages.error(self.request, _('Off Code Invalid!'), 'danger')
        return redirect('order:create_order', pk=request.POST['order_id'])


class AddQuantityView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(status='d')
        order = order.get(customer__user=request.user)
        order_menu_item = OrderMenuItem.objects.get(id=kwargs['pk'])
        if order_menu_item.menu_item_variant.count > 0:
            order_menu_item.quantity += 1
            order_menu_item.save()
            order_menu_item.menu_item_variant.count -= 1
            order_menu_item.menu_item_variant.save()

        return redirect('order:order_detail')


class RemoveQuantityView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(status='d')
        order = order.get(customer__user=request.user)
        order_menu_item = OrderMenuItem.objects.get(id=kwargs['pk'])
        if order_menu_item.quantity > 0:
            order_menu_item.quantity -= 1
            order_menu_item.save()
            order_menu_item.menu_item_variant.count += 1
            order_menu_item.menu_item_variant.save()
        if order_menu_item.quantity == 0:
            order_menu_item.my_delete()
        if not order.ordermenuitem_set.filter().exists():
            order.my_delete()

        return redirect('order:order_detail')


class RemoveOrderItemView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(status='d')
        order = order.get(customer__user=request.user)
        order_menu_item = OrderMenuItem.objects.get(id=kwargs['pk'])
        order_menu_item.menu_item_variant.count += order_menu_item.quantity
        order_menu_item.menu_item_variant.save()
        order_menu_item.my_delete()
        if not order.ordermenuitem_set.filter().exists():
            order.my_delete()
        return redirect('order:order_detail')


class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['pk'])
        addresses = Address.objects.filter(owner__user=request.user)
        context = {
            'order': order,
            'addresses': addresses,
        }
        return render(request, 'order/create_order.html', context)


class RemoveOffCodeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['pk'])
        order.off_code = None
        order.save()
        messages.success(self.request, _('The off code is deleted!'), 'success')
        return redirect('order:create_order', pk=kwargs['pk'])


class SelectAddress(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        addresses = Address.objects.filter(owner__user=request.user)
        is_empty = True
        if addresses.exists():
            is_empty = False
            context = {
                'addresses': addresses,
                'is_empty': is_empty,
            }
        else:
            context = {
                'is_empty': is_empty,
            }
        return render(request, 'order/select_address.html', context)

    def get(self, request, *args, **kwargs):
        addresses = Address.objects.filter(owner__user=request.user)
        is_empty = True
        if addresses.exists():
            is_empty = False
            context = {
                'addresses': addresses,
                'is_empty': is_empty,
            }
        else:
            context = {
                'is_empty': is_empty,
            }
        category = Category.objects.filter(is_sub_category=False)
        context['category'] = category
        return render(request, 'order/select_address.html', context)


class AddressCreateView(LoginRequiredMixin, generic.FormView):
    template_name = 'customer/address_create.html'
    form_class = AddressFormModel
    success_url = reverse_lazy('order:select_address')

    def form_valid(self, form):
        messages.success(self.request, _('Add address was successful'), 'success')
        owner = Customer.objects.get(user=self.request.user)
        form.instance.owner = owner
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('Add address failed'), 'danger')
        return super().form_invalid(form)


class PaymentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(status='d', customer__user=request.user)
        for i in order:
            i.paid_price = i.final_price()
            i.status = 'p'
            i.save()
            for j in i.ordermenuitem_set.all():
                j.menu_item_variant.menu_item.sell += j.quantity
                j.menu_item_variant.menu_item.save()
        return render(request, 'order/payment.html')


class CancelOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(status='d', customer__user=request.user)
        for i in order:
            i.paid_price = i.final_price()
            i.status = 'c'
            i.save()
        return redirect('order:canceled_order_detail')
