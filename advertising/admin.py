from django.contrib import admin

from advertising.models import Advertising, Category

admin.site.register(Category)
admin.site.register(Advertising)