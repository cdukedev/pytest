import requests
from bs4 import BeautifulSoup
import re

# Fetch the web page
url = "https://www.ratemyprofessors.com/professor/2436180"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the ul containing all reviews
reviews_ul = soup.find('ul', {'id': 'ratingsList'})

# Initialize an empty list to hold review objects
reviews_list = []

# Loop through each li (review) in the ul
if reviews_ul:  # Check if reviews_ul is not None
    for li in reviews_ul.find_all('li'):
        review_object = {}
        
        # Locate the parent div with the regex class pattern
        parent_div = li.find('div', class_=re.compile('Rating__RatingInfo'))
        
        course_elem = li.find('div', class_=re.compile('RatingHeader__StyledClass'))
        if course_elem:
            review_object['courseNumber'] = course_elem.text
            
        quality_elem = li.find('div', class_=re.compile('CardNumRating__CardNumRatingNumber'))
        if quality_elem:
            review_object['Quality'] = quality_elem.text
            
        difficulty_elem = li.find('div', class_=re.compile('CardNumRating__CardNumRatingNumber'))
        if difficulty_elem:
            review_object['Difficulty'] = difficulty_elem.text
            
        # Using CSS selector to find the review comment directly
        comment_elem_by_selector = li.select_one('div > div > div.Rating__RatingInfo-sc-1rhvpxz-3.kEVEoU > div.Comments__StyledComments-dzzyvm-0.gRjWel')
        
        # Update the review_object dictionary if the comment element is found
        if comment_elem_by_selector:
            review_object['Review'] = comment_elem_by_selector.text.strip()
        
        # Append the review_object to the reviews_list
        reviews_list.append(review_object)

# Display the list of review objects
for review in reviews_list:
    print(review)
