# Generated by Django 3.0.5 on 2020-04-12 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crwaling', '0005_auto_20200412_1837'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='qeustion',
            new_name='issue',
        ),
    ]
