# Import Dependencies for this module : Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=False)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_image_urls(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        
    except AttributeError:
        return None, None

    return news_title, news_p, featured_image

# ## JPL Space Images Featured Image

def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    try:
        # find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url

 ## Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def title_url(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    hemi_image = soup(html, 'html.parser')

    # Create a for loop find all div's matching the class "item" from hemi_image
    for item in hemi_image.find_all("div", class_="item"):
        
        #Create a dictionary to hold the hemisphere photos.
        hemispheres= {}
        
        #Get the thumbnail text from the heading 3 HTML tag
        thumb_nail = item.select_one('h3').get_text()
        
        # Find all href attributes for <a> tags with the class "itemLink product-item" 
        # and assign them to a variable.
        link = item.find('a', class_='itemLink product-item')['href']
        
        #Visit the link using Splinter
        browser.visit(f'https://astrogeology.usgs.gov{link}')
        
        # Get the html from the new link
        html = browser.html
        
        # Put the html into a beautiful soup
        mysoup = soup(html, 'html.parser')
        
        #Find all div tags with the parent class holding the img
        downloads_img = mysoup.find('div', class_='downloads')
        
        # Get the href attributes of the  image jpg
        img_url = downloads_img.find('a')['href']
        
        # Assign the values to our hemisphere dictionary.
        hemispheres['title']= thumb_nail
        hemispheres['url']= img_url
        
        #Append the dictionary to hisphere_image_urls
        hemisphere_image_urls.append(hemispheres)

    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
