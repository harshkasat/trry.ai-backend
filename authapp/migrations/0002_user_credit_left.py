# Generated by Django 5.1.5 on 2025-02-19 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='credit_left',
            field=models.IntegerField(default=5),
        ),
    ]
