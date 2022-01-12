from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name = 'index'),
    path('profile', views.profile, name="profile"),
    path('update/<id>', views.update_profile, name='update_profile'),
    path('neighbourhood/', views.neighbourhood, name='neighbourhood'),
    path('business/', views.business, name='business'),
    path("businesses/", views.businesses, name="businesses"),
    path("create_business", views.create_business, name="create_business"),
    path('join_neighbourhood/<id>', views.join_neighbourhood, name='join_neighbourhood'),
    path('leave_neighbourhood/<id>', views.leave_neighbourhood, name='leave_neighbourhood'),
    path('post', views.posts, name='post'),
    path('create_post', views.create_post, name='create_post'),
    path("alert/", views.alerts, name="alert"),
    path("contacts/", views.contacts, name="contacts"),
    path("search", views.search, name="search"),
    
]
