# Generated by Django 3.2.8 on 2023-07-16 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soulmates', '0018_auto_20230714_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='public_room_chat_messages',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
