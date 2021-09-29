# Generated by Django 3.1.4 on 2021-09-25 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0015_auto_20210920_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('borrowed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.borrow')),
                ('saved', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.save')),
            ],
        ),
    ]