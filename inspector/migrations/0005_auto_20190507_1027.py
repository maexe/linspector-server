# Generated by Django 2.2 on 2019-05-07 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspector', '0004_auto_20190506_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='probingtask',
            name='contrastive',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='model',
            name='upload',
            field=models.FileField(upload_to=''),
        ),
    ]
