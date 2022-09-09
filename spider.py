from dputils import scrape as sc
from bs4 import BeautifulSoup
import pandas as pd
from database import ReviewData
import os


def get_review_link(product_url=""):
    if 'amazon.com' in product_url:
        start_index = product_url.find('com/')+4
        stop_index = product_url.find('?')
        sub_url = product_url[start_index:stop_index]
        product_url_parts = sub_url.strip().split('/')
        # https://www.amazon.com/Amazon-Basics-Hydroclean-Water-Flosser/dp/B08N7GMGML?ref_=ast_sto_dp
        print(product_url_parts)
        # https://www.amazon.com/Utopia-Kitchen-Nonstick-Saucepan-Set/dp/B07NQJ4XM6/ref=sr_1_1?crid=NP5PQWOYI7XQ&keywords=pot&qid=1662698943&s=amazon-devices&sprefix=pot%2Camazon-devices%2C217&sr=1-1
        if len(product_url_parts) == 3:
            if product_url_parts[1] == 'dp':
                final_url = 'https://www.amazon.com/' + product_url_parts[0] + '/product-reviews/' + product_url_parts[2]
            else:
                final_url = 'https://www.amazon.com/product-reviews/' + product_url_parts[1]

        else: 
            final_url = 'https://www.amazon.com/' + product_url_parts[0] + '/product-reviews/' + product_url_parts[2]

        return final_url
    
    # try:
    #     soup = sc.get_webpage_data(product_url)
    #     review_link_area = sc.extract_one(soup, div={'tag':'div','attrs':{'id':'reviews-medley-footer'},'output':'object'})
    #     all_review_link = review_link_area['div'].find('a').get('href')
    #     return base_url + all_review_link
    # except Exception as e:
    #     print(e)
    #     return None

    
def collect_reviews(reviews_link=None, limit=-1, page = 1):
    if reviews_link is None:
        return None

    # review params
    target = {'tag':'div','attrs':{'id':'cm_cr-review_list'}} # the page subpart
    items= {'tag':'div','attrs':{'class':'a-section review aok-relative'}} # the repeating elements
    reviewer = {'tag':'span','attrs':{'class':'a-profile-name'}} # the name inside a single repeating element
    review = {'tag':'span','attrs':{'class':'a-size-base review-text review-text-content'}} # the review inside a single repeating element

    datalist = [] # final container for the data
    while True:
        if limit == 0:
            print(f"LOG: limit reached, limit is {limit}")
            break
        # print(type(reviews_link))
        review_link = reviews_link + '?pageNumber=' + str(page)
        print('=>>>',review_link)
        review_soup = sc.get_webpage_data(review_link)
        if review_soup == None:
            return None
        output =sc.extract_many(review_soup, target=target, items=items, reviewer=reviewer, content= review)
        if output is None:
            print("LOG: No more reviews, output is None")
            break
        elif len(output) == 0:
            print("LOG: No more reviews, output is empty")
            break
        else:
            datalist.extend(output)
            page += 1
            if limit > 0:
                limit -= 1
    return datalist

def save_reviews(datalist=None, filename='reviews.json', db=None):
    if datalist is None:
        return None
    if len(datalist)>0:
        if not os.path.exists('static/mined_data'):
            os.makedirs('static/mined_data')
        save_path = os.path.join('static/mined_data', filename)
        df = pd.DataFrame(datalist)
        df.to_json(save_path)
    return save_path

if __name__ == '__main__':
    product_url = 'https://www.amazon.com/dp/B0957LTZ6M/ref=cm_gf_abxk_iaac_d_p0_e0_qd0_gObwS1uwHE95fpRHhwqM'
    reviews_link = get_review_link(product_url)
    print(reviews_link)
    reviews = collect_reviews(reviews_link, limit=3)
    for review in reviews:
        print(review)
        print('-'*50)
    if len(reviews) > 0:
        path = save_reviews(reviews, filename='macbook.json')
    else:
        print('reviews empty')

    path =save_reviews(reviews, filename='macbook.json')
    print(f'LOG: {len(reviews)} reviews saved to {path}')

# from dputils import scrape as sc
# from bs4 import BeautifulSoup
# import pandas as pd
# import os

# def scraper(product_url="", base_url = 'https://www.amazon.com'):
#     try:
#         soup = sc.get_webpage_data(product_url)
#         review_link_area = sc.extract_one(soup, div={'tag':'div','attrs':{'id':'reviews-medley-footer'},'output':'object'})
#         all_review_link = review_link_area.find('a').get('href')
#         return base_url + all_review_link

#     except Exception as e:
#         print(e)
#         return

# # Save data into file/database
# def collect_reviews(review_link=None, page = 1, limit = -1):
#     if review_link is None:
#         return None

#     # Review parameters
#     target = {'tag':'div','attrs':{'id':'cm_cr-review_list'}} # the page subpart
#     items= {'tag':'div','attrs':{'class':'a-section review aok-relative'}} # the repeating elements
#     reviewer = {'tag':'span','attrs':{'class':'a-profile-name'}} # the name inside a single repeating element
#     review = {'tag':'span','attrs':{'class':'a-size-base review-text review-text-content'}} # the review inside a single repeating element

#     datalist = []
#     while True:
#         if limit == 0:
#             print(f"LOG: limit reached, limit is {limit}")
#             break
#         review_link = review_link + '&pageNumber=' + str(page)
#         print('=>>>',review_link)
#         review_soup = sc.get_webpage_data(review_link)
#         output =sc.extract_many(review_soup, target=target, items=items, reviewer=reviewer, content= review)
#         if output is None:
#             print("LOG: No more reviews, output is None")
#             break
#         elif len(output) == 0:
#             print("LOG: No more reviews, output is empty")
#             break
#         else:
#             datalist.extend(output)
#             page += 1
#             if limit > 0:
#                 limit -= 1
#     return datalist

# def save_reviews(datalist = None, filename = 'reviews.json', db = None):
#     if datalist is None:
#         return
    
#     if len(datalist) > 0:
#         if not os.path.exists('static/mined_data'):
#             os.makedirs('static/mined_data')

#         save_path = os.path.join('static/mined_data', filename)
#         df = pd.DataFrame(datalist)
#         df.to_json(save_path)

#         return save_path

# if __name__ == '__main__':
#     product_url = 'https://www.amazon.com/Apple-MacBook-13-inch-256GB-Storage/dp/B08N5M7S6K/ref=sr_1_1?crid=3D2TWY8NWW02P&keywords=macbook&qid=1661143915&sprefix=macbook%2Caps%2C348&sr=8-1'
#     reviews_link = scraper(product_url)
#     print(reviews_link)
#     reviews = collect_reviews(reviews_link, limit=3)
#     for review in reviews:
#         print(review)
#         print('-'*50)
#     path =save_reviews(reviews, filename='macbook.json')
#     print(f'LOG: {len(reviews)} reviews saved to {path}')

#     # call scrapper function
#     # save result in database