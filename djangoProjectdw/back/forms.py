from datetime import date
from django import forms
from .models import Even
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


def disable_fields(form):
    current_date = date.today()

    if current_date < date(2023, 1, 1) or current_date > date(2023, 12, 31):
        # Если текущая дата не входит в указанный период, блокируем все поля
        for field in form.fields.values():
            field.widget.attrs['disabled'] = 'disabled'
    elif current_date <= date(2023, 3, 31):
        # Если текущая дата находится в 1 квартале, блокируем поля cvartal2, cvartal3 и cvartal4
        form.fields['cvartal2'].widget.attrs['disabled'] = 'disabled'
        form.fields['cvartal3'].widget.attrs['disabled'] = 'disabled'
        form.fields['cvartal4'].widget.attrs['disabled'] = 'disabled'
    elif current_date <= date(2023, 6, 30):
        # Если текущая дата находится во 2 квартале, блокируем поля cvartal3 и cvartal4
        form.fields['cvartal3'].widget.attrs['disabled'] = 'disabled'
        form.fields['cvartal4'].widget.attrs['disabled'] = 'disabled'
        form.fields['cvartal1'].widget.attrs['disabled'] = 'disabled'
    elif current_date <= date(2023, 9, 30):
        # Если текущая дата находится в 3 квартале, блокируем только поле cvartal4
        form.fields['cvartal4'].widget.attrs['disabled'] = 'disabled'
        form.fields['cvartal2'].widget.attrs['disabled'] = 'disabled'
        form.fields['cvartal1'].widget.attrs['disabled'] = 'disabled'
    elif current_date <= date(2023, 12, 30):
        # Если текущая дата находится в 4 квартале, блокируем только поле cvartal4
        form.fields['cvartal3'].widget.attrs['disabled'] = 'disabled'
        form.fields['cvartal2'].widget.attrs['disabled'] = 'disabled'
        form.fields['cvartal1'].widget.attrs['disabled'] = 'disabled'


class EvenForm(forms.ModelForm):
    station = forms.CharField(label='Станция', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    gpa_number = forms.CharField(label='Номер ГПА', widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        disable_fields(self)

        current_date = date.today()

        if current_date < date(2023, 1, 1) or current_date > date(2023, 12, 31):
            # Если текущая дата не входит в указанный период, блокируем все поля
            for field in self.fields.values():
                field.widget.attrs['disabled'] = 'disabled'
        else:
            # Разблокируем все поля
            for field in self.fields.values():
                field.widget.attrs['disabled'] = False

            if current_date <= date(2023, 3, 31):
                # Если текущая дата находится в 1 квартале, блокируем поля cvartal2, cvartal3 и cvartal4
                self.fields['cvartal2'].widget.attrs['disabled'] = 'disabled'
                self.fields['cvartal3'].widget.attrs['disabled'] = 'disabled'
                self.fields['cvartal4'].widget.attrs['disabled'] = 'disabled'
            elif current_date <= date(2023, 6, 30):
                # Если текущая дата находится во 2 квартале, блокируем поля cvartal3 и cvartal4
                self.fields['cvartal3'].widget.attrs['disabled'] = 'disabled'
                self.fields['cvartal4'].widget.attrs['disabled'] = 'disabled'
                self.fields['cvartal1'].widget.attrs['disabled'] = 'disabled'
            elif current_date <= date(2023, 9, 30):
                # Если текущая дата находится в 3 квартале, блокируем только поле cvartal4
                self.fields['cvartal4'].widget.attrs['disabled'] = 'disabled'
                self.fields['cvartal2'].widget.attrs['disabled'] = 'disabled'
                self.fields['cvartal1'].widget.attrs['disabled'] = 'disabled'
            elif current_date <= date(2023, 12, 30):
                # Если текущая дата находится в 4 квартале, блокируем только поле cvartal4
                self.fields['cvartal3'].widget.attrs['disabled'] = 'disabled'
                self.fields['cvartal2'].widget.attrs['disabled'] = 'disabled'
                self.fields['cvartal1'].widget.attrs['disabled'] = 'disabled'
    class Meta:
        model = Even
        fields = ['station', 'gpa_number', 'isnotnecessary', 'text', 'complete', 'cvartal1', 'cvartal2', 'cvartal3', 'cvartal4']
        widgets = {
            'complete': forms.HiddenInput(),
        }


class RegisterForm(UserCreationForm):
    username = forms.CharField(label=_('Никнейм'), max_length=30, widget=forms.TextInput(attrs={'class': 'reg-input', 'style': 'display: block;'}))
    first_name = forms.CharField(label=_('Имя'), max_length=30,
                                 widget=forms.TextInput(attrs={'class': 'reg-input', 'style': 'display: block;'}))
    last_name = forms.CharField(label=_('Фамилия'), max_length=30,
                                widget=forms.TextInput(attrs={'class': 'reg-input', 'style': 'display: block;'}))
    password1 = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput(attrs={'class': 'reg-input', 'style': 'display: block;'}))
    password2 = forms.CharField(label=_('Повторите пароль'), widget=forms.PasswordInput(attrs={'class': 'reg-input','style': 'display: block;'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class AuthForm(AuthenticationForm):
    username = forms.CharField(label=_('Имя'), widget=forms.TextInput(attrs={'class': 'login-input', 'style': 'display: block;', 'placeholder': 'Имя'}),
                               max_length=20)
    password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput(attrs={'class': 'password-input', 'style': 'display: block;', 'placeholder': 'Пароль'}))


class PredictionForm(forms.Form):
    type_refuses = forms.CharField(label='Тип отказа (АО, НПО)', max_length=500)
    type_gpa = forms.CharField(label='Тип Гпа', max_length=500)
    type_say = forms.CharField(label='Тип Сау', max_length=500)
    type_equioment = forms.CharField(label='Внешнее проявление отказа', max_length=500, widget=forms.TextInput(attrs={'style': 'width: 100% !important;'}))
    refuses_element = forms.CharField(label='Отказавший элемент', max_length=500)





