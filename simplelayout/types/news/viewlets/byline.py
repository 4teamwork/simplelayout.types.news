from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class NewsByline(ViewletBase):

    template = ViewPageTemplateFile('byline.pt')

    def render(self):
        return self.template()
