from biofid.tests.base import BiofidLiveWebsiteTestCase


class TestWebsiteFunctionality(BiofidLiveWebsiteTestCase):
    urls = 'FidBioDjangoCMS.urls'

    def test_sitemap(self):
        self.selenium.get(self.create_test_url('/sitemap.xml'))
        self.assertTrue(self.selenium.find_element_by_tag_name('urlset'))

    def test_robots_txt(self):
        self.selenium.get(self.create_test_url('/robots.txt'))
        self.assertTrue('Disallow:' in self.selenium.page_source)

    def test_publications(self):
        self.selenium.get(self.create_test_url('/de/publications'))
        self.assertIn('Publikationen', self.selenium.title)

        self.selenium.get(self.create_test_url('/en/publications'))
        self.assertIn('Publications', self.selenium.title)


