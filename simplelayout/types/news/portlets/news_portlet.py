import random
from zope import schema
from zope.formlib import form
from plone.app.portlets.portlets import base
from collective.portlet.collectionmultiview.collectionmultiview import (
    ICollectionMultiView,
    Assignment as base_assignment,
    Renderer as base_renderer)
from collective.portlet.collectionmultiview.i18n import messageFactory as _
from plone.memoize.instance import memoize
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
        if self.data.random:
            return self._random_results()
        else:
            return self._standard_results()

    def _standard_results(self):
        results = self.collection()
        limit = self.data.limit
        if limit and limit > 0:
            return results[:limit]
        return results

    def _random_results(self):
        # intentionally non-memoized
        results = self.collection()
        limit = self.data.limit and min(len(results), self.data.limit) or 1
        if len(results) < limit:
            limit = len(results)
        return random.sample(results, limit)

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
    form_fields = form_fields.omit('random', 'show_dates')
