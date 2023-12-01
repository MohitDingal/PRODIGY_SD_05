from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
def get_price(soup):
    # price = soup.find("div",id= 'corePriceDisplay_desktop_feature_div' ).find("div",class_ = 'a-section a-spacing-none aok-align-center aok-relative').find('span',class_ = 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay').find('span',class_ = "span.a-price-whole").get_text()
    price = soup.find('span',class_ = 'a-price-whole').get_text()

    return price


def get_rating(soup):
    rating = soup.find("span",attrs = {'class':'a-icon-alt'}).string.strip()
    return rating

def review_count(soup):
    count = soup.find("span",attrs = {'id':'acrCustomerReviewText'}).string.strip()
    return count
def get_name(soup):
    name = soup.find("span",attrs = {'id':'productTitle'}).string.strip()
    return name

if __name__ == '__main__':

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    url = "https://www.amazon.in/s?k=samsung&crid=J7HCS4BYW66Z&sprefix=samsung+%2Caps%2C188&ref=nb_sb_noss_2"
    webpage = requests.get(url,headers = headers)

    soup = BeautifulSoup(webpage.content,"html.parser")
    links = soup.find_all('a',attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    links_list = []
    for link in links:
        links_list.append(link.get('href'))

    d = {"Name":[],"price":[],"rating":[],"reviews":[]}

    for link in links_list:
        product_page = requests.get("https://www.amazon.in"+link,headers = headers)
        new_soup = BeautifulSoup(product_page.content,"html.parser")
        d["Name"].append(get_name(new_soup))
        d["price"].append(get_price(new_soup))
        d["rating"].append(get_rating(new_soup))
        d["reviews"].append(review_count(new_soup))

    final_op = pd.DataFrame.from_dict(d)
    final_op['Name'].replace('',np.nan,inplace=True)
    final_op = final_op.dropna(subset=['Name'])
    final_op.to_excel("SamsungPhoneScraped.xlsx",header = True,index = False)














