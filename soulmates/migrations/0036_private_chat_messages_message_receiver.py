# Generated by Django 3.2.8 on 2023-07-30 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('soulmates', '0035_private_chat_messages_message_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='private_chat_messages',
            name='message_receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver', to='soulmates.member'),
            preserve_default=False,
        ),
    ]