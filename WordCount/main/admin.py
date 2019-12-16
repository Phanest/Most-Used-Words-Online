from django.contrib import admin
from main.models import *
# Register your models here.

class NameAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender']
    ordering = ['name']
    actions = ['addNames']

    def addNames(self, modeladmin, request, queryset):
        for query in queryset:
            query.start('http://www.behindthename.com/names/usage/macedonian')

    addNames.short_description = "Add new names"


class WordAdmin(admin.ModelAdmin):
    list_display = ['word', 'gender']
    ordering = ['word']
    actions = ['addWords']

    def addWords(self, modeladmin, request, queryset):
        for query in queryset:
            query.start('http://makedonski.info')

admin.site.register(Word)
admin.site.register(EnglishWord)
admin.site.register(Type)
admin.site.register(Name, NameAdmin)
admin.site.register(Site)
admin.site.register(WordSoup)
admin.site.register(NameSoup)