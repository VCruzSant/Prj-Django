from django.shortcuts import render
from recipes.models import Recipe
# from django.db.models.aggregates import Count, Sum, Min, Max
# from django.db.models import Q, F
from django.db.models import Value, F
from django.db.models.functions import Concat


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

    # recipes = Recipe.objects \
    #     .values('id', 'title', 'author__username')[10:20]

    # recipes = Recipe.objects \
    #     .only('id', 'title')[10:20]

    # recipes = Recipe.objects \
    #     .defer('is_published')[10:20]

    # recipes = Recipe.objects \
    #     .values('id', 'title')[10:20]

    # number_od = recipes.aggregate(number=Count('id'))

    recipes = Recipe.objects.all().annotate(
        author_full_name=Concat(
            F('author__first_name'), F('author__last_name'),
            Value(' ('),
            F('author__username'),
            Value(')')
        )
    )[:10]

    context = {
        'recipes': recipes,
        # 'number_od': number_od['number']
    }

    return render(
        request, 'recipes/pages/theory.html', context=context
    )
