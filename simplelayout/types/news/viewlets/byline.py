from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class NewsByline(ViewletBase):

    template = ViewPageTemplateFile('byline.pt')

    def render(self):
        return self.template()

    def creator(self):
        userid = self.context.Creator()
        mt = getToolByName(self.context, 'portal_membership')
        member = mt.getMemberById(userid)
        if member:
            return member.getProperty('fullname') or userid
        return userid
