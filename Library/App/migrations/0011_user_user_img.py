# Generated by Django 3.1.4 on 2021-07-18 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_auto_20210715_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_img',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/profile pictures'),
        ),
    ]
