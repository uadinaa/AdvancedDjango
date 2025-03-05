# Generated by Django 5.1.6 on 2025-03-05 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('carbs', models.FloatField(default=0)),
                ('proteins', models.FloatField(default=0)),
                ('fats', models.FloatField(default=0)),
                ('calories', models.IntegerField(default=0)),
            ],
        ),
    ]
