from django.views.generic import ListView
from django.shortcuts import get_list_or_404
import os

from ..models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, context.get('recipes'), PER_PAGE
        )
        context.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )
        return context


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        qs = get_list_or_404(
            qs.filter(
                category_id=self.kwargs.get('category_id'), is_published=True
            )
        )
        return qs
