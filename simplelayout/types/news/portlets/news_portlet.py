from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from simplelayout.types.news import _
from plone.formwidget.contenttree import PathSourceBinder
from z3c.form import form, button, field, interfaces
from plone.app.portlets.browser.interfaces import IPortletAddForm
from plone.app.portlets.browser.interfaces import IPortletEditForm
from plone.app.portlets.interfaces import IPortletPermissionChecker
from plone.app.portlets.portlets import base
from Acquisition import aq_parent, aq_inner
from zope.interface import implements
from plone.formwidget.contenttree import MultiContentTreeFieldWidget
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

class INewsPortlet(IPortletDataProvider):

    portlet_title = schema.TextLine(
        title=_(u'Title'),
        description=u'',
        required=True,
        default=u'')

    show_image = schema.Bool(title=_(u'label_show_image'),
        required=True,
        default=True)

    path = schema.List(
        title=_(u"Path"),
        description=u"",
        value_type=schema.Choice(
            title=_(u"xx"),
            source=PathSourceBinder(
                navigation_tree_query={
                    'is_folderish': True},
                is_folderish=True),
            ),
        required=False,
        )

    only_context = schema.Bool(title=_(u'label_only_context'),
                               description=_('help_only_context'),
                               default=True,
                               )

    classification_items = schema.List(
        title=_(u"Classification Items"),
        description=u"",
        value_type=schema.Choice(
            title=_(u"xx"),
            source=PathSourceBinder(
                navigation_tree_query={
                    'portal_type': 'ClassificationItem'},
                portal_type='ClassificationItem'),
            ),
        required=False,
        )

    quantity = schema.Int(title=_(u'label_quantity'),
                          default=5)

    subjects = schema.List(
        title=_(u'label_subjects'),
        description=_(u'help_subjects'),
            value_type = schema.Choice(
                title=_("xx"),
                vocabulary='simplelayout.types.news.subjects',

            )
       )



class AddForm(form.AddForm):
    implements(IPortletAddForm)
    label=_(u'Add News Portlet')
    description = _(u'This Portlet displays News')

    fields = field.Fields(INewsPortlet)

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(AddForm, self).__call__()

    def nextURL(self):
        editview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(editview))
        url = str(getMultiAdapter((context, self.request),
                                  name=u"absolute_url"))
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_(u"label_save", default=u"Save"), name='add')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True

    @button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"),
                             name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(nextURL)
        return ''

    def add(self, object):
        ob = self.context.add(object)
        self._finishedAdd = True
        return ob

    def updateWidgets(self):
        self.fields['classification_items'].widgetFactory = MultiContentTreeFieldWidget
        self.fields['path'].widgetFactory = MultiContentTreeFieldWidget
        #self.fields['subjects'].widgetFactory = atapi.MultiSelectionWidget
        if not self.context.portal_types.get('ClassificationItem', None):
            self.fields['classification_items'].mode = interfaces.HIDDEN_MODE
        super(AddForm, self).updateWidgets()



    def create(self, data):
        return Assignment(
            portlet_title = data.get('portlet_title', 'News'),
            show_image = data.get('show_image', True),
            only_context = data.get('only_context', True),
            quantity = data.get('quantity', 5),
            classification_items = data.get('classification_items', []),
            path = data.get('path', []),
            subjects = data.get('subjects', []),
            )

class Assignment(base.Assignment):
    implements(INewsPortlet)

    def __init__(self, portlet_title="News", show_image=True, only_context=True, quantity=5, classification_items=[],
                 path=[], subjects=[]):
        self.portlet_title = portlet_title
        self.show_image = show_image
        self.only_context = only_context
        self.quantity = quantity
        self.classification_items = classification_items
        self.path = path
        self.subjects = subjects

    @property
    def title(self):
        return u'News Portlet'

class Renderer(base.Renderer):
    render = ViewPageTemplateFile('news_portlet.pt')


    def tag_image(self, brain):
        if not self.data.show_image:
            return ''
        obj = self.context.restrictedTraverse(brain.getPath())
        scale = getMultiAdapter((obj, self.request), name=u"images")
        scaled_img = scale.scale('image', scale='thumb', direction='down')
        if scaled_img:
            return scaled_img.tag()
        return ''

    def get_news(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        url_tool = getToolByName(self.context, 'portal_url')
        portal_path = url_tool.getPortalPath()
        query = {'portal_type': 'News'}
        if self.data.only_context:
            path = '/'.join(self.context.getPhysicalPath())
            query['path'] = {'query': path}
        else:
            if self.data.path:
                cat_path = []
                for index,item in enumerate(self.data.path):
                    cat_path.append('/'.join([portal_path, item]))
                query['path'] = {'query': cat_path}
        if self.data.classification_items:
            cs_uids = []
            for item in self.data.classification_items:
                obj = self.context.restrictedTraverse('/'.join([portal_path, item.strip('/')]))
                cs_uids.append(obj.UID())
            query['cs_uids'] = cs_uids
        if self.data.subjects:
            query['Subject'] = self.data.subjects

        query['sort_on'] = 'effective'
        query['sort_order'] = 'descending'
        results = catalog.searchResults(query)
        return results[0:self.data.quantity -1]


class EditForm(form.EditForm):
    implements(IPortletEditForm)
    label=_(u'Add News Portlet')
    description = _(u'This Portlet displays News')

    fields = field.Fields(INewsPortlet)

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(EditForm, self).__call__()

    def nextURL(self):
        editview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(editview))
        url = str(getMultiAdapter((context, self.request),
                                  name=u"absolute_url"))
        return url + '/@@manage-portlets'


    @button.buttonAndHandler(_(u"label_save", default=u"Save"), name='apply')
    def handleSave(self, action):
       data, errors = self.extractData()
       if errors:
           self.status = self.formErrorsMessage
           return
       changes = self.applyChanges(data)
       if changes:
           self.status = "Changes saved"
       else:
           self.status = "No changes"

       nextURL = self.nextURL()
       if nextURL:
           self.request.response.redirect(nextURL)
       return ''

    @button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"),
                             name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(nextURL)
        return ''

    def updateWidgets(self):
        self.fields['classification_items'].widgetFactory = MultiContentTreeFieldWidget
        self.fields['path'].widgetFactory = MultiContentTreeFieldWidget
        if not self.context.portal_types.get('ClassificationItem', None):
            self.fields['classification_items'].mode = interfaces.HIDDEN_MODE

        super(EditForm, self).updateWidgets()
