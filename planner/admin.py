from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Country)
admin.site.register(Trip)
admin.site.register(Destination)
admin.site.register(TripDetail)
admin.site.register(TripDetailDestination)
