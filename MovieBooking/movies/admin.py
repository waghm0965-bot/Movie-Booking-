from django.contrib import admin
from .models import Movie, Show, Seat, Booking

admin.site.register(Movie)
admin.site.register(Show)
admin.site.register(Seat)
admin.site.register(Booking)