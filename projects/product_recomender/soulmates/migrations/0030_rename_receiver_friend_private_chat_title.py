# Generated by Django 3.2.8 on 2023-07-23 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soulmates', '0029_private_chat_private_chat_messages'),
    ]

    operations = [
        migrations.RenameField(
            model_name='private_chat',
            old_name='receiver_friend',
            new_name='title',
        ),
    ]