from django.contrib import admin
from .models import Category, Recipe
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'created_at', 'is_published', 'category', 'author'
    )
    list_display_links = 'id', 'title',
    search_fields = 'id', 'title', 'description', 'author', 'preparation_step'
    list_filter = (
        'category', 'author', 'is_published', 'preparation_step_is_html'
    )
    list_per_page = 10
    list_editable = 'is_published',
    prepopulated_fields = {
        "slug": ('title',)
    }
