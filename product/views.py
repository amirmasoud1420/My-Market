from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.utils.translation import gettext_lazy as _
from .models import *
from django.contrib import messages
from .forms import *


# Create your views here.


def test(request):
    return render(request, 'base/base.html')


class MenuItemCardView(generic.DetailView):
    template_name = 'menu_item/menu_item_card.html'
    model = MenuItemVariant
    context_object_name = 'menu_item'


class MenuItemCategoryView(generic.DetailView):
    template_name = 'menu_item/menu_item_list.html'
    model = Category
    context_object_name = 'category'


class MenuItemVariantDetailView(View):

    def get(self, request, *args, **kwargs):
        menu_item_variant = get_object_or_404(MenuItemVariant, id=kwargs['pk'])
        is_like = False
        if menu_item_variant.likes.filter(id=request.user.id).exists():
            is_like = True
        is_dislike = False
        if menu_item_variant.un_likes.filter(id=request.user.id).exists():
            is_dislike = True
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
        }
        return render(request, 'menu_item/menu_item_detail.html', context)

    def post(self, request, *args, **kwargs):
        menu_item_variant = get_object_or_404(MenuItemVariant, id=request.POST.get('select'))
        is_like = False
        if menu_item_variant.likes.filter(id=request.user.id).exists():
            is_like = True
        is_dislike = False
        if menu_item_variant.un_likes.filter(id=request.user.id).exists():
            is_dislike = True
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
