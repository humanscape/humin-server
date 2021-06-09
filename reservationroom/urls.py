"""reservationroom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from batch_tasks import views as batch_task_view
from events import views as event_view
from users import views as user_view

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/update/', batch_task_view.get, name='update'),
    path('api/room/', event_view.get_full_roomnames, name='roomname_list'),
    path('api/event/', event_view.list, name='event_list'),
    path('api/event/<room_name>/', event_view.retrieve, name='event_retrieve'),
    path('api/user/', user_view.list, name='user_list'),
    path('api/user/<email>/', user_view.retrieve, name='user_retrieve'),
    path('api/user/search/<keyword>/', user_view.search, name='user_search'),
    path('api/user/organization/<organization>/', user_view.list_by_organization, name='user_list_by_org')
]
