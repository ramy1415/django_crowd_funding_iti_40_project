# Generated by Django 2.2.1 on 2020-03-18 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profiles',
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='images/profiles/default_profile.png', upload_to='images/profiles/'),
        ),
    ]