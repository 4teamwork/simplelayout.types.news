from ftw.testing import MockTestCase
from simplelayout.types.news.portlets.news_portlet import Assignment, Renderer
from mocker import MATCH
class TestNewsPortlet(MockTestCase):


    def test_onlycontext(self):

        def query_matcher(query):
            self.assertEqual(query['path']['query'], 'folder/file')
            return True


        context = self.mocker.mock()
        request = self.mocker.mock()
        view = self.mocker.mock()
        manager = self.mocker.mock()
        catalog = self.mocker.mock()
        url = self.mocker.mock()
        self.mock_tool(catalog, 'portal_catalog')
        self.mock_tool(url, 'portal_url')
        self.expect(url.getPortalPath()).result('/plone')
        self.expect(context.getPhysicalPath()).result(('folder', 'file'))
        self.expect(catalog.searchResults(MATCH(query_matcher))).count(1).result(['1', '2', '3', '4', '5'])
        self.replay()
        obj = Assignment(path=['/peter/hans'])
        renderer = Renderer(context, request, view, manager, obj)
        renderer.get_news()


    def test_path(self):

        def query_matcher(query):
            self.assertEqual(query['path']['query'], 'peter/hans')
            return True


        context = self.mocker.mock()
        request = self.mocker.mock()
        view = self.mocker.mock()
        manager = self.mocker.mock()
        catalog = self.mocker.mock()
        url = self.mocker.mock()
        self.mock_tool(catalog, 'portal_catalog')
        self.mock_tool(url, 'portal_url')
        self.expect(url.getPortalPath()).result('/plone')
        self.expect(context.getPhysicalPath()).result(('folder', 'file'))
        self.expect(catalog.searchResults(MATCH(query_matcher))).count(1).result(['1', '2', '3', '4', '5'])
        self.replay()
        obj = Assignment(path=['/peter/hans'], only_context=False)
        renderer = Renderer(context, request, view, manager, obj)
        renderer.get_news()
