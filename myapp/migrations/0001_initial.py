# Generated by Django 5.0.4 on 2024-12-11 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.TextField(max_length=30)),
                ('publication', models.TextField(max_length=45)),
                ('date', models.DateField(max_length=30)),
            ],
        ),
    ]
