from ftw.testing.layer import ComponentRegistryLayer


class ZCMLLayer(ComponentRegistryLayer):
    """Test layer loading the complete package ZCML.
    """

    def setUp(self):
        super(ZCMLLayer, self).setUp()
        import ftw.book.tests
        self.load_zcml_file('test.zcml', simplelayout.type.tests)


ZCML_LAYER = ZCMLLayer()
