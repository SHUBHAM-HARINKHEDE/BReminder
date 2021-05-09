# Generated by Django 3.0.8 on 2020-08-28 13:36

from django.db import migrations, models
import user.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200708_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='birthday',
            name='email',
            field=models.EmailField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='birthday',
            name='mobile',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[user.validators.validate_mobile_number]),
        ),
        migrations.AddField(
            model_name='birthday',
            name='whatsapp_number',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[user.validators.validate_mobile_number]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[user.validators.validate_mobile_number]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='whatsapp_number',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[user.validators.validate_mobile_number]),
        ),
    ]