from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from datetime import datetime
from datetime import timedelta
from .forms import BookingForm
from .models import Booking
from .models import Testimonial
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
import os
import json

def index(request):
    return render(request, 'main/index.html')

def get_houses():
    return [
        {
            'id': '3house',
            'image': 'main/img/3house.png',
            'title': 'Домик на берегу моря',
            'price': 1200,
            'capacity': 'До 3 чел',
            'description': 'Уютный домик с видом на море и выходом на пляж. Отлично подходит для семейного отдыха.',
            'features': [
                'Прямой выход к пляжу',
                'Терраса с видом на море',
                'Полностью оборудованная кухня',
            ]
        },
        {
            'id': '4house',
            'image': 'main/img/4house.png',
            'title': 'Домик на берегу моря',
            'price': 1500,
            'capacity': 'До 4 чел',
            'description': 'Уютный домик с видом на море и выходом на пляж. Отлично подходит для семейного отдыха.',
            'features': [
                'Собственный гамак на террасе',
                'Камин в гостиной',
                'Детская площадка рядом',
            ]
        },
        {
            'id': '5house',
            'image': 'main/img/5house.png',
            'title': 'Домик возле моря',
            'price': 2200,
            'capacity': 'До 5 чел',
            'description': 'Уютный домик с видом на море и выходом на пляж. Отлично подходит для семейного отдыха.',
            'features': [
                'Просторная терраса с мангалом',
                '2 спальни и гостиная',
                'Парковка рядом',
            ]
        },
        {
            'id': '8house',
            'image': 'main/img/8house.png',
            'title': 'Домик возле моря',
            'price': 3200,
            'capacity': 'До 8 чел',
            'description': 'Уютный домик с видом на море и выходом на пляж. Отлично подходит для семейного отдыха.',
            'features': [
                '3 спальни и 2 ванные',
                'Большая терраса с зоной отдыха',
                'До моря 150 метров',
            ]
        },
    ]

def rentals_view(request):
    houses = get_houses()
    context = {
        'houses': houses
    }
    return render(request, 'main/rentals/rentals.html', context)

def book_house(request):
    houses = get_houses()
    house_id = request.POST.get('house_id') if request.method == 'POST' else request.GET.get('house_id')
    selected_house = next((h for h in houses if h['id'] == house_id), None)
    if not selected_house:
        raise Http404("Домик не найден")

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.house_id = selected_house['id']
            booking.house_title = selected_house['title']
            booking.house_price = selected_house['price']
            booking.save()

            # ✅ Сохраняем id
            request.session['booking_id'] = booking.id

            # ✅ ОТПРАВКА ПИСЬМА
            try:
                html_content = render_to_string(
                    'main/emails/booking_confirmation.html',
                    {
                        'booking': booking,
                        'domain': 'https://yourdomain.ru',  # замени на свой домен
                        'current_year': timezone.now().year
                    }
                )
                email = EmailMultiAlternatives(
                    subject='Ваше бронирование подтверждено!',
                    body='Ваше бронирование подтверждено.',
                    from_email='your_email@gmail.com',
                    to=[booking.email]
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
                print("✅ Email отправлен")
            except Exception as e:
                print("❌ Ошибка при отправке письма:", e)

            return redirect('main:booking_success')
    else:
        form = BookingForm()

    booked_dates = get_booked_dates()

    return render(request, 'main/booking/book_house.html', {
        'form': form,
        'house': selected_house,
        'booked_dates': booked_dates,
        'errors': form.errors.get('__all__', []),
    })

def get_booked_dates():
    bookings = Booking.objects.all()
    disabled = set()

    for booking in bookings:
        current = booking.start_date
        while current < booking.end_date:
            disabled.add(current.strftime('%Y-%m-%d'))
            current += timedelta(days=1)

    return sorted(disabled)

def booking_success(request):
    booking_id = request.session.get('booking_id')
    if not booking_id:
        return redirect('main:index')
    
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return redirect('main:index')
    
    context = {
        'booking': booking
    }
    return render(request, 'main/booking/success.html', context)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'testimonials_data.json')

# Загрузка отзывов из файла
def load_testimonials():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Сохранение отзывов в файл
def save_testimonials(testimonials):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(testimonials, f, ensure_ascii=False, indent=2)

# Получение всех отзывов (GET)
def testimonials_list(request):
    testimonials = load_testimonials()
    # Сортировка по времени (новые сверху)
    testimonials_sorted = sorted(testimonials, key=lambda x: x['created_at'], reverse=True)
    return JsonResponse(testimonials_sorted, safe=False)

# Создание отзыва (POST)
@csrf_exempt
def testimonial_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        name = data.get('name')
        rating = data.get('rating')
        text = data.get('text')

        if not all([name, rating, text]):
            return JsonResponse({'error': 'Missing fields'}, status=400)

        new_testimonial = {
            'name': name,
            'rating': int(rating),
            'text': text,
            'created_at': datetime.now().isoformat()
        }

        testimonials = load_testimonials()
        testimonials.append(new_testimonial)
        save_testimonials(testimonials)

        return JsonResponse(new_testimonial)
    
    return JsonResponse({'error': 'Invalid method'}, status=405)

def booking_success_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Отправка email
    subject = 'Ваше бронирование подтверждено!'
    from_email = 'your_email@gmail.com'
    to_email = [booking.email]
    
    html_content = render_to_string('emails/booking_confirmation.html', {'booking': booking})
    email = EmailMultiAlternatives(subject, '', from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()

    return render(request, 'main/booking_success.html', {'booking': booking})

def support(request):
    return render(request, 'main/support.html')