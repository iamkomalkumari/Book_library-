# Generated by Django 5.0.4 on 2025-01-22 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myapp', '0004_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=30)),
                ('publication', models.CharField(max_length=45)),
                ('date', models.DateField()),
            ],
        ),
    ]
