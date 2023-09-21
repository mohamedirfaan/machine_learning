# Generated by Django 3.2.8 on 2023-07-16 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('soulmates', '0025_auto_20230716_2206'),
    ]

    operations = [
        migrations.CreateModel(
            name='public_chat_room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('users', models.ManyToManyField(blank=True, help_text='users online', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='public_room_chat_message_manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='public_room_chat_messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room1', to='soulmates.public_chat_room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]