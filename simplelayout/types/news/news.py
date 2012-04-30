from DateTime import DateTime
from simplelayout.types.common.content.simplelayout_schemas import imageSchema
from simplelayout.types.common.content import page
from simplelayout.types.common.content.page import Page

from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from simplelayout.types.news.config import PROJECTNAME
from simplelayout.types.common.content.simplelayout_schemas import finalize_simplelayout_schema
from zope.interface import implements
from simplelayout.types.news.interfaces import INews
from simplelayout.base.interfaces import ISimpleLayoutCapable


news_schema = page.page_schema.copy() + imageSchema.copy()

news_schema['effectiveDate'].required = True
news_schema['effectiveDate'].default_method = 'getDefaultEffectiveDate'

finalize_simplelayout_schema(news_schema, folderish=True)

class News(Page):

    implements(INews, ISimpleLayoutCapable)
    security = ClassSecurityInfo()

    schema = news_schema

    def getDefaultEffectiveDate(self):
        return DateTime().Date()



atapi.registerType(News, PROJECTNAME)

