# Generated by Django 4.0.5 on 2022-06-28 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tellme', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='items',
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ForeignKey(default='', help_text='Item Category', on_delete=django.db.models.deletion.CASCADE, to='tellme.category'),
            preserve_default=False,
        ),
    ]
