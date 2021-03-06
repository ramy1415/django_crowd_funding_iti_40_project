# Generated by Django 2.2.1 on 2020-03-18 00:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_body', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('details', models.TextField()),
                ('current_money', models.IntegerField(default=0)),
                ('total_target', models.IntegerField()),
                ('start_time', models.DateField(auto_now_add=True)),
                ('end_time', models.DateField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ReportProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_project_body', models.TextField()),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.Project')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReportComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_comment_body', models.TextField()),
                ('comment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.Comment')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.Project')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(to='Projects.Tag'),
        ),
        migrations.AddField(
            model_name='project',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic_path', models.ImageField(upload_to='images/projects/')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='FeaturedProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.Project')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.Project'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
