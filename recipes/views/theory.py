from django.shortcuts import render
from recipes.models import Recipe
# from django.db.models import Q, F


def theory(request, *args, **kwargs):
    # recipes = Recipe.objects.filter(
    #     Q(title__icontains='recipe',
    #       id__gt=5,
    #       is_published=True,) |
    #     Q(
    #         id__gt=100
    #     )
    # )[:10]

    # recipes = Recipe.objects.all()
    # recipes = recipes \
    #     .order_by('-id') \
    #     .first()

    # recipes = Recipe.objects.filter(
    #     id=F('author__id'),
    # )[:10]

    recipes = Recipe.objects \
        .values('id', 'title', 'author__username')[10:20]

    context = {
        'recipes': recipes
    }

    return render(
        request, 'recipes/pages/theory.html', context=context
    )
