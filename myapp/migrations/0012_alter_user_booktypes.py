# Generated by Django 5.0.4 on 2025-01-25 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_alter_user_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='booktypes',
            field=models.CharField(max_length=45),
        ),
    ]
