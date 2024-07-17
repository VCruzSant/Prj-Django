from django.urls import path

from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path(
        'login/create/', views.login_create,  # type: ignore
        name='login_create'
    ),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path(
        'dashboard/recipe/register/',
        views.register_recipe_view,
        name='dashboard_recipe_register'
    ),
    path(
        'dashboard/recipe/register/create/',
        views.register_recipe_create,
        name='register_recipe_create'
    ),
    path(
        'dashboard/recipe/delete/',
        views.dashboard_recipe_delete,
        name='dashboard_recipe_delete'
    ),
    path(
        'dashboard/recipe/<int:id>/edit/',
        views.DashboardRecipe.as_view(),
        name='dashboard_recipe_edit'
    ),

]
