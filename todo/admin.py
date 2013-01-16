from django.contrib import admin
from todo.models import List, Item

class ListAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,		{'fields': ['title']})
	]

class ItemAdmin(admin.ModelAdmin):
	list_display = ('title', 'created_date', 'completed', 'priority', 'todo_list')
	list_filter = ['created_date', 'completed']
	search_fields = ['question']
	date_hierarchy = 'created_date'

admin.site.register(List, ListAdmin)
admin.site.register(Item, ItemAdmin)
