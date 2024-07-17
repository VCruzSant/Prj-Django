from django.views.generic import DetailView
from ..models import Recipe


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {'is_detail_page': True}
        )

        return context

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs = qs.filter(is_published=True)

        return qs
