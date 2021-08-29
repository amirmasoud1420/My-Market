from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.utils.translation import gettext_lazy as _
from .models import *
from django.contrib import messages
from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator
from .filters import *
from django.db.models import Avg, Min, Max


# Create your views here.


class HomeView(View):
    def get(self, request, *args, **kwargs):
        search_form = SearchForm()
        category = Category.objects.filter(is_sub_category=False)
        gallery = Gallery.objects.all()
        create = MenuItem.objects.all().order_by('-create_time_stamp')[:6]
        context = {
            'create': create,
            'gallery': gallery,
            'category': category,
            'search_form': search_form,
        }
        return render(request, 'home/home.html', context)


class MenuItemCardView(generic.DetailView):
    template_name = 'menu_item/menu_item_card.html'
    model = MenuItemVariant
    context_object_name = 'menu_item'


class MenuItemCategoryView(generic.DetailView):
    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, id=kwargs['pk'])
        menu_items = category.menuitem_set.all()

        menu_item_filter = MenuItemFilter(request.GET, queryset=menu_items)
        menu_items = menu_item_filter.qs

        menu_item_variants = []
        for i in menu_items:
            data = i.menuitemvariant_set.all().aggregate(price=Min('price'))
            if data['price']:
                menu_item_variants.append(i.menuitemvariant_set.filter(price=int(data['price'])).last())

        id_list = []
        for i in menu_item_variants:
            id_list.append(i.id)
        menu_item_variants_q = MenuItemVariant.objects.filter(id__in=id_list)
        min_price = 0
        min = menu_item_variants_q.all().aggregate(price=Min('price'))
        if min['price']:
            min_price = int(min['price'])
        max_price = 1000000
        max = menu_item_variants_q.all().aggregate(price=Max('price'))
        if max['price']:
            max_price = int(max['price'])

        menu_item_variant_filter = MenuItemVariantFilter(request.GET, queryset=menu_item_variants_q)
        menu_items = menu_item_variant_filter.qs

        paginator = Paginator(menu_items, 12)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        category = Category.objects.filter(is_sub_category=False)
        context = {
            'category': category,
            'menu_items': page_obj,
            'filter': menu_item_variant_filter,
            'menu_item_filter': menu_item_filter,
            'min_price': min_price,
            'max_price': max_price,
        }
        return render(request, 'menu_item/menu_item_list.html', context)


# class MenuItemCategoryView(generic.DetailView):
#     template_name = 'menu_item/menu_item_list.html'
#     model = Category
#     context_object_name = 'category'
#
#     def get(self, request, *args, **kwargs):
#         category = get_object_or_404(Category, id=kwargs['pk'])
#         menu_item = MenuItem.objects.filter(category=category)
#         paginator = Paginator(menu_item, 2)
#         page_num = request.GET['page']
#         page_obj = paginator.get_page(page_num)
#         return super().get(request, *args, **kwargs)


class MenuItemVariantDetailView(View):

    def get(self, request, *args, **kwargs):
        menu_item_variant = get_object_or_404(MenuItemVariant, id=kwargs['pk'])

        is_like = False
        if request.user.is_authenticated:
            if menu_item_variant.likes.filter(id=request.user.id).exists():
                is_like = True

        is_dislike = False
        if request.user.is_authenticated:
            if menu_item_variant.un_likes.filter(id=request.user.id).exists():
                is_dislike = True

        is_favorites = False
        if request.user.is_authenticated:
            if menu_item_variant.menu_item.favorites_customers.filter(user=request.user).exists():
                is_favorites = True

        variants = menu_item_variant.menu_item.menuitemvariant_set.all()
        similar_product = menu_item_variant.menu_item.tags.similar_objects()[:5]

        comment_form = CommentForm()
        comments = Comment.objects.filter(menu_item=menu_item_variant.menu_item, is_reply=False)
        reply_from = ReplyForm()

        category = Category.objects.filter(is_sub_category=False)
        context = {
            'category': category,
            'menu_item_variant': menu_item_variant,
            'variants': variants,
            'similar_product': similar_product,
            'is_like': is_like,
            'is_dislike': is_dislike,
            'comment_form': comment_form,
            'comments': comments,
            'reply_from': reply_from,
            'is_favorites': is_favorites,
        }
        return render(request, 'menu_item/menu_item_detail.html', context)

    def post(self, request, *args, **kwargs):
        menu_item_variant = get_object_or_404(MenuItemVariant, id=request.POST.get('select'))

        is_like = False
        if request.user.is_authenticated:
            if menu_item_variant.likes.filter(id=request.user.id).exists():
                is_like = True

        is_dislike = False
        if request.user.is_authenticated:
            if menu_item_variant.un_likes.filter(id=request.user.id).exists():
                is_dislike = True

        is_favorites = False
        if request.user.is_authenticated:
            if menu_item_variant.menu_item.favorites_customers.filter(user=request.user).exists():
                is_favorites = True

        variants = menu_item_variant.menu_item.menuitemvariant_set.all()
        similar_product = menu_item_variant.menu_item.tags.similar_objects()[:5]

        comment_form = CommentForm()
        comments = Comment.objects.filter(menu_item=menu_item_variant.menu_item, is_reply=False)
        reply_from = ReplyForm()

        context = {
            'menu_item_variant': menu_item_variant,
            'variants': variants,
            'similar_product': similar_product,
            'is_like': is_like,
            'is_dislike': is_dislike,
            'comment_form': comment_form,
            'comments': comments,
            'reply_from': reply_from,
            'is_favorites': is_favorites,
        }
        return redirect('menu_item_detail', pk=request.POST.get('select'))


class MenuItemVariantLikeView(View):
    def get(self, request, *args, **kwargs):
        is_like = False
        menu_item_variant = get_object_or_404(MenuItemVariant, id=kwargs['pk'])
        if menu_item_variant.likes.filter(id=request.user.id).exists():
            menu_item_variant.likes.remove(request.user)
            is_like = False
            messages.success(self.request, _('Like Removed!'), 'warning')
        else:
            menu_item_variant.likes.add(request.user)
            is_like = True
            messages.success(self.request, _('Thank you for like!'), 'success')
        return redirect('menu_item_detail', pk=menu_item_variant.id)


class MenuItemVariantUnLikeView(View):
    def get(self, request, *args, **kwargs):
        is_dislike = False
        menu_item_variant = get_object_or_404(MenuItemVariant, id=kwargs['pk'])
        if menu_item_variant.un_likes.filter(id=request.user.id).exists():
            menu_item_variant.un_likes.remove(request.user)
            is_dislike = False
            messages.success(self.request, _('dislike Removed!'), 'info')
        else:
            menu_item_variant.un_likes.add(request.user)
            is_dislike = True
            messages.success(self.request, _('you disliked this product'), 'danger')
        return redirect('menu_item_detail', pk=menu_item_variant.id)


class MenuItemCommentView(View):
    def post(self, request, *args, **kwargs):
        comment_from = CommentForm(request.POST)
        if comment_from.is_valid():
            data = comment_from.cleaned_data
            if not data['rate']:
                data['rate'] = 1
            menu_item_variant = get_object_or_404(MenuItemVariant, id=kwargs['pk'])
            Comment.objects.create(
                comment=data['comment'],
                rate=data['rate'],
                user=request.user,
                menu_item=menu_item_variant.menu_item,
            )
            messages.success(self.request, _('Your comment has been submitted'), 'success')
        else:
            messages.error(self.request, _('The submission was failed!'), 'danger')
        return redirect('menu_item_detail', pk=kwargs['pk'])


class MenuItemCommentReplyView(View):
    def post(self, request, *args, **kwargs):
        reply_from = ReplyForm(request.POST)
        if reply_from.is_valid():
            data = reply_from.cleaned_data
            menu_item_variant = get_object_or_404(MenuItemVariant, id=kwargs['pk'])
            Comment.objects.create(
                comment=data['comment'],
                user=request.user,
                menu_item=menu_item_variant.menu_item,
                parent=Comment.objects.get(id=kwargs['comment_id']),
                is_reply=True,
            )
            messages.success(self.request, _('Your reply has been submitted'), 'success')
        else:
            messages.error(self.request, _('The submission was failed!'), 'danger')
        return redirect('menu_item_detail', pk=kwargs['pk'])


class CommentLikeView(View):
    def get(self, request, *args, **kwargs):
        url = request.META.get('HTTP_REFERER')
        is_like = False
        comment = get_object_or_404(Comment, id=kwargs['pk'])
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
            is_like = False
            messages.success(self.request, _('Like Removed!'), 'warning')
        else:
            comment.likes.add(request.user)
            is_like = True
            messages.success(self.request, _('Thank you for like!'), 'success')
        return redirect(url)


class CommentUnLikeView(View):
    def get(self, request, *args, **kwargs):
        url = request.META.get('HTTP_REFERER')
        is_dislike = False
        comment = get_object_or_404(Comment, id=kwargs['pk'])
        if comment.un_likes.filter(id=request.user.id).exists():
            comment.un_likes.remove(request.user)
            is_dislike = False
            messages.success(self.request, _('dislike Removed!'), 'info')
        else:
            comment.un_likes.add(request.user)
            is_dislike = True
            messages.success(self.request, _('you disliked this comment'), 'danger')
        return redirect(url)


class ProductSearchView(View):
    def get(self, request, *args, **kwargs):

        return redirect('home')

    def post(self, request, *args, **kwargs):
        url = request.META.get('HTTP_REFERER')
        menu_items = MenuItem.objects.all()
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data is not None:
                if (data['key']).isdigit():

                    menu_items = menu_items.filter(
                        Q(menuitemvariant__discount__price__exact=int(data['key'])) |
                        Q(menuitemvariant__discount__percent__exact=int(data['key'])) |
                        Q(menuitemvariant__price__exact=int(data['key']))
                    )
                else:
                    menu_items = menu_items.filter(name__icontains=data['key'])
            return render(request, 'menu_item/search_list.html', {'menu_items': menu_items})
        else:
            messages.error(self.request, _('Search Failed!'), 'danger')
            return redirect(url)


class FavoritesAddView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        url = request.META.get('HTTP_REFERER')
        menu_item = get_object_or_404(MenuItem, id=kwargs['pk'])
        c = Customer.objects.get(user=request.user)
        is_favorites = False
        if menu_item.favorites_customers.filter(user=request.user).exists():
            menu_item.favorites_customers.remove(c)
            is_favorites = False
            messages.success(self.request, _("Remove from your favorites"), 'warning')
        else:
            menu_item.favorites_customers.add(c)
            is_favorites = True
            messages.success(self.request, _("Add into your favorites"), 'success')
        return redirect(url)
