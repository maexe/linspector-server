# Generated by Django 2.2 on 2019-05-28 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspector', '0005_auto_20190507_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='probingtask',
            name='name',
            field=models.CharField(max_length=35, unique=True),
        ),
    ]
