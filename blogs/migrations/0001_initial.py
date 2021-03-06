# Generated by Django 3.0.3 on 2020-06-19 18:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('youtube_video_id', models.CharField(max_length=500)),
                ('video', models.FileField(null=True, upload_to='Blogs/Videos', verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='BlogComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, validators=[django.core.validators.MinLengthValidator(250)])),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.Blog')),
                ('usr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Communities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UploadImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='Blogs/Images')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('status', models.CharField(max_length=500)),
                ('usr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogUpvotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='blogs.BlogComments')),
                ('users', models.ManyToManyField(blank=True, related_name='requirement_comment_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogDownvotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dis_likes', to='blogs.BlogComments')),
                ('users', models.ManyToManyField(blank=True, related_name='requirement_comment_dis_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='community',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogs.Communities'),
        ),
        migrations.AddField(
            model_name='blog',
            name='usr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
