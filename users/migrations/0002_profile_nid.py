# Generated by Django 2.1.7 on 2019-04-03 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='nid',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
    ]