# Generated by Django 3.2.8 on 2023-07-16 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('soulmates', '0023_auto_20230716_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='public_room_chat_messages',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='public_room_chat_messages',
            name='content',
        ),
        migrations.AddField(
            model_name='public_room_chat_messages',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='public_room_chat_messages',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room1', to='soulmates.public_chat_room'),
        ),
        migrations.RemoveField(
            model_name='public_room_chat_messages',
            name='user',
        ),
        migrations.AddField(
            model_name='public_room_chat_messages',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Messages',
        ),
    ]
