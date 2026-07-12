from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path(
        'movie/<int:movie_id>/',
        views.movie_detail,
        name='movie_detail'
    ),

    path(
        'show/<int:show_id>/',
        views.select_seat,
        name='select_seat'
    ),

    path(
        'book/<int:seat_id>/',
        views.book_ticket,
        name='book_ticket'
    ),

    path(
        'my-bookings/',
        views.my_bookings,
        name='my_bookings'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        views.logout_user,
        name='logout'
    ),
    path(
    'payment/<int:seat_id>/',
    views.payment_page,
    name='payment'
),
path(
    'cancel/<int:booking_id>/',
    views.cancel_booking,
    name='cancel_booking'
),
path(
    'profile/',
    views.profile,
    name='profile'
),
]