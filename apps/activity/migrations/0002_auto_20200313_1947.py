# Generated by Django 2.2.7 on 2020-03-13 19:47

from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='image',
            field=stdimage.models.StdImageField(blank=True, default='', upload_to='Activity/image', verbose_name='图片路径'),
        ),
    ]
