import argparse
import json
import os
from CSIS_scraper import yield_latest_allnews
from CSIS_scraper import strf_to_datetime
from CSIS_scraper import news_dateformat


def save(json_obj, directory):
    url = json_obj['url']
    title = [p for p in url.split('/') if p][-1:] # this site`s url don`t contain category
    dt = strf_to_datetime(json_obj['time'], news_dateformat)
    name = '{}-{}-{}_{}'.format(dt.year, dt.month, dt.day, title[:50])
    filepath = '{}/{}.json'.format(directory, name)
    with open(filepath, 'w', encoding='utf-8') as fp:
        json.dump(json_obj, fp, indent=2, ensure_ascii=False)

def scraping(begin_date, max_num, sleep, directory, verbose):

    n_exceptions = 0
    for i, json_obj in enumerate(yield_latest_allnews(begin_date, max_num, sleep)):
        try:
            save(json_obj, directory)
        except Exception as e:
            n_exceptions += 1
            print(e)
            continue

        if verbose:
            title = json_obj['title']
            time = json_obj['time']
            print('[{} / {}] ({}) {}'.format(i+1, max_num, time, title))

    if n_exceptions > 0:
        print('Exist %d exceptions' % n_exceptions)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--begin_date', type=str, default='2019-01-10', help='datetime YYYY-mm-dd')
    parser.add_argument('--directory', type=str, default='./output/', help='Output directory')
    parser.add_argument('--max_num', type=int, default=100, help='Maximum number of news to be scraped')
    parser.add_argument('--sleep', type=float, default=1.0, help='Sleep time for each news')
    parser.add_argument('--verbose', dest='VERBOSE', action='store_true')

    args = parser.parse_args()
    begin_date = args.begin_date
    directory = args.directory
    max_num = args.max_num
    sleep = args.sleep
    VERBOSE = args.VERBOSE

    # check output directory
    if not os.path.exists(directory):
        os.makedirs(directory)

    scraping(begin_date, max_num, sleep, directory, VERBOSE)

if __name__ == '__main__':
    main()
