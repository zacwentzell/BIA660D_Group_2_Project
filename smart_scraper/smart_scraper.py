
# coding: utf-8

# In[247]:

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
#select works to select from an item
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
import pandas as pd
import pickle
import re


# In[248]:

#To simulate the delay
import random
import time
start_time = time.time()
normal_delay = random.normalvariate(2, 0.5)
time.sleep(normal_delay)    
print("--- %.5f seconds ---" % (time.time() - start_time))

def delay(t):
    normal_delay = random.normalvariate(t, 0.5)
    time.sleep(normal_delay)


# In[249]:

# Run the Chrome Driver
#driver = webdriver.Chrome(executable_path=r'Dropbox/Academic/Courses/Term # 4/Web Analytics/chromedriver')
driver = webdriver.Chrome(executable_path=r"/Users/pouria/Dropbox/chromedriver")
#r"C:\Chrome\chromedriver.exe"

# In[250]:

# Let's go the main page of Amazon website
driver.get('http://www.amazon.com')
#We can get access the full page source with this line of code
"""
driver.page_source
"""


# In[251]:

# Let's find the search field and click on it to make it ready to type on
delay(4)
search_field = driver.find_element_by_id('twotabsearchtextbox')
search_field.click()
search_field.send_keys('Headphones')
delay(3)
search_field.send_keys(Keys.ENTER)
# READ MORE: http://selenium-python.readthedocs.io/locating-elements.html


# In[252]:

# Finding the list of all brands
"""
left_nav_container = driver.find_elements_by_xpath(".//span[contains(@class, 'a-label a-checkbox-label')]") 

Brands = [y.text for y in left_nav_container]
Brands = ["RESET"] + Brands
Brands = [x for x in Brands if len(x)> 0]

first_index = left_nav_container_words.index("Brand")

Feature_index = [i for i in range(len(left_nav_container_words)) if left_nav_container_words[i] == "Feature"]
for index in Feature_index:
    if left_nav_container_words[index-1]=="Headphone":
        left_nav_container_words[index-1:index] = [' '.join(left_nav_container_words[index-1:index+1])]
last_index = left_nav_container_words.index("Headphone Feature")
Brands = left_nav_container_words[first_index+1:last_index]
"""


# In[ ]:




# In[262]:

intended_checkboxes = ['Sony', 'Wireless']
print(intended_checkboxes)


# In[255]:

for ccc in intended_checkboxes:
    string = ".//input[contains(@name, '{}')]".format(ccc)
    print(string)
    driver.find_element_by_xpath(string ).click() # and @type='checkbox']
    delay(3)


# In[256]:

#Review scraper function, we use this fu

def scrape_reviews(item,product_name):
    #item_name = item.text
    #send_keys(Keys.COMMAND + Keys.RETURN) in order to open the links in the page
    # Remember each item is a link to the page for each product
    main_window = driver.current_window_handle
    delay(5)
    item.send_keys(Keys.COMMAND + Keys.RETURN) 
    
    # Switch tab to the new tab, on the right
    delay(4) 
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)    
    # It is not enough. We need to put focus on the current visible tab
    driver.switch_to_window(driver.window_handles[1])
    # We need to get ASIN of the product: a unique code for each product on Amazon website
    try:
        Product_information_table = driver.find_element_by_id("productDetails_detailBullets_sections1")
    except:
        Product_information_table = driver.find_element_by_id("detail-bullets")
    
    Product_information = Product_information_table.text.split()
    Cleaned_product_information = [re.sub(':','', x) for x in Product_information]
    ASIN_index = Cleaned_product_information.index('ASIN')
    product_ID = Cleaned_product_information[ASIN_index+1]
    print("Product ID: {}".format(product_ID))
    # Now, we are interested to see all the reviews for the product, the following commands do this 
    delay(5)

    # We have multiple pages of reviews each contain almost 10~20 reviews
    # We need to sweep all of those pages
    

    all_reviews = {"Name":product_name, "ID": product_ID, "reviews": []} 
    #we have a few products without any reviews, let's skip them
    try:
        see_all = driver.find_element_by_css_selector(".a-link-emphasis.a-text-bold")
        see_all.click()
    except:
        return product_ID, all_reviews

    while ( True ):

        # First, let's find the list of links to the classes containing the reviews' text
        title_links = driver.find_elements_by_css_selector(".a-size-base.a-link-normal.review-title.a-color-base.a-text-bold")
        date_links = driver.find_elements_by_css_selector(".a-size-base.a-color-secondary.review-date")
        review_links = driver.find_elements_by_css_selector(".a-size-base.review-text")
        rating_links = driver.find_elements_by_xpath(".//a[contains(@title,  'out of 5 stars')]")
        comment_links = driver.find_elements_by_xpath("//*[contains(text(), 'Was this review helpful to you?')]")
        # And add them to the list of all the reviews
        titles = [title_link.text for title_link in title_links]
        dates = [date_link.text for date_link in date_links]
        ratings = [rating_link.get_attribute("title") for rating_link in rating_links]
        reviews = [review_link.text for review_link in review_links]
        comments = [comment_link.text for comment_link in comment_links]
        compact_reviews = zip(titles, dates, ratings, reviews, comments)
        all_reviews["reviews"] += compact_reviews
        # although we can click on the link to the other pages. 
        """
        other_pages = driver.find_elements_by_class_name("page-button")
        print([t.text for t in other_pages])
        """

        #print the selected button
        current_page = driver.find_element_by_css_selector(".a-selected.page-button")
        print("The reviews on page {} successfully extraced".format(current_page.text))

        # we prefer to use the Next→ button
        try:
            next_page = driver.find_element_by_class_name("a-last")
        except:
            next_page = None
            
        
        #We can also use the link text to find the intended links
        
        """
        print(driver.find_element_by_link_text('2').text)
        """
        # We continue the sweeping the review pages until getting to the last page
        
        try:
            is_last_page = driver.find_element_by_css_selector(".a-disabled.a-last")
        except:
            is_last_page = None
            
        if (is_last_page != None):
            print("All the reviews extracted successfully")
            print("-------------------------------------------------")
            break
        delay(10)
        next_page.click()
        delay(5)
    # We extracted all the reviews from this page. Let's close the current tab    
    delay(4)    
    driver.close()
    # And remember to put driver focus on current window which will be the window opener
    driver.switch_to_window(main_window)
    #driver.close()
    return product_ID, all_reviews


# In[257]:

def gen(whatever):
    for i in whatever:
        yield i


# In[258]:

#Now we selected the intended list of products and want to sweep the list of shown product
"""now we are ready to get reviews, but first we should click on the items one-by-one"""
main_window = driver.current_window_handle
driver.switch_to_window(main_window)

items_names = []

try:
    with open('successfully_scraped_products.pickle', 'rb') as handle:
        scraped_products = pickle.load(handle)
except:
    scraped_products = []
    with open('successfully_scraped_products.pickle', 'wb') as handle:
        pickle.dump([], handle, protocol=pickle.HIGHEST_PROTOCOL)


while(True):
    search_items_links = driver.find_elements_by_css_selector(".a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal")
    
    items_names += [ link.text for link in search_items_links]

    item_generator = gen(items_names)
    
    for item in search_items_links:
        product_name = next(item_generator)
        print("Product Name: {}".format(product_name))
        if product_name not in scraped_products:
            product_ID, all_reviews = scrape_reviews(item, product_name)        
            #df = pd.DataFrame.from_dict(all_reviews, orient='columns', dtype=None)
            #df.to_csv('{}.csv'.format(list(all_items_reviews.keys())[0]))
            #df.to_csv('{}.csv'.format(product_ID))
            with open('{}.pickle'.format(product_ID), 'wb') as fp:
                pickle.dump(all_reviews, fp)
            scraped_products += [product_name]
            with open('successfully_scraped_products.pickle', 'wb') as handle:
                pickle.dump(scraped_products, handle, protocol=pickle.HIGHEST_PROTOCOL)

    try:
        next_page = driver.find_element_by_class_name("pagnRA")
    except:
        next_page = None

        
    try:
        is_last_page = driver.find_element_by_css_selector("pagnRA1")
    except:
        is_last_page = None

    if (is_last_page != None or next_page == None):
        print("All the products' reviews extracted successfully")
        print("-------------------------------------------------")
        break
    next_page.click()
    delay(5)

# an important point to manage class names containing space
# we need to substitute spaces with periods
# Here we get all the items showed in the first respose page
# At the moment we just sweep the items at the first page




# A point about feeding the driver with keyboard keys:
# 
# Some of the typical commands are:
# 
# Command+w :close the tab 
# 
# Command+tab: go to next tab
# 
# Command+return: open the link in the new window

# In[27]:

# We can also use the represented text to find intended classes
"""
X = driver.find_elements_by_xpath("//*[contains(text(), '5.0 out of 5 stars')]")
"""

