# Generated by Django 3.1.4 on 2021-07-15 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_remove_user_user_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='url',
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='publisher',
            name='url_a',
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
    ]
