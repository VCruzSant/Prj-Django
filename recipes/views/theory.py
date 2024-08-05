from django.shortcuts import render


def theory(request, *args, **kwargs):
    return render(
        request, 'recipes/pages/theory.html'
    )
