# Generated by Django 3.2.8 on 2023-07-16 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soulmates', '0024_auto_20230716_2203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='public_chat_room',
            name='users',
        ),
        migrations.DeleteModel(
            name='public_room_chat_message_manager',
        ),
        migrations.RemoveField(
            model_name='public_room_chat_messages',
            name='room',
        ),
        migrations.RemoveField(
            model_name='public_room_chat_messages',
            name='user',
        ),
        migrations.DeleteModel(
            name='public_chat_room',
        ),
        migrations.DeleteModel(
            name='public_room_chat_messages',
        ),
    ]
