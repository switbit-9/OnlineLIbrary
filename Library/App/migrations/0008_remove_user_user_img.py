# Generated by Django 3.1.4 on 2021-07-13 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_books_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_img',
        ),
    ]
