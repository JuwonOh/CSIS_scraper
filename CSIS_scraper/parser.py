from .utils import get_soup
from .utils import now
from dateutil.parser import parse

def parse_author(soup):
    authors = [a.text.strip() for a in soup.select('a') if '/people/' in a.attrs.get('href', '')]
    authors = '' if not authors else ', '.join(authors)
    if not authors:
        return None
    return authors
def parse_title(soup):
    title = soup.find('article', role= 'article')
    if not title:
        return None
    return title.find('h1').text

def parse_date(soup):
    date = soup.find('article', role= 'article')
    if not date:
        return None
    sub_date = date.find('p')
    if not sub_date:
        return None
    return parse(sub_date.text)

def parse_content(soup):
    phrases = soup.find_all('p')
    if not phrases:
        return None
    content = '\n'.join([p.text.strip() for p in phrases])
    return content

def parse_page(url):
    """
    Argument
    --------
    url : str
        Web page url

    Returns
    -------
    json_object : dict
        JSON format web page contents
        It consists with
            title : article title
            time : article written time
            content : text with line separator \\n
            url : web page url
            scrap_time : scrapped time
    """
    try:
        soup = get_soup(url)
        json_object = {
            'title' : parse_title(soup),
            'time' : parse_date(soup),
            'author' : parse_author(soup),
            'content' : parse_content(soup),
            'url' : url,
            'scrap_time' : now()
        }
        return json_object

    except Exception as e:
        print(e)
        print('Parsing error from {}'.format(url))
        return None
