from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import Tag, TaggedItem, TaggedItemBase

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        context = super().get_context(request)
        q = self.get_children().live().order_by('-first_published_at')
        tag = request.GET.get('tag',None)
        if tag:
            q = q.filter(tags__name=tag)
        context['blogpages'] = q.all()
        q = Tag.objects.all().annotate(count=Count("%s_items" % BlogPageTag._meta.db_table))
        context['nav_tags'] = q.all()
        return context

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

class BlogTagIndexPage(RoutablePageMixin,Page):
    def get_context(self, request,*args,**kwargs):
        q = BlogPage.objects.all()
        context = super().get_context(request)
        if 'tag' in kwargs:
            q = q.filter(tags__name=kwargs['tag'])
            context['tag'] = kwargs['tag']
        context['blogpages'] = q.all()
        return context

    @route(r'^$')
    def index(self, request, *args, **kwargs):
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^(?P<tag>[\w-]+)')
    def tag(self, request,tag, *args, **kwargs):
        kwargs["tag"] = tag
        return Page.serve(self, request, *args, **kwargs)
