from django.contrib import admin
from .models import *

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['author_id', 'name']
    search_fields= ['author_id', 'name']

class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'publication']
    search_fields= ['publication', 'name']

admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Book, BookAdmin)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(IssuedBook)
admin.site.register(Fine)