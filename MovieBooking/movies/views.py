from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import random

from .models import Movie, Show, Seat, Booking


def home(request):
    query = request.GET.get('q')

    if query:
        movies = Movie.objects.filter(
            title__icontains=query
        )
    else:
        movies = Movie.objects.all()

    return render(
        request,
        'home.html',
        {
            'movies': movies
        }
    )


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    shows = Show.objects.filter(movie=movie)

    return render(
        request,
        'movie_detail.html',
        {
            'movie': movie,
            'shows': shows
        }
    )


def select_seat(request, show_id):

    show = get_object_or_404(Show, id=show_id)
    

    seats = Seat.objects.filter(
        show=show
    ).order_by('seat_number')

    return render(
        request,
        'select_seat.html',
        {
            'show': show,
            'seats': seats
        }
    )


@login_required
def book_ticket(request, seat_id):
    seat = Seat.objects.get(id=seat_id)

    if not seat.is_booked:

        Booking.objects.create(
            user=request.user,
            show=seat.show,
            seat=seat
        )

        seat.is_booked = True
        seat.save()

    return render(
        request,
        'ticket.html',
        {
            'seat': seat
            
        }
    )
@login_required
def profile(request):

    total_bookings = Booking.objects.filter(
        user=request.user
    ).count()

    return render(
        request,
        'profile.html',
        {
            'total_bookings': total_bookings
        }
    )


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )

@login_required
def payment_page(request, seat_id):

    seat = Seat.objects.get(id=seat_id)

    if request.method == "POST":

        booking = Booking.objects.create(
            user=request.user,
            show=seat.show,
            seat=seat,
            payment_status="Paid"
        )
        booking.booking_id = f"MOV{random.randint(10000,99999)}"
        booking.save()

        
        seat.is_booked = True
        seat.save()

        return render(
            request,
            'ticket.html',
            {
                'seat': seat,
                'booking': booking
            }
        )

    return render(
        request,
        'payment.html',
        {
            'seat': seat
        }
    )


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user
    )

    return render(
        request,
        'my_bookings.html',
        {
            'bookings': bookings
        }
    )

@login_required
def cancel_booking(request, booking_id):

    booking = Booking.objects.get(
        id=booking_id,
        user=request.user
    )

    booking.seat.is_booked = False
    booking.seat.save()

    booking.delete()

    return redirect('my_bookings')


def logout_user(request):
    logout(request)
    return redirect('/')