from django.urls import path
from back.views import *


urlpatterns = [
    path('documentation/', DocumentListView.as_view(), name='documentation'),
    path('documentation/download/<int:document_id>/', download, name='download'),
    path('report/', Document2ListView.as_view(), name='report'),
    path('report/download/<int:document_id>/', download, name='download'),
    path('suggestions/', Document1ListView.as_view(), name='suggestions'),
    path('suggestions/download1/<int:document_id>/', download1, name='download1'),
    path('index/', index, name='index'),
    path('k/', EvenView.as_view(), name='k'),
    path('Notk/', NotEvenView.as_view(), name='Notk'),
    path('completed/', CompletedView.as_view(), name='completed'),
    path('not-completed/', NotCompletedView.as_view(), name='not_completed'),
    path('<int:pk>/update/', UpdateEven.as_view(), name='update'),

    path('<int:pk>/update2/', NotUpdateEven.as_view(), name='update2'),

    path('notnot-completed/', NotNotCompletedView.as_view(), name='notnot_completed'),

    path('Notk/<str:category>/', NotEvenView.as_view(), name='NotK'),


    path('completed2/', CompCompletedView.as_view(), name='completed2'),

    path('analiz/', prediction_view2, name='analiz'),
    path('predictions/', prediction_view, name='predictions'),
    path('newsletters/', VnerdenieView.as_view(), name='newsletters'),
    path('<int:pk>/updates/', UpdateVnerdenie.as_view(), name='updates'),
    path('user_detail/', UserInfo.as_view(), name='user_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', AuthView.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('k/<str:category>/', EvenView.as_view(), name='even'),
    path('control/', ControlView.as_view(), name='control'),
    path('control/<str:category5>/', ControlView.as_view(), name='control2'),
    path('<int:pk>/updatesss/', UpdateControl.as_view(), name='updatesss'),
    path('reister/', ReisterView.as_view(), name='reister'),
    path('reister/download3/<int:document_id>/', download3, name='download3'),
    path('<int:pk>/updatessss/', UpdateReister.as_view(), name='updatessss'),
    path('chat/', chat_view, name='chat_api'),  # API для обработки сообщений
    path('c/', chat_page, name='chat_page'),      # Веб-страница чата
    path('t/', chatbot_view, name='chatbot_api'),
    path('r', chat2_page, name='chat2_page'),

    path('v/', chat_page, name='chat_page'),  # Отображение HTML-страницы
    path('chaat/', chatbot_view, name='chatbot_api'),  # API для обработки сообщений
]

