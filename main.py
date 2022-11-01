import requests
from bs4 import BeautifulSoup
import pandas as pd

HOME_URL = 'https://books.toscrape.com/catalogue/category/books_1/'

def scrape(url):
    '''scrape function'''
    print('scraping: ' + url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    results = []
    for item in soup.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        item_result = {}
        item_result['title'] = item.find('h3').find('a')['title']
        item_result['stars'] = item.find('p', class_='star-rating')['class'][1]
        item_result['instock'] = item.find('p', class_='instock availability').get_text().strip()
        item_result['price'] = HOME_URL + item.find('p', class_='price_color').get_text()
        item_result['image_url'] = HOME_URL + item.find('img')['src']
        results.append(item_result)
    
    next_tag = soup.find('li', class_='next')
    if next_tag:
        next_url = HOME_URL + next_tag.find('a')['href']
        return results + scrape(next_url)

    return results


def save_to_csv(list_of_data):
    '''write list of dictionaries to csv'''
    df = pd.DataFrame(list_of_data)
    df.to_csv('result.csv')


def main():
    '''main function'''
    results = scrape(HOME_URL)
    save_to_csv(results)


if __name__ == '__main__':
    main()
    