# Generated by Django 3.2.7 on 2021-10-18 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20211017_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
