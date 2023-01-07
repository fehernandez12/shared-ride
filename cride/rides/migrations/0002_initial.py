# Generated by Django 4.1.5 on 2023-01-07 23:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rides', '0001_initial'),
        ('circles', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='offered_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ride',
            name='offered_in',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='circles.circle'),
        ),
        migrations.AddField(
            model_name='ride',
            name='passengers',
            field=models.ManyToManyField(related_name='passengers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rating',
            name='circle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circles.circle'),
        ),
        migrations.AddField(
            model_name='rating',
            name='rated_user',
            field=models.ForeignKey(help_text='User that receives the rating.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rated_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rating',
            name='rating_user',
            field=models.ForeignKey(help_text='User that emits the rating', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rating_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rating',
            name='ride',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated_ride', to='rides.ride'),
        ),
    ]
