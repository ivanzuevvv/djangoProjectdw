from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .forms import EvenForm, AuthForm, RegisterForm, PredictionForm
from .models import Execution, Event, Even, Narabotka, Otkaz, Vnerdenie, Profile, Category, Control, \
    Document1, Document3, Predicions, Document5, Category5
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page


def index(request):
    events = Category.objects.all()
    events1 = Execution.objects.all()
    events2 = Narabotka.objects.all()
    events3 = Otkaz.objects.all()

    return render(request, 'index.html', {'events': events, 'events1': events1, 'events2': events2, 'events3': events3})


class CreateEven(CreateView):
    model = Even
    fields = ('station', 'gpa_number', 'sau_modifications', 'plan',)

    def form_valid(self, form):
        response = super().form_valid(form)
        station = form.cleaned_data['station']
        department = form.cleaned_data['department']
        gpa_number = form.cleaned_data['gpa_number']
        sau_modifications = form.cleaned_data['sau_modifications']
        plan = form.cleaned_data['plan']
        complete = form.cleaned_data['complete']
        cvartal1 = form.cleaned_data['cvartal1']
        cvartal2 = form.cleaned_data['cvartal2']
        cvartal3 = form.cleaned_data['cvartal3']
        cvartal4 = form.cleaned_data['cvartal4']
        isnotnecessary = form.cleaned_data['isnotnecessary']
        #marks = form.cleaned_data['marks']
        text = form.cleaned_data['text']
        Even.objects.create(station=station,
                            department=department,
                            gpa_number=gpa_number,
                            sau_modifications=sau_modifications,
                            plan=plan,
                            complete=complete,
                            cvartal1=cvartal1,
                            cvartal2=cvartal2,
                            cvartal3=cvartal3,
                            cvartal4=cvartal4,
                            isnotnecessary=isnotnecessary,
                            #marks=marks,
                            text=text)
        return response


class UpdateEven(UpdateView):
    model = Even
    form_class = EvenForm
    template_name = 'update.html'
    success_url = reverse_lazy('k')

    def get_queryset(self):
        queryset = Even.objects.filter(user=self.request.user)
        return queryset

    # Обработка случая, когда пользователь не аутентифицирован

    def form_valid(self, form):
        current_complete = self.object.complete
        new_complete = form.cleaned_data['complete']
        diff = new_complete - current_complete

        cvartal1 = form.cleaned_data['cvartal1'] or 0
        cvartal2 = form.cleaned_data['cvartal2'] or 0
        cvartal3 = form.cleaned_data['cvartal3'] or 0
        cvartal4 = form.cleaned_data['cvartal4'] or 0

        self.object.cvartal1 == cvartal1
        self.object.cvartal2 == cvartal2
        self.object.cvartal3 == cvartal3
        self.object.cvartal4 == cvartal4

        self.object.complete = self.object.cvartal1 + self.object.cvartal2 + self.object.cvartal3 + self.object.cvartal4

        self.object.save()

        return super().form_valid(form)


class EvenView(ListView):
    model = Even
    context_object_name = 'evens'
    template_name = 'even.html'

    def get_queryset(self):
        queryset = Even.objects.filter(user=self.request.user)
        category = self.kwargs.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CompletedView(ListView):
    model = Even
    context_object_name = 'evens'
    template_name = 'even.html'

    def get_queryset(self):
        queryset = Even.completed().filter(user=self.request.user)
        return queryset


class NotCompletedView(ListView):
    model = Even
    context_object_name = 'evens'
    template_name = 'even.html'

    def get_queryset(self):
        queryset = Even.not_completed().filter(user=self.request.user)
        return queryset


@cache_page(60 * 15)
class CreateVnerdenie(CreateView):
    model = Vnerdenie
    fields = ('lpu', 'department', 'gpa_number', 'ip', 'type_equipment', 'ip_number')

    def form_valid(self, form):
        response = super().form_valid(form)
        lpu = form.cleaned_data['lpu']
        gpa_number = form.cleaned_data['gpa_number']
        department = form.cleaned_data['department']
        ip = form.cleaned_data['ip']
        type_equipment = form.cleaned_data['type_equipment']
        ip_number = form.cleaned_data['ip_number']
        done = form.cleaned_data['done']
        reason = form.cleaned_data['reason ']
        Vnerdenie.objects.create(lpu=lpu,
                            gpa_number=gpa_number,
                            department=department,
                            ip=ip,
                            type_equipment=type_equipment,
                            ip_number=ip_number,
                            done=done,
                            reason=reason)
        return response


class UpdateVnerdenie(UpdateView):
    model = Vnerdenie
    fields = ('reason', 'done')
    template_name = 'vnedreine_update.html'
    success_url = reverse_lazy('newsletters')


class VnerdenieView(ListView):
    model = Vnerdenie
    context_object_name = 'evenss'
    template_name = 'newsletters.html'

    def get_queryset(self):
        queryset = Vnerdenie.objects.filter(user=self.request.user)
        return queryset


class DocumentListView(ListView):
    model = Document5
    template_name = 'documentation.html'
    context_object_name = 'documents'


def download(request, document_id):
    document = get_object_or_404(Document5, pk=document_id)
    response = HttpResponse(document.document, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{document.document.name}"'
    return response


class Document1ListView(ListView):
    model = Document1
    template_name = 'racsuggestions.html'
    context_object_name = 'documents'


def download1(request, document_id):
    document = get_object_or_404(Document1, pk=document_id)
    response = HttpResponse(document.document1.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{document.document1.name}"'
    return response


def analiz(request):
    return render(request, 'analiz.html')


def prediction_view(request):
    if request.method == 'POST':
        type_refuses = request.POST.get('type_refuses')
        type_gpa = request.POST.get('type_gpa')
        type_say = request.POST.get('type_say')
        type_equioment = request.POST.get('type_equioment')

        predictions = Predicions.objects.filter(
            type_refuses=type_refuses,
            type_gpa=type_gpa,
            type_say=type_say,
            type_equioment=type_equioment
        )


        context = {
            'predictions': predictions,
            'type_equioment': Predicions.objects.filter(
                type_refuses=type_refuses,
                type_gpa=type_gpa,
                type_say=type_say,
            ).values_list('type_equioment', flat=True).distinct()
        }

        return render(request, 'refuses_form.html', context)

    type_refuses = Predicions.objects.values_list('type_refuses', flat=True).distinct()
    type_gpa = Predicions.objects.values_list('type_gpa', flat=True).distinct()
    type_say = Predicions.objects.values_list('type_say', flat=True).distinct()

    context = {
        'type_refuses': type_refuses,
        'type_gpa': type_gpa,
        'type_say': type_say,
    }

    return render(request, 'refuses_form.html', context)


def prediction_view2(request):
    if request.method == 'POST':
        type_refuses = request.POST.get('type_refuses')
        type_gpa = request.POST.get('type_gpa')
        type_say = request.POST.get('type_say')
        refuses_element = request.POST.get('refuses_element')

        predictions = Predicions.objects.filter(
            type_refuses=type_refuses,
            type_gpa=type_gpa,
            type_say=type_say,
            refuses_element=refuses_element
        )


        context = {
            'predictions': predictions,
            'refuses_element': Predicions.objects.filter(
                type_refuses=type_refuses,
                type_gpa=type_gpa,
                type_say=type_say,
            ).values_list('refuses_element', flat=True).distinct()
        }

        return render(request, 'analiz.html', context)

    type_refuses = Predicions.objects.values_list('type_refuses', flat=True).distinct()
    type_gpa = Predicions.objects.values_list('type_gpa', flat=True).distinct()
    type_say = Predicions.objects.values_list('type_say', flat=True).distinct()

    context = {
        'type_refuses': type_refuses,
        'type_gpa': type_gpa,
        'type_say': type_say,
    }

    return render(request, 'analiz.html', context)


def suggestions(request):
    return render(request, 'suggestions.html')


def newsletters(request):
    return render(request, 'newsletters.html')


# Регистрация, авторизация, выход из учетной записи пользователя
class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'register.html'

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        form = RegisterForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            user = form.save()
            if self.request.FILES:
                avatar = self.request.FILES['avatar']
                Profile.objects.create(user=user, avatar=avatar)
            user.save()
        return super(RegisterView, self).form_valid(form)


class AuthView(LoginView):
    form_class = AuthForm
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('index')


class LogOut(LogoutView):
    template_name = 'logout.html'
    next_page = '/'


# Информация о пользователе

class UserInfo(DetailView):
    model = User
    template_name = 'user_info.html'
    context_object_name = 'user_info'


    def get_object(self, queryset=None):
        return self.request.user


class CreateControl(CreateView):
    model = Control
    fields = ('lpu', 'station', 'department', 'gpa_number', 'gpa_typle', 'sau_modifications', 'type_equioment', 'ip', 'data_complete', 'n_ip')

    def form_valid(self, form):
        response = super().form_valid(form)
        lpu = form.cleaned_data['lpu']
        station = form.cleaned_data['station']
        department = form.cleaned_data['department']
        gpa_typle = form.cleaned_data['gpa_typle']
        gpa_number = form.cleaned_data['gpa_number']
        sau_modifications = form.cleaned_data['sau_modifications']
        ip_number = form.cleaned_data['ip_number']
        type_equioment = form.cleaned_data['type_equioment']
        n_ip = form.cleaned_data['n_ip']
        data_complete = form.cleaned_data['data_complete']
        category5 = form.cleaned_data['category5']
        text = form.cleaned_data['text']
        Control.objects.create(lpu=lpu,
                            station=station,
                            department=department,
                            gpa_number=gpa_number,
                            sau_modifications = sau_modifications ,
                            ip_number=ip_number,
                            type_equioment=type_equioment,
                            n_ip=n_ip,
                            data_complete=data_complete,
                            category5=category5,
                            text=text,
                            gpa_typle=gpa_typle

                                 )
        return response


class UpdateControl(UpdateView):
    model = Control
    fields = ('text', 'category5')
    template_name = 'control_update.html'
    success_url = reverse_lazy('control')


class ControlView(ListView):
    model = Control
    context_object_name = 'evenss'
    template_name = 'control.html'

    def get_queryset(self):
        queryset = Control.objects.filter(user=self.request.user)
        category5 = self.kwargs.get('category5')
        if category5:
            queryset = queryset.filter(category5__name=category5)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories5'] = Category5.objects.all()
        return context


class CreateReister(CreateView):
    model = Document3
    fields = ('ip', 'ip_code ', 'naim_ip', 'type_gpa', 'type_equioment', 'type_equiomentt', 'filial', 'date', 'link',)

    def form_valid(self, form):
        response = super().form_valid(form)
        ip = form.cleaned_data['ip']
        ip_code = form.cleaned_data['ip_code']
        naim_ip = form.cleaned_data['naim_ip']
        type_gpa = form.cleaned_data['type_gpa']
        type_equioment = form.cleaned_data['type_equioment']
        type_equiomentt = form.cleaned_data['type_equiomentt']
        filial = form.cleaned_data['filial']
        date = form.cleaned_data['date']
        link = form.cleaned_data['link']
        text = form.cleaned_data['text']
        Document3.objects.create(ip=ip,
                            ip_code=ip_code,
                            naim_ip=naim_ip,
                            type_gpa=type_gpa,
                            type_equioment=type_equioment,
                            type_equiomentt=type_equiomentt,
                            filial=filial,
                            date=date,
                            link=link,
                            text=text,

                                 )
        return response


class UpdateReister(UpdateView):
    model = Document3
    fields = ('text',)
    template_name = 'reister_update.html'
    success_url = reverse_lazy('reister')


class ReisterView(ListView):
    model = Document3
    context_object_name = 'documents'
    template_name = 'reister.html'


def download3(request, document_id):
    document = get_object_or_404(Document3, pk=document_id)
    response = HttpResponse(document.document3.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{document.document3.name}"'
    return response

