# Generated by Django 3.2.7 on 2021-10-22 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_userprofile_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='about',
            field=models.TextField(blank=True, null=True, verbose_name='о себе'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'М'), ('W', 'Ж')], max_length=5, verbose_name='пол'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='tagline',
            field=models.CharField(blank=True, max_length=128, verbose_name='тэги'),
        ),
    ]
