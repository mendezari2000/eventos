from django.contrib import admin
from .models import Event, Venue, Category


class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "date")
    search_fields = ("title", "date")
    list_filter = ("date",)
    
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'capacity')
    search_fields = ('name', 'city')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)

admin.site.register(Event, EventAdmin)
