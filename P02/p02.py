
import requests
from protego import Protego
from lxml import etree
import gzip
from io import BytesIO


def get_rp(robots_url):
    rp = requests.get(robots_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.119 Safari/537.36'})
    return Protego.parse(rp.text)
    pass

def my_hash(username):
    import hashlib
    m = hashlib.sha256()
    m.update(bytes(username, 'utf-8'))
    return int(m.hexdigest()[:16], 16)

def main():

    websites = [
    'addthis.com', 'ea.com', 'fandom.com', 'harvard.edu', 'jimdo.com',
    'lexpress.fr', 'mozilla.com', 'nih.gov', 'opera.com', 'plos.org',
    'sedo.com', 'thenai.org', 'translate.google.com', 'usnews.com',
    'whitehouse.gov', 'wp.com', 'wsj.com', 'www.google.com', 'zendesk.com',
    ]

    #this is 2.1

    username = 'boulethj'
    index = my_hash(username) % len(websites)
    url = websites[index]
    print(f'The website for user "{username}" is {url}')

    #this is 2.2
    rp_url = get_rp("https://mozilla.com/robots.txt")
    sitemaps = list(rp_url.sitemaps)
    print(sitemaps)
    print(type(sitemaps))
    count = len(sitemaps)
    type(sitemaps)

    f = open("mozilla.com.urls.txt", 'w')

    for x in sitemaps:

        response = requests.get(x, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.119 Safari/537.36'})
        root = etree.XML(bytes(response.text, 'utf-8'))

        print(root.tag)
        if ("sitemapindex" in root.tag):
            for child in root:
                for loc in child:
                    sitemaps.append(loc.text)
                    if "loc" in loc.tag:
                            print(loc.text)
        else:
            for child in root:
                for loc in child:
                    if "loc" in loc.tag:
                            print(loc.text)
                            f.write(loc.text + "\n")
    f.close()

    rp_gzip = get_rp('http://picasa.google.com/robots.txt')
    sitemaps = list(rp_gzip.sitemaps)
    print(sitemaps)
    print(type(sitemaps))
    count = len(sitemaps)
    type(sitemaps)

    b = open("picasa.google.com.urls.txt", 'w')

    for x in sitemaps:
        print(x)

        response = requests.get(x, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/109.0.5414.119 Safari/537.36'})
        if response.ok:
            try:
                with gzip.open(BytesIO(response.content), 'rb') as gz:
                    s = gz.read()

            except gzip.BadGzipFile as e:
                   s = response.content
            root = etree.XML(s)
            print(root.tag)
            if ("sitemapindex" in root.tag):
                for child in root:
                    for loc in child:
                        sitemaps.append(loc.text)
                        if "loc" in loc.tag:
                            print(loc.text)
            else:
                for child in root:
                    for loc in child:
                        if "loc" in loc.tag:
                            print(loc.text)
                            b.write(loc.text + "\n")
    b.close()
if __name__ == '__main__':
    main()


