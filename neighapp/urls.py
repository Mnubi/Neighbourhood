from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name = 'index'),
    path('profile', views.profile, name="profile"),
    path('post', views.post, name="post"),
    path('update/<id>', views.update_profile, name='update_profile'),
    path('neighbourhood/', views.neighbourhood, name='neighbourhood'),
    path('business/', views.business, name='business'),
    path('join_neighbourhood/<id>', views.join_neighbourhood, name='join_neighbourhood'),
    path('leave_neighbourhood/<id>', views.leave_neighbourhood, name='leave_neighbourhood'),
    path('post', views.post, name='post'),
    path("alert/", views.alerts, name="alert"),
    path("contacts/", views.contacts, name="contacts"),
    
]
