
# coding: utf-8

# In[2]:


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


# In[3]:


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


# In[4]:


# Run the Chrome Driver
driver = webdriver.Chrome(executable_path=r'Dropbox/Academic/Courses/Term # 4/Web Analytics/chromedriver')


# In[5]:


# Let's go the main page of Amazon website
driver.get('http://www.amazon.com')
#We can get access the full page source with this line of code
"""
driver.page_source
"""


# In[6]:


# Let's find the search field and click on it to make it ready to type on
delay(4)
search_field = driver.find_element_by_id('twotabsearchtextbox')
search_field.click()
# READ MORE: http://selenium-python.readthedocs.io/locating-elements.html


# In[7]:


# Here we feed the keyword in search field
delay(3)
search_field.send_keys('Edifier H650 Hi-Fi On-Ear Headphones - Noise-isolating Foldable and Lightweight Headphone - Fit Adults and Kids - Blue')
delay(3)
search_field.send_keys(Keys.ENTER)
#inputElement.submit() 


# In[8]:


# an important point to manage class names containing space
# we need to substitute spaces with periods
# Here we get all the items showed in the first respose page
# At the moment we just sweep the items at the first page
search_items_links = driver.find_elements_by_css_selector(".a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal")
items_names = [ link.text for link in search_items_links]
def gen(whatever):
    for i in whatever:
        yield i
item_generator = gen(items_names)


# A point about feeding the driver with keyboard keys:
# 
# Some of the typical commands are:
# 
# Command+w :close the tab 
# 
# Command+tab: go to next tab
# 
# Command+return: open the link in the new window

# In[9]:


"""now we are ready to get reviews, but first we should click on the items one-by-one"""
main_window = driver.current_window_handle
driver.switch_to_window(main_window)
all_items_reviews = {}
for item in search_items_links[0:1]:
    #item_name = item.text
    #send_keys(Keys.COMMAND + Keys.RETURN) in order to open the links in the page
    # Remember each item is a link to the page for each product
    delay(5)
    item.send_keys(Keys.COMMAND + Keys.RETURN) 
    
    # Switch tab to the new tab, on the right
    delay(4) 
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)    
    # It is not enough. We need to put focus on the current visible tab
    driver.switch_to_window(driver.window_handles[1])
       
    # Now, we are interested to see all the reviews for the product, the following commands do this 
    delay(5)
    see_all = driver.find_element_by_css_selector(".a-link-emphasis.a-text-bold")
    see_all.click()
    # We have multiple pages of reviews each contain almost 10~20 reviews
    # We need to sweep all of those pages
    product_name = next(item_generator)
    print("Product Name: {}".format(product_name))
    all_items_reviews.update({product_name: []}) #Let's work for one review at the moment
    while ( True ):

        # First let's find the list of links to the classes containing the reviews' text
        review_links = driver.find_elements_by_css_selector(".a-size-base.review-text")
        
        # And add them to the list of all the reviews
        all_items_reviews[product_name] += [review_link.text for review_link in review_links]    
        # although we can click on the link to the other pages. 
        """
        other_pages = driver.find_elements_by_class_name("page-button")
        print([t.text for t in other_pages])
        """


        #print the selected button
        current_page = driver.find_element_by_css_selector(".a-selected.page-button")
        print("The reviews on page {} successfully extraced".format(current_page.text))

        # we prefer to use the Next→ button
        next_page = driver.find_element_by_class_name("a-last")
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
            print("All the reviews extracted successfully ")
            break
        delay(10)
        next_page.click()
        delay(5)
    # We extracted all the reviews from this page. Let's close the current tab    
    delay(4)    
    driver.close()
    # And remember to put driver focus on current window which will be the window opener
    driver.switch_to_window(main_window)
    driver.close()


# In[17]:


import pandas as pd
df = pd.DataFrame.from_dict(all_items_reviews, orient='columns', dtype=None)
df.to_csv('{}.csv'.format(list(all_items_reviews.keys())[0]))


# In[ ]:


"""I skip this part since the output format should be in csv"""
"""
#saving reviews
import pickle

with open('all_items_reviews.pickle', 'wb') as handle:
    pickle.dump(all_items_reviews, handle, protocol=pickle.HIGHEST_PROTOCOL)

# To test everything done correctly
with open('all_items_reviews.pickle', 'rb') as handle:
    reviews = pickle.load(handle)
#reviews
"""

