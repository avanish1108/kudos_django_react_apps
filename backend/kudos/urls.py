# kudos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('me/', views.current_user, name='current-user'),
    path('team-members/', views.TeamMembersListView.as_view(), name='team-members'),
    path('kudos/give/', views.KudoCreateView.as_view(), name='give-kudo'),
    path('kudos/received/', views.ReceivedKudosListView.as_view(), name='received-kudos'),
    path('kudos/given/', views.GivenKudosListView.as_view(), name='given-kudos'),
]