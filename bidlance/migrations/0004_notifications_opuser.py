# Generated by Django 4.0.3 on 2022-03-24 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidlance', '0003_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='opuser',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]