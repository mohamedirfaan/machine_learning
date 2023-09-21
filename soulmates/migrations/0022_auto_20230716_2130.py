# Generated by Django 3.2.8 on 2023-07-16 16:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soulmates', '0021_auto_20230716_2038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='public_room_chat_messages',
            name='content',
        ),
        migrations.RemoveField(
            model_name='public_room_chat_messages',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='public_chat_room',
            name='content',
            field=models.ManyToManyField(blank=True, related_name='content', to='soulmates.Messages'),
        ),
        migrations.RemoveField(
            model_name='public_room_chat_messages',
            name='user',
        ),
        migrations.AddField(
            model_name='public_room_chat_messages',
            name='user',
            field=models.ManyToManyField(related_name='user1', to=settings.AUTH_USER_MODEL),
        ),
    ]
