from django.contrib import admin
from .models import Thesis
# Register your models here.
@admin.register(Thesis)
class Thesis(admin.ModelAdmin):
    list_display = ['title', 'get_authors']

    def get_authors(self, obj):
        return ", ".join([t.userId for t in obj.authors.all()]) 