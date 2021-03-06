import re
import time
from dateutil.parser import parse
from .parser import parse_page
from .utils import get_soup

def is_matched(url):
    for pattern in patterns:
        if pattern.match(url):
            return True
    return False

def is_unmatched(url):
    for pattern in unpatterns:
        if pattern.match(url):
            return False
    return True

patterns = [
    re.compile('https://www.csis.org/analysis/[\w]+')]
unpatterns = [
    re.compile('https://www.csis.org/analysis/issues-insights-vol[\w]+'),
    re.compile('https://www.csis.org/analysis/pacnet[\w]+')]

url_base = 'https://www.csis.org/analysis/page%3D7?page={}/'

def yield_latest_allnews(begin_date, max_num=10, sleep=1.0):
    """
    Artuments
    ---------
    begin_date : str
        eg. 2018-01-01
    max_num : int
        Maximum number of news to be scraped
    sleep : float
        Sleep time. Default 1.0 sec

    It yields
    ---------
    news : json object
    """

    # prepare parameters
    d_begin = parse(begin_date)
    end_page = 100
    n_news = 0
    outdate = False

    for page in range(0, end_page+1):

        # check number of scraped news
        if n_news >= max_num or outdate:
            break

        # get urls
        links_all= []
        url = url_base.format(page)
        soup = get_soup(url)
        sub_links = soup.find_all('div', class_= 'node node--publication node--two-column-list view-mode-two_column_list clearfix')
        links = [i.find('div', class_= 'teaser__title').find('a')['href'] for i in sub_links]
        links_all += links
        links_all = ['https://www.csis.org' + i for i in links_all]
        links_all = [url for url in links_all if is_matched(url)]
        links_all = [url for url in links_all if is_unmatched(url)]

        # scrap
        for url in links_all:
            news_json = parse_page(url)
            try:
                # check date
                d_news = news_json['time']
                if d_begin > d_news:
                    outdate = True
                    print('Stop scrapping. {} / {} blog was scrapped'.format(n_news, max_num))
                    print('The oldest article has been created after {}'.format(begin_date))
                    break

                # yield
                yield news_json
            except Exception as e:
                print(e)
                print('Parsing error from {}'.format(url))
                return None

            # check number of scraped news
            n_news += 1
            if n_news >= max_num:
                break
            time.sleep(sleep)

def get_allnews_urls(begin_page=0, end_page=3, verbose=True):
    """
    Arguments
    ---------
    begin_page : int
        Default is 1
    end_page : int
        Default is 3
    verbose : Boolean
        If True, print current status

    Returns
    -------
    links_all : list of str
        List of urls
    """

    links_all = []
    for page in range(begin_page, end_page+1):
        url = url_base.format(page)
        soup = get_soup(url)
        sub_links = soup.find_all('div', class_= 'node node--publication node--two-column-list view-mode-two_column_list clearfix')
        links = [i.find('div', class_= 'teaser__title').find('a')['href'] for i in sub_links]
        links_all += links
        if verbose:
            print('get briefing statement urls {} / {}'.format(page, end_page))

    links_all = ['https://www.csis.org' + i for i in links_all]
    return links_all

def get_last_page_num():
    """
    Returns
    -------
    page : int
        Last page number.
        eg: 503 in 'https://www.csis.org/analysis?page=1254'
    """

    def is_last_link(link):
        return 'pager__link--last' in link.attrs['class']

    def parse(href):
        return int(href.split('page=')[-1])

    last_page = -1
    url = 'https://www.csis.org/analysis'
    soup = get_soup(url)
    for link in soup.select('a[class^=pager__link]'):
        if is_last_link(link):
            last_page = parse(link.attrs['href'])
    return last_page
