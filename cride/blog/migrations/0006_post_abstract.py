# Generated by Django 4.2.5 on 2023-09-15 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='abstract',
            field=models.CharField(default='', max_length=255),
        ),
    ]