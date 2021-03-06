# Generated by Django 4.0.5 on 2022-06-28 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Category Name', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Item Name', max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.CharField(help_text='Player Name', max_length=50)),
                ('time', models.DurationField(blank=True, help_text='Game Duration', null=True)),
                ('answer', models.CharField(blank=True, help_text='Player Answer', max_length=50, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(help_text='Category Selected', on_delete=django.db.models.deletion.RESTRICT, to='tellme.category')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='items',
            field=models.ManyToManyField(help_text='Category Items', to='tellme.item'),
        ),
    ]
