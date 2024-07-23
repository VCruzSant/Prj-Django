import os

from django.http import Http404, JsonResponse
from django.shortcuts import get_list_or_404
from django.db.models import Q
from django.views.generic import ListView

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


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes'].object_list.values()

        return JsonResponse(
            list(recipes),
            safe=False
        )


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = get_list_or_404(
            qs.filter(
                category_id=self.kwargs.get('category_id'), is_published=True
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        title = f'{context.get("recipes")[0].category.name} - Category',

        context.update({'title': title})
        return context


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()

        if not search_term:
            raise Http404

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            ),
            is_published=True
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()
        context = super().get_context_data(*args, **kwargs)

        context.update(
            {
                'page_title': f'Search for "{search_term}"',
                'additional_url_query': f'&q={search_term}'
            }
        )
        return context
