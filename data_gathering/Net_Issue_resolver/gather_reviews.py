from selenium import webdriver

import time
import random
import pandas as pd
import csv
import glob
import re

normal_delay = random.normalvariate(3, 0.5)
normal_delay_2 = random.normalvariate(5, 0.5)

driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('https://www.amazon.com/Transmitter-Cigarette-Otium-S06-Bluetooth/product-reviews/B077HQ66J9/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')


def to_csv():
    path = r'../BIA660D_Group_2_Project/data_gathering' # use your path
    allFiles = glob.glob(path + "/*.csv")
    frame = pd.DataFrame()
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_,index_col=None, header=0)
        list_.append(df)
    return pd.concat(list_)


def extract_reviews(driver):
    product_link = driver.find_element_by_css_selector('#cm_cr-brdcmb > ul > li:nth-child(1) > span > a')
    title_links = driver.find_elements_by_css_selector(".a-size-base.a-link-normal.review-title.a-color-base.a-text-bold")
    date_links = driver.find_elements_by_css_selector(".a-size-base.a-color-secondary.review-date")
    review_links = driver.find_elements_by_css_selector(".a-size-base.review-text")
    rating_links = driver.find_elements_by_xpath(".//a[contains(@title,  'out of 5 stars')]")
    comment_links = driver.find_elements_by_xpath("//*[contains(text(), 'Was this review helpful to you?')]")

    product = product_link.text
    titles = [title_link.text for title_link in title_links]
    dates = [date_link.text.strip('on').replace(',','') for date_link in date_links]
    ratings = [rating_link.get_attribute("title") for rating_link in rating_links]
    reviews = [review_link.text for review_link in review_links]
    comments = [comment_link.text for comment_link in comment_links]

    del dates[0:2]

    return pd.DataFrame({'Product': product, 'Title': titles, 'Date': dates, 'Ratings': ratings, 'Reviews': reviews, 'Comments': comments})


df = extract_reviews(driver)
df.to_csv('0 test.csv')
for i in range(1,5):
    current_page = driver.find_element_by_css_selector(".a-selected.page-button")
    print("The reviews on page {} successfully extracted".format(current_page.text))

    next_page = driver.find_element_by_class_name("a-last")

    try:
        is_last_page = driver.find_element_by_css_selector(".a-disabled.a-last")
    except:
        is_last_page = None

    if is_last_page is not None:
        print("All the reviews extracted successfully ")
        break
    time.sleep(normal_delay)
    next_page.click()
    time.sleep(normal_delay_2)
    page_reviews = extract_reviews(driver)
    df = df.append(page_reviews)
    page_reviews.to_csv(str(i) + ' test.csv')
    time.sleep(normal_delay)


data_frame = to_csv()

product_link = driver.find_element_by_css_selector('#cm_cr-brdcmb > ul > li:nth-child(1) > span > a')
product_link.click()
try:
    Product_information_table = driver.find_element_by_id("productDetails_detailBullets_sections1")
except:
    Product_information_table = driver.find_element_by_id("detail-bullets")

Product_information = Product_information_table.text.split()
Cleaned_product_information = [re.sub(':', '', x) for x in Product_information]
ASIN_index = Cleaned_product_information.index('ASIN')
product_ID = Cleaned_product_information[ASIN_index + 1]

data_frame.to_csv('{}.csv'.format(product_ID))


