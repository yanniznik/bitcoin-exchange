from django.contrib import admin

# Register your models here.
from exchange.models import *

class showId(admin.ModelAdmin):
    list_display = ('owner' , 'amount', "address")

class displayList(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
admin.site.register(Profile)

admin.site.register(Transactions)
admin.site.register(Wallets, showId)
admin.site.register(Contacts)
