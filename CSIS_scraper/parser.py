from .utils import get_soup
from .utils import now

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
        title = soup.find('article', role= 'article').find('h1').text
        time = soup.find('article', role= 'article').find('p').text
        author = soup.find('div', class_='teaser__title').text
        phrases = soup.find_all('p')
        content = '\n'.join([p.text.strip() for p in phrases])

        json_object = {
            'title' : title,
            'time' : time,
            'author' : author,
            'content' : content,
            'url' : url,
            'scrap_time' : now()
        }
        return json_object
    except Exception as e:
        print(e)
        print('Parsing error from {}'.format(url))
        return None
