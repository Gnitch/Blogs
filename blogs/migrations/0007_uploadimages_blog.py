# Generated by Django 3.0.3 on 2020-05-22 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_remove_uploadimages_blog_super'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadimages',
            name='blog',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blogs.Blog'),
            preserve_default=False,
        ),
    ]