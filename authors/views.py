from django.shortcuts import render

# Create your views here.


def regsiter_view(request):
    return render(request, 'authors/pages/register_view.html')
