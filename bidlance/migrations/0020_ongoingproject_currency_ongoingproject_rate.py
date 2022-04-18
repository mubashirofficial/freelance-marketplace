# Generated by Django 4.0.3 on 2022-03-27 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidlance', '0019_ongoingproject'),
    ]

    operations = [
        migrations.AddField(
            model_name='ongoingproject',
            name='currency',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ongoingproject',
            name='rate',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
