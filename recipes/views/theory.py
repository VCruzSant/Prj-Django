from django.shortcuts import render
from recipes.models import Recipe


def theory(request, *args, **kwargs):
    recipes = Recipe.objects.get(id=20)
    # recipes = Recipe.objects.all()
    # recipes = recipes \
    #     .order_by('-id') \
    #     .first()

    context = {
        'recipes': recipes
    }

    return render(
        request, 'recipes/pages/theory.html', context=context
    )
