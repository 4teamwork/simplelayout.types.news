from zope import schema
from zope.formlib import form
from plone.app.portlets.portlets import base
from collective.portlet.collectionmultiview.collectionmultiview import (
    ICollectionMultiView,
    Assignment as base_assignment,
    Renderer as base_renderer)
from collective.portlet.collectionmultiview.i18n import messageFactory as _
from zope.interface import implements


class INewsPortlet(ICollectionMultiView):

    # Override target_collection, its now filled with types
    target_collection = schema.List(
        title=_(u"Types"),
        description=_(u"Types to list"),
        required=True,
        value_type=schema.TextLine())


class Assignment(base_assignment):
    """
    """
    implements(INewsPortlet)


class Renderer(base_renderer):
    """
    """

    @property
    def collection_url(self):
        # Since we don't have any collection return absolute_url
        return self.context.absolute_url()

    def results(self):
        results = self.collection()
        limit = self.data.limit
        if limit and limit > 0:
            return results[:limit]
        return results

    def collection(self):
        query = {}
        types = self.data.target_collection
        if types:
            query['portal_type'] = types

        query['path'] = '/'.join(self.context.getPhysicalPath())
        query['sort_on'] = 'effective'
        query['sort_order'] = 'reverse'
        return self.context.portal_catalog(**query)

    @property
    def available(self):
        return bool(self.results())

    def update(self):
        super(Renderer, self).update()
        self.data.random = False
        self.data.show_more = False
        self.data.show_dates = False


class AddForm(base.AddForm):
    """
    """
    form_fields = form.Fields(INewsPortlet)
    form_fields = form_fields.omit('random', 'show_more', 'show_dates')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """
    """
    form_fields = form.Fields(INewsPortlet)
    form_fields = form_fields.omit('random', 'show_more', 'show_dates')
