# Generated by Django 4.0.3 on 2022-03-23 17:07

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovedProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='title', unique=True)),
                ('userimg', models.ImageField(upload_to='')),
                ('about', models.TextField()),
                ('category', models.CharField(max_length=30)),
                ('currency', models.CharField(max_length=10)),
                ('minrate', models.IntegerField()),
                ('maxrate', models.IntegerField()),
                ('skill1', models.CharField(max_length=50)),
                ('skill2', models.CharField(max_length=50)),
                ('skill3', models.CharField(max_length=50)),
                ('skill4', models.CharField(max_length=50)),
                ('skill5', models.CharField(max_length=50)),
                ('jobstart', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='PendingProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='title', unique=True)),
                ('userimg', models.ImageField(upload_to='')),
                ('about', models.TextField()),
                ('category', models.CharField(max_length=30)),
                ('currency', models.CharField(max_length=10)),
                ('minrate', models.IntegerField()),
                ('maxrate', models.IntegerField()),
                ('skill1', models.CharField(max_length=50)),
                ('skill2', models.CharField(max_length=50)),
                ('skill3', models.CharField(max_length=50)),
                ('skill4', models.CharField(max_length=50)),
                ('skill5', models.CharField(max_length=50)),
                ('jobstart', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=50)),
                ('image', models.ImageField(default='default/default.jpg', upload_to='default')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
