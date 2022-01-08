from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name = 'index'),
    path('profile', views.profile, name="profile"),
    path('post', views.post, name="post"),
    path('update/<id>', views.update_profile, name='update_profile'),
    path('neighbourhood/', views.neighbourhood, name='neighbourhood'),
    path("contacts/", views.contacts, name="contacts"),
    
]
