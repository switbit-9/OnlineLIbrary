# Generated by Django 3.1.4 on 2021-07-12 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_user_user_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='user_book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.user'),
        ),
    ]
