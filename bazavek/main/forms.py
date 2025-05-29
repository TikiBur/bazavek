from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError
from .models import Booking
import re

class BookingForm(forms.ModelForm):
    date_range = forms.CharField(label="Даты проживания", required=True)

    class Meta:
        model = Booking
        fields = ['date_range', 'guests', 'name', 'email', 'phone']
        labels = {
            'date_range': 'Даты проживания',
            'guests': 'Количество гостей',
            'name': 'Ваше имя',
            'email': 'Электронная почта',
            'phone': 'Телефон',
        }
        error_messages = {
            'guests': {
                'min_value': "Минимальное количество гостей - 1",
                'max_value': "Максимальное количество гостей - 10",
            },
            'email': {
                'invalid': "Введите корректный адрес электронной почты",
            }
        }

    def clean_date_range(self):
        value = self.cleaned_data['date_range']
        try:
            start_str, end_str = value.split(' - ')
            start_date = datetime.strptime(start_str.strip(), "%d.%m.%Y").date()
            end_date = datetime.strptime(end_str.strip(), "%d.%m.%Y").date()
        except:
            raise ValidationError("Неверный формат диапазона дат. Пример: 01.01.2025 - 05.01.2025")

        nights = (end_date - start_date).days
        if nights < 1:
            raise ValidationError("Выберите минимум 1 ночь (разные даты).")

        self.cleaned_data['start_date'] = start_date
        self.cleaned_data['end_date'] = end_date
        self.cleaned_data['nights'] = nights
        return value

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.start_date = self.cleaned_data['start_date']
        instance.end_date = self.cleaned_data['end_date']
        if commit:
            instance.save()
        return instance