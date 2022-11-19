

class TestSetup:
    def test_import(self):
        import pyinvest
        import pyinvest.crawler
        import pyinvest.crawler.eastmoney
        import pyinvest.strategy

    def test_version(self):
        import pyinvest
        # print(pyinvest.__version__)
        assert pyinvest.__version__ is not None
    

