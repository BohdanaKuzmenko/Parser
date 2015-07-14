import requests
from lxml import html
from StringIO import StringIO
from bs4 import BeautifulSoup
import urllib
import Image


class Parser(object):

    def get_pictures(self,url):
        f = urllib.urlopen(url)
        page = f.read()
        f.close()
        images = []
        soup = BeautifulSoup(page)
        for link in soup.findAll('img'):
            images.append(link.get('src'))
        return images

    def download_image(self, name, url):
        r = requests.get(url)
        i = Image.open(StringIO(r.content))
        i.save(name+'.jpg')

    def make_request(self):
        page_number = 0
        self.pages = 1
        while page_number < self.pages:
            page_number+=1
            url = 'http://www.realestate.co.nz/residential/search/page'+str(page_number)
            page_content = requests.get(url)
            root = html.fromstring(page_content.content)
            if(page_number == 1):
                self.pages = int([page.text_content() for page in root.xpath('//*[@id="leftCol"]/ul/li[5]')][0])

            names = []
            address = []
            detail_info = []
            details = []
            ids = [id.get('id') for id in root.xpath("//div[@class = 'listing featuredListing']")]
            image_urls = self.get_pictures(url)

            for i in ids:
                names.append([name.text_content() for name in root.xpath("//*[@id='%s']/div[4]/div[1]/h3/a" % i)][0])
                address.append([' '.join(adr.text_content().split()) for adr in root.xpath("//*[@id='%s']/div[4]/div[1]/div[1]" % i)][0])
                detail_info.append([det.text_content().split() for det in root.xpath("//*[@id='%s']/div[4]/div[2]" % i)][0])
                image_url = [im_url for im_url in image_urls if  i.split('-')[1] in im_url][0]
                self.download_image(i, image_url)


            for det in detail_info:
                try:
                    details.append({det[i+1]: det[i] for i in range(0, len(det), 2)})
                except:
                    pass

            parsed_response = zip(names, address, details)

            for i in parsed_response:
                print(i)


parser = Parser()
parser.make_request()
