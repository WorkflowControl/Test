# Generated by Django 3.2.7 on 2022-04-22 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0053_auto_20220413_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='keep_mail',
            field=models.BooleanField(default=False, help_text='After processing, should mail be kept in the inbox? (IMAP only.)'),
        ),
    ]
