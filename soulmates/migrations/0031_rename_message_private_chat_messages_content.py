# Generated by Django 3.2.8 on 2023-07-23 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soulmates', '0030_rename_receiver_friend_private_chat_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='private_chat_messages',
            old_name='message',
            new_name='content',
        ),
    ]
