# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    browser_2 = Browser("chrome", executable_path="chromedriver", headless=True)
    browser_3 = Browser("chrome", executable_path="chromedriver", headless=True)
    
    news_title, news_paragraph = mars_news(browser)
   
   # Run all scraping functions and store results in dictionary
    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": mars_facts(),
          "last_modified": dt.datetime.now(),
          "mars_hemis": mars_hemis(browser, browser_2, browser_3)
          }
    return data

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first <a> tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except (AttributeError):
        return None, None

    return news_title, news_p

# Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    # print('full image: ', full_image_elem)

    # Find more info button and click
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    # print('more info: ', more_info_elem)
    more_info_elem.click()

    # Parse resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # print('htm: ', html)

    try:
        # Find relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        # print('img_url_rel:', img_url_rel)

    except AttributeError:
        return None

    # Create absolute url with base url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    # print('img_url: ', img_url)
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
        # print("dot zero index")

    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def mars_hemis(browser, browser_2, browser_3):
    
        # url = 'http://127.0.0.1:5500/mars/index.html'
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        
        # Navigate to page
        browser.visit(url)

        #Ensure page is loaded
        browser.is_element_present_by_tag("a", wait_time=5)

        # Convert the browser html to a soup object
        html = browser.html
        html_soup = soup(html, 'html.parser')

        # Get anchors from overview page

        anchors = html_soup.find_all("a", class_="product-item")
#         print(anchors)
        
        dup_hrefs_1 = []
        # Get hrefs to second_page
        for a1_tag in anchors:
            hrefs_1 = a1_tag.get('href')
            dup_hrefs_1.append(hrefs_1)
#         print(dup_hrefs_1)
        
        # Get unique hrefs
        unique_hrefs_1 = []
        for dup_href in dup_hrefs_1:
            if dup_href not in unique_hrefs_1:
                unique_hrefs_1.append(dup_href)
#         print(unique_hrefs_1)

        # Create absolute urls to each hemisphere page
        unique_links_1 = []
        for unique_href in unique_hrefs_1:
            unique_links_1.append(f'https://astrogeology.usgs.gov{unique_href}')
#         print(unique_links_1)

        # Navigate to each URL and get hrefs
        
        # Visit unique_1 links and store html objects in html_2_objects
        html_2_objects = []
        for unique_link_1 in unique_links_1:
            browser_2.visit(unique_link_1)
            html_2 = browser_2.html
            html_2_objects.append(html_2)
#         print(len(html_2_objects))
        
        # Convert hmls_objects to soup
        sample_links = []
        titles = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']
        for html_2_object in html_2_objects:
            html_soup_2 = soup(html_2_object, 'html.parser')
#             print(len(html_2_soup_objects))
#             print(html_soup_2.find('div', class_='downloads').find('li').find('a').get('href'))
            # Get hrefs from soup objects
            sample_links.append((html_soup_2.find('div', class_='downloads').find('li').find('a').get('href')))
        
        dictionary_list = []
        for j, k in enumerate(sample_links):
            print(titles[j])
            dictionary_list.append({'title':titles[j], 'url': k})
#         print(dictionary_list)
        return dictionary_list

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())