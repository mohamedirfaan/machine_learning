# Generated by Django 3.2.8 on 2023-07-10 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soulmates', '0014_alter_member_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='profile_pic',
            field=models.ImageField(blank=True, default='C:\\Users\\mohamed irfaan\\OneDrive\\Pictures\\GHOST house.png', null=True, upload_to='images/'),
        ),
    ]