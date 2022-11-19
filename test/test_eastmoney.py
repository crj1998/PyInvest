
import pyinvest

class TestAPI:
    def test_fund_list_page(self):
        from pyinvest.crawler.eastmoney import fund_list_page
        df = fund_list_page()
        # print()
        # print(df.head(5))
    
    def test_get_kline(self):
        from pyinvest.crawler.eastmoney import get_kline
        df = get_kline('1.000001', lastcount=100)
        assert len(df) == 100
        # print(df.head(5))