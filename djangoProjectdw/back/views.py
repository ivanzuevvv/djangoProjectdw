from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .forms import EvenForm, AuthForm, RegisterForm, PredictionForm, NotEvenForm
from .models import Execution, Event, Even, Narabotka, Otkaz, Vnerdenie, Profile, Category, Control, \
    Document1, Document3, Predicions, Document5, Category5, Document6, NotEven, Category4
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

########################
class Document2ListView(ListView):
    model = Document6
    template_name = 'report.html'
    context_object_name = 'documents'


def download2(request, document_id):
    document = get_object_or_404(Document5, pk=document_id)
    response = HttpResponse(document.document, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{document.document.name}"'
    return response

###########################
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





################################################################
class NotCreateEven(CreateView):
    model = NotEven
    fields = ('station', 'gpa_number', 'sau_modifications', 'plan',)

    def form_valid(self, form):
        response = super().form_valid(form)
        station = form.cleaned_data['station']
        department = form.cleaned_data['department']
        gpa_number = form.cleaned_data['gpa_number']
        sau_modifications = form.cleaned_data['sau_modifications']
        cvartal1 = form.cleaned_data['cvartal1']
        cvartal2 = form.cleaned_data['cvartal2']
        cvartal3 = form.cleaned_data['cvartal3']
        cvartal4 = form.cleaned_data['cvartal4']
        cvartal5 = form.cleaned_data['cvartal5']
        cvartal6 = form.cleaned_data['cvartal6']
        cvartal7 = form.cleaned_data['cvartal7']
        cvartal8 = form.cleaned_data['cvartal8']
        cvartal9 = form.cleaned_data['cvartal9']
        cvartal10 = form.cleaned_data['cvartal10']
        cvartal11 = form.cleaned_data['cvartal11']
        cvartal12 = form.cleaned_data['cvartal12']
        isnotnecessary = form.cleaned_data['isnotnecessary']
        #marks = form.cleaned_data['marks']
        text = form.cleaned_data['text']
        category = form.cleaned_data['category']
        NotEven.objects.create(station=station,
                            department=department,
                            gpa_number=gpa_number,
                            sau_modifications=sau_modifications,
                            cvartal1=cvartal1,
                            cvartal2=cvartal2,
                            cvartal3=cvartal3,
                            cvartal4=cvartal4,
                            cvartal5=cvartal5,
                            cvartal6=cvartal6,
                            cvartal7=cvartal7,
                            cvartal8=cvartal8,
                            cvartal9=cvartal9,
                            cvartal10=cvartal10,
                            cvartal11=cvartal11,
                            cvartal12=cvartal12,
                            category=category,
                               )
        return response


class NotUpdateEven(UpdateView):
    model = NotEven
    form_class = NotEvenForm
    template_name = 'notupdate.html'
    success_url = reverse_lazy('Notk')

    def get_queryset(self):
        queryset = NotEven.objects.filter(user=self.request.user)
        return queryset

    # Обработка случая, когда пользователь не аутентифицирован

    def form_valid(self, form):
        current_complete = self.object.complete
        new_complete = form.cleaned_data['complete']
        diff = new_complete - current_complete

        # Получаем значения кварталов из формы
        cvartal1 = form.cleaned_data['cvartal1']
        cvartal2 = form.cleaned_data['cvartal2']
        cvartal3 = form.cleaned_data['cvartal3']
        cvartal4 = form.cleaned_data['cvartal4']
        cvartal5 = form.cleaned_data['cvartal5']
        cvartal6 = form.cleaned_data['cvartal6']
        cvartal7 = form.cleaned_data['cvartal7']
        cvartal8 = form.cleaned_data['cvartal8']
        cvartal9 = form.cleaned_data['cvartal9']
        cvartal10 = form.cleaned_data['cvartal10']
        cvartal11 = form.cleaned_data['cvartal11']
        cvartal12 = form.cleaned_data['cvartal12']

        # Присваиваем значения объекту
        self.object.cvartal1 = cvartal1
        self.object.cvartal2 = cvartal2
        self.object.cvartal3 = cvartal3
        self.object.cvartal4 = cvartal4
        self.object.cvartal5 = cvartal5
        self.object.cvartal6 = cvartal6
        self.object.cvartal7 = cvartal7
        self.object.cvartal8 = cvartal8
        self.object.cvartal9 = cvartal9
        self.object.cvartal10 = cvartal10
        self.object.cvartal11 = cvartal11
        self.object.cvartal12 = cvartal12

        # Суммируем все кварталы и сохраняем результат в поле complete
        self.object.complete = (
            (cvartal1 == '-') + (cvartal2 == '-') + (cvartal3 == '-') +
            (cvartal4 == '-') + (cvartal5 == '-') + (cvartal6 == '-') +
            (cvartal7 == '-') + (cvartal8 == '-') + (cvartal9 == '-') +
            (cvartal10 == '-') + (cvartal11 == '-') + (cvartal12 == '-')
        )

        self.object.save()

        return super().form_valid(form)

class NotEvenView(ListView):
    model = NotEven
    context_object_name = 'evens'
    template_name = 'noteven.html'

    def get_queryset(self):
        queryset = NotEven.objects.filter(user=self.request.user)
        category = self.kwargs.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category4.objects.all()
        return context


class NotNotCompletedView(ListView):
    model = NotEven
    context_object_name = 'evens'
    template_name = 'noteven.html'

    def get_queryset(self):
        queryset = NotEven.not_completed().filter(user=self.request.user)
        return queryset


class CompCompletedView(ListView):
    model = NotEven
    context_object_name = 'evens'
    template_name = 'noteven.html'

    def get_queryset(self):
        queryset = NotEven.completed().filter(user=self.request.user)
        return queryset


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ChatResponse

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', 'привет').lower()

        # Ищем подходящий ответ
        response_obj = ChatResponse.objects.filter(keyword__iexact=user_message).first()
        if response_obj:
            response = response_obj.response
        else:
            response = "Извините, я не понял ваш запрос."

        return JsonResponse({'response': response})

    return JsonResponse({'error': 'Только POST-запросы поддерживаются.'})

def chat_page(request):
    return render(request, 'chat_page.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import DialogueStep


@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '').lower()
        current_step_id = data.get('current_step')  # ID текущего шага диалога

        # Если это начало диалога
        if not current_step_id:
            first_step = DialogueStep.objects.filter(previous_step__isnull=True).first()
            if first_step:
                return JsonResponse({
                    'question': first_step.question,
                    'step_id': first_step.id
                })

        # Если диалог продолжается
        try:
            current_step = DialogueStep.objects.get(id=current_step_id)
            if user_message == current_step.expected_answer.lower():
                next_step = current_step.next_step
                if next_step:
                    return JsonResponse({
                        'question': next_step.question,
                        'step_id': next_step.id
                    })
                else:
                    return JsonResponse({'message': 'Диалог завершён.'})
            else:
                return JsonResponse({'message': 'Ответ не распознан, попробуйте ещё раз.'})
        except DialogueStep.DoesNotExist:
            return JsonResponse({'error': 'Текущий шаг не найден.'})

    return JsonResponse({'error': 'Только POST-запросы поддерживаются.'})






from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Сценарий диалога
dialogue_script = [
    {"question": "Здравствуйте, что у вас случилось?", "expected": None},
    {"question": "Прошу уточнить наименование системы.", "expected": None},
    {"question": "Подскажите, неисправный компонент найден?", "expected": ["нет", "да"]},
    {"question": (
        "Вам необходимо проверить работоспособность оборудования цепи контроля: "
        "датчик, линия связи, промежуточные блоки. Используйте при этом руководство "
        "по эксплуатации и инструкции по проверке работоспособности. Не забывайте о "
        "мерах безопасности, подготовьте рабочее место и допустите сменного инженера."
    ), "expected": None},
]

# Обработчик для отображения HTML-страницы
def chat_page(request):
    return render(request, 'chat1.html')  # Путь к HTML-шаблону

# Обработчик для API чата
@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '').strip().lower()
        step = int(data.get('step', 0))  # Текущий шаг диалога (по умолчанию 0)

        # Проверяем шаг
        if step < len(dialogue_script):
            current_step = dialogue_script[step]
            # Проверяем ответ пользователя, если это необходимо
            if current_step["expected"] and user_message not in current_step["expected"]:
                return JsonResponse({"question": "Ответ не распознан. Попробуйте ещё раз.", "step": step})

            # Переходим к следующему шагу
            step += 1
            if step < len(dialogue_script):
                next_question = dialogue_script[step]["question"]
                return JsonResponse({"question": next_question, "step": step})
            else:
                return JsonResponse({"question": "Диалог завершён. Спасибо!", "step": step})

    return JsonResponse({"error": "Неверный запрос"})





from django.shortcuts import render

# Сценарий диалога
dialogue_script = [
    {"question": "", "expected": ["произошло ложное срабатывание системы пожаротушения"]},
    {"question": "Прошу уточнить наименование системы.", "expected": ["аспикз"]},
    {"question": "Подскажите, неисправный компонент найден?", "expected": ["нет"]},
    {"question": (

        "Вам необходимо проверить работоспособность оборудования цепи контроля: "
        "датчик, линия связи, промежуточные блоки. Используйте при этом руководство "
        "по эксплуатации и инструкции по проверке работоспособности. Не забывайте о "
        "мерах безопасности, подготовьте рабочее место и допустите сменного инженера."
    ), "expected": None},
]

def chat2_page(request):
    # Получаем данные из запроса
    step = int(request.POST.get('step', 0))  # Текущий шаг (по умолчанию 0)
    user_message = request.POST.get('message', '').strip().lower()  # Сообщение пользователя

    # Проверяем текущий шаг
    if step > 0 and step <= len(dialogue_script):
        current_step = dialogue_script[step - 1]

        # Проверяем ожидания на этом шаге
        if current_step["expected"] and user_message not in current_step["expected"]:
            bot_message = "Ответ не распознан. Попробуйте ещё раз."
            step -= 1  # Возвращаемся на этот же шаг
        else:
            bot_message = dialogue_script[step]["question"] if step < len(dialogue_script) else "Диалог завершён. Спасибо!"
    else:
        # Начало диалога
        bot_message = dialogue_script[0]["question"]

    # Передаем данные в шаблон
    return render(request, 'chat2.html', {
        'bot_message': bot_message,
        'step': step + 1,  # Переходим к следующему шагу
        'user_message': user_message,
    })