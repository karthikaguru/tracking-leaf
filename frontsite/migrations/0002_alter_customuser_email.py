# Generated by Django 4.2.20 on 2025-04-22 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontsite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(db_index=True, max_length=255),
        ),
    ]
