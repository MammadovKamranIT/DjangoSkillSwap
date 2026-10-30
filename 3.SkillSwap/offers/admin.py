from django.contrib import admin

from offers.models import Offer,  Category, Tag
from django.contrib.auth import get_user_model

User = get_user_model()

# Unregister if already registered somewhere else to avoid conflicts
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    autocomplete_fields = ['tags']
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at')


