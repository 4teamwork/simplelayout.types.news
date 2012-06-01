from zope.publisher.browser import BrowserView
import DateTime
from Products.CMFCore.utils import getToolByName
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile


class NewsListing(BrowserView):

    template = ViewPageTemplateFile('newslisting.pt')
    template_rss = ViewPageTemplateFile('newslisting_rss.pt')
    result_template = ViewPageTemplateFile('news_result.pt')

    def __call__(self):
        if self.__name__ == 'news_rss_listing':
            return self.template_rss()
        return self.template()

    def get_today(self, plus=0, minus=0):
        date = DateTime.DateTime() + plus - minus
        return date.Date()

    def get_creator(self, item):
        memberid = item.Creator
        mt = getToolByName(self.context, 'portal_membership')
        member = mt.getMemberById(memberid)
        if member:
            return member
        return None

    def get_news(self):
        """Get all news items"""
        context = self.context
        ct = context.portal_type
        query = {}
        query['portal_type'] = 'News'
        query['sort_on'] = 'effective'
        query['sort_order'] = 'reverse'


        end = self.request.form.get('end', '')
        if end:
            end = DateTime.DateTime(end).Date()
        start = self.request.form.get('start', '')
        if start:
            start = DateTime.DateTime(start).Date()
            if end:
                query['effective'] = {'range': 'min:max',
                                      'query': (start, end)}
            else:
                query['effective'] = {'range': 'min', 'query': start}
        elif end:
            query['effective'] = {'range': 'max', 'query': end}
        else:
            query['effective'] = {'range': 'min:max',
                                  'query': (self.get_today(minus=30),
                                            self.get_today())}

        if ct == 'ContentPage':
            return context.getFolderContents(query)
        elif ct == 'Topic':
            return context.queryCatalog()
        else:
            return

    def has_img(self, news):
        return bool(news.getObject().getImage())

    def get_img(self, news):
        obj = news.getObject()
        scale = obj.restrictedTraverse('@@images')
        return scale.scale(
            'image',
            width=200,
            height=200).tag(**{'class': 'tileImage'})

    def news_result(self):
        """Returns Newslisting"""
        return self.result_template()
