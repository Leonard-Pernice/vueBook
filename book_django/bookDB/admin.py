from django.contrib import admin

# Register your models here; created with the admin interface.

from .models import *

admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Paragraph)
admin.site.register(Character)
admin.site.register(Player)
admin.site.register(Relationship)
admin.site.register(Stat)
admin.site.register(Skill)
admin.site.register(Quest)
admin.site.register(Item)
# admin.site.register(Equipment)
# admin.site.register(Inventory)
# admin.site.register(Slot)
admin.site.register(Currency)
