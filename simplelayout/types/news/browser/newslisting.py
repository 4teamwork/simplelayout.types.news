from zope.publisher.browser import BrowserView
import DateTime
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
import datetime
from Products.CMFPlone import PloneMessageFactory as _
import calendar
from zope.i18n import translate

class NewsListing(BrowserView):
    
    template = ViewPageTemplateFile('newslisting.pt')
    template_rss = ViewPageTemplateFile('newslisting_rss.pt')
    result_template = ViewPageTemplateFile('news_result.pt')
    
    def __call__(self):
        if self.__name__ == 'news_rss_listing':
            return self.template_rss()
        return self.template()
        
    def get_news(self):
        """Troll"""
        context = self.context
        request = self.request
        ct = context.portal_type
        query = {}
        query['portal_type'] = 'News'
        query['sort_on'] = 'effective'
        query['sort_order'] = 'reverse'
        
        if request.get('showmonth', ''):
            date = request.get('showmonth', '').split(';')
            month = int(date[0])
            year = int(date[1])
            firstday = datetime.date(year, month,1)
            monthrange = calendar.monthrange(year, month)[1]
            lastday = datetime.date(year, month, monthrange)
            query['effective'] = {'query':(lastday,firstday),'range':'min:max'}
        
        else:
            lastday = DateTime.DateTime()
            firstday = lastday - 28
            query['effective'] = {'query':(lastday,firstday),'range':'min:max'}
        if ct == 'ContentPage':
            return context.getFolderContents(query)
        elif ct == 'Collection':
            import pdb; pdb.set_trace( )
        else:
            return    
        
    def has_img(self, news):
        obj = news.getObject()
        if obj.getImage():
            return True
        else: 
            return False

    def get_img(self, news):
        obj = news.getObject()
        return obj.getField('image').tag(obj, scale='thumb', **{'class':'image-left'})
        
    def get_months_strings(self, month):
        date = month.split(';')
        monthstring = datetime.date(int(date[1]), int(date[0]), 1).strftime('month_%b').lower()
        monthstring = translate(monthstring, domain='plonelocales', context=self.request)
        return monthstring + ' ' + date[1]

    def get_months(self):
        context = self.context
        ct = context.portal_type

        if ct == 'ContentPage':
            news = context.getFolderContents({'portal_type':'News','sort_on':'effective','sort_order':'ascending',})
            Months = set()
            for newsitem in news:
                month = newsitem.effective.month()
                year = newsitem.effective.year()
                date = str(month) + ';' + str(year)
                Months.add(date)
            return Months
        elif ct == 'Collection':
            import pdb; pdb.set_trace( )
        else:
            return
            
    def news_result(self):
        """Returns Newslisting"""
        return self.result_template()
