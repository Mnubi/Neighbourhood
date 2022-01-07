from django.contrib import admin
from django.contrib import admin

from neighapp.models import Neighbourhood, Profile, Business, Contact, Post

# Register your models here.
admin.site.register(Neighbourhood)
admin.site.register(Profile)
admin.site.register(Business)
admin.site.register(Contact)
admin.site.register(Post)