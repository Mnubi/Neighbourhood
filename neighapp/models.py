from django.db import models
from datetime import datetime as dt
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Location(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # save location
    def save_location(self):
        self.save()

    def __str__(self):
        return self.name

class Neighbourhood(models.Model):
    neighbourhood_name = models.CharField(max_length=200)
    neighbourhood_location = models.CharField(max_length=200)
    neighbourhood_description = models.CharField(max_length=500)
    neighbourhood_photo = CloudinaryField('photo', default='photo')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.neighbourhood_name

    def save_neighbourhood(self):
        self.save()

    def delete_neighbourhood(self):
        self.delete()

    @classmethod
    def find_neighbourhood(cls, neighbourhood_id):
        return cls.objects.filter(id=neighbourhood_id)

    @property
    def occupants_count(self):
        return self.neighbourhood_users.count()

    def update_neighbourhood(self):
        neighbourhood_name = self.neighbourhood_name
        self.neighbourhood_name = neighbourhood_name

class Business(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # create business
    def create_business(self):
        self.save()

    # delete business
    def delete_business(self):
        self.delete()

    # update business
    def update_business(self):
        self.update()

    # search business
    @classmethod
    def search_by_name(cls, search_term):
        business = cls.objects.filter(name__icontains=search_term)
        return business

    # find business by id
    @classmethod
    def find_business(cls, id):
        business = cls.objects.get(id=id)
        return business

    def __str__(self):
        return self.name

# contact class model
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    neighbourhood = models.ForeignKey(
        Neighbourhood, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # creating contact
    def create_contact(self):
        self.save()

    # deleting contact
    def delete_contact(self):
        self.delete()

    # updating contact
    def update_contact(self):
        self.update()

    # searching for contact
    @classmethod
    def search_by_name(cls, search_term):
        contact = cls.objects.filter(name__icontains=search_term)
        return contact

    # find contact by id
    @classmethod
    def find_contact(cls, id):
        contact = cls.objects.get(id=id)
        return contact

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, blank=True, null=True)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, blank=True, null=True)
    profile_pic = CloudinaryField('image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save_profile(self):
        self.save()

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=150)
    image = CloudinaryField('images')
    content = models.TextField(max_length=300, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    neighbourhood = models.ForeignKey(
        Neighbourhood, on_delete=models.CASCADE, default='', null=True, blank=True)

    def create_post(self):
        self.save()

    def save_post(self):
        return self.save()

    def delete_post(self):
        self.delete()

    def __str__(self):
        return self.title