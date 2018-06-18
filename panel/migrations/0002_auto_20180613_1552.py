# Generated by Django 2.0.5 on 2018-06-13 20:52

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-publicar',)},
        ),
        migrations.AlterModelManagers(
            name='post',
            managers=[
                ('objetos', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RenameField(
            model_name='post',
            old_name='publicado',
            new_name='publicar',
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=250, unique_for_date='publicar'),
        ),
    ]
