# Generated by Django 4.0.3 on 2022-03-27 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bidlance', '0013_alter_proposals_options_proposals_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposals',
            name='slug',
        ),
    ]