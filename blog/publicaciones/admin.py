from django.contrib import admin
from .models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
	"""docstring fos PostAdmin"""
	list_display = ('id', 'title','imagen_html','text','created_date','published_date','author')
	fields = ['title','text','imagen','created_date','published_date','author']
	list_per_page=3
	search_fields = ['title','text']
	list_filter = ['author']

admin.site.register(Post,PostAdmin)