# Generated by Django 3.2.9 on 2022-01-10 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('neighapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='neighbourhood',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='neighapp.neighbourhood'),
        ),
    ]
