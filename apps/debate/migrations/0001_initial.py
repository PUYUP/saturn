# Generated by Django 2.2.7 on 2019-11-21 04:35

import apps.debate.utils.files
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('label', models.CharField(max_length=255)),
                ('slug', models.SlugField(editable=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, limit_choices_to={'parent__isnull': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='childs', to='debate.Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'debate_category',
                'abstract': False,
                'unique_together': {('label',)},
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('label', models.CharField(max_length=355)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Tertunda'), ('reviewed', 'Ditinjau'), ('published', 'Terbit'), ('returned', 'Dikembalikan'), ('rejected', 'Ditolak'), ('draft', 'Konsep')], default='draft', max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('response_count', models.IntegerField(blank=True, editable=False, null=True)),
                ('vote_up_count', models.IntegerField(blank=True, editable=False, null=True)),
                ('vote_down_count', models.IntegerField(blank=True, editable=False, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='topics', to='debate.Category')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='topics', to='person.Person')),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
                'db_table': 'debate_topic',
                'abstract': False,
                'unique_together': {('label', 'creator')},
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('label', models.CharField(blank=True, max_length=355, null=True)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('vote_up_count', models.IntegerField(blank=True, editable=False, null=True)),
                ('vote_down_count', models.IntegerField(blank=True, editable=False, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responses', to='person.Person')),
                ('response_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responses', to='debate.Response')),
                ('topic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responses', to='debate.Topic')),
            ],
            options={
                'verbose_name': 'Response',
                'verbose_name_plural': 'Responses',
                'db_table': 'debate_response',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Discussed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discusseds', to='debate.Topic')),
            ],
            options={
                'verbose_name': 'Discussed',
                'verbose_name_plural': 'Discusseds',
                'db_table': 'debate_discussed',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('value_image', models.ImageField(blank=True, max_length=500, null=True, upload_to=apps.debate.utils.files.directory_image_path)),
                ('value_file', models.FileField(blank=True, max_length=500, null=True, upload_to=apps.debate.utils.files.directory_file_path)),
                ('featured', models.BooleanField(null=True)),
                ('caption', models.TextField(blank=True, max_length=500, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(limit_choices_to=models.Q(app_label='debate'), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attachments', to='person.Person')),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachments',
                'db_table': 'debate_attachment',
                'ordering': ('-date_updated',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(choices=[('U', 'Up Vote'), ('D', 'Down Vote')], max_length=1)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(limit_choices_to=models.Q(app_label='debate'), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='votes', to='person.Person')),
            ],
            options={
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
                'db_table': 'debate_vote',
                'abstract': False,
                'unique_together': {('object_id', 'creator')},
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('label', models.CharField(max_length=255)),
                ('slug', models.SlugField(editable=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(limit_choices_to=models.Q(app_label='debate'), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tags', to='person.Person')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'db_table': 'debate_tag',
                'abstract': False,
                'unique_together': {('label',)},
            },
        ),
    ]
