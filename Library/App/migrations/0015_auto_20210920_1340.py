# Generated by Django 3.1.4 on 2021-09-20 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0014_auto_20210920_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='books_img',
            field=models.URLField(blank=True, default=None, max_length=2000, null=True),
        ),
    ]
