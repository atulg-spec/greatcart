# Generated by Django 5.1.5 on 2025-02-23 00:33

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_slider_is_mobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, help_text="The URL of the page (e.g., 'about-us'). Automatically generated from the title if not provided.", max_length=200, unique=True)),
                ('title', models.CharField(help_text="The title of the page (e.g., 'About Us'). This will appear in the browser tab and as the H1 tag.", max_length=200)),
                ('meta_description', models.CharField(blank=True, help_text='A brief description of the page for SEO purposes (160-300 characters recommended).', max_length=300)),
                ('meta_keywords', models.CharField(blank=True, help_text="Comma-separated keywords for SEO purposes (e.g., 'about us, company, history').", max_length=200)),
                ('content', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('canonical_url', models.URLField(blank=True, help_text="The canonical URL of the page (e.g., 'https://example.com/about-us').", max_length=500)),
                ('og_title', models.CharField(blank=True, help_text="The title of the page for social media sharing (e.g., 'About Us | Company Name').", max_length=200)),
                ('og_description', models.CharField(blank=True, help_text='The description of the page for social media sharing.', max_length=300)),
                ('og_image', models.URLField(blank=True, help_text='The URL of the image to display when the page is shared on social media.', max_length=500)),
                ('twitter_card', models.CharField(blank=True, help_text="The type of Twitter card to use (e.g., 'summary', 'summary_large_image').", max_length=50)),
                ('twitter_title', models.CharField(blank=True, help_text='The title of the page for Twitter sharing.', max_length=200)),
                ('twitter_description', models.CharField(blank=True, help_text='The description of the page for Twitter sharing.', max_length=300)),
                ('twitter_image', models.URLField(blank=True, help_text='The URL of the image to display when the page is shared on Twitter.', max_length=500)),
                ('structured_data', models.TextField(blank=True, help_text='JSON-LD structured data for rich snippets (e.g., FAQ, Article, Breadcrumb).')),
                ('robots_index', models.BooleanField(default=True, help_text='Whether search engines should index this page.')),
                ('robots_follow', models.BooleanField(default=True, help_text='Whether search engines should follow links on this page.')),
                ('is_published', models.BooleanField(default=True, help_text='Whether the page is published and visible on the site.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
                'ordering': ['title'],
            },
        ),
    ]
