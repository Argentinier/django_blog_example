# Generated by Django 4.0.3 on 2022-04-10 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='slug_name',
            new_name='slug',
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[(None, 'Select the Post Status'), ('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=250),
        ),
    ]
