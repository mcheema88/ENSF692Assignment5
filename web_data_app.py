# web_data_app.py
# June 2025
# Modified by: Marley Cheemaa
#
# An simple program for demonstrating web applications using Flask and web scraping of data using Beautiful Soup.
# Detailed specifications are provided via the Assignment 5 README file.


import pandas as pd     # needed for data manipulation

from flask import Flask, render_template    # needed for web app

from bs4 import BeautifulSoup               # needed for web scraping
import requests

from datetime import datetime               # needed for time/regular expressions
import re


###
# Initialize our FLASK application object from the Flask class like so:
app = Flask(__name__)

@app.route("/")
def index():
    """
    Our first (topmost) route (aka 'view').  Routes are like URLs, 
    which we can access from a browser. The line immediately below is known as a 
    'decorator' and implements some boilerplate code for us without much work on 
    our end.  Basically it creates a 'view' to our app and data to show the user.
    This one merely shows a static message.  Easy-peasy.
    """
    return "Hello World!"


@app.route("/hello/<name>")
def hello_there(name):
    """
    This route shows a bit more of what we can do, including some 'REST'full user 
    interaction.  If a user specifies a name in the url like so: http://localhost:5000/hello/supercoder
    the response will include the value 'supercoder' in the `name` variable, and 
    can then be validated with the RE `match_object` output.  If an invalid value is specified
    for `name` the validator code will simply assign 'friend' value to the `clean_name`
    instead.  If no value is specified, it will error out and present a 404 error to the browser.
    """
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)
    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    # Output the semi-static text with the time and supplied name (if any)
    content = "Hello there, " + clean_name + "! Welcome to Assignment 5. It's " + formatted_now
    return content


@app.route("/data")
def book_data():
    """
    Now let's take what we learned about Pandas and scrap some data from the internet!
    """

    # Web scraping can be against the Terms of Use. 
    # Always check to make sure that you are web scraping legally and ethically.
    # The following site was specifically created to practice web scraping.
    source = requests.get("http://books.toscrape.com/")
    soup = BeautifulSoup(source.content, 'html.parser')     # Use BeautifulSoup to parse the website html code
    book_results = soup.find_all(attrs={'class':'product_pod'})  # By inspecting the site, we know books = product_pod class

    titles = []
    prices = []

    # For each book listed on the page, get the title and the price from inside in the html data
    for book in book_results:
        titles.append(book.h3.a.get('title'))
        prices.append(float(book.find('p', class_="price_color").text[1:]))

    # Create a DataFrame using the two lists
    book_data = pd.DataFrame(list(zip(titles, prices)), columns=['Titles','Prices'])    
    print(book_data)        # Print to the terminal as confirmation - only we can see this

    # This is a function that I added -> called salePrices which hold point is to take in a value and convert to a sale price outlining a 25 % discount
    # @param : This function takes in the original price
    # @return : It returns the original price and reduces it by 25%
    def salePrices(prices):
        salePrice = round(prices * 0.75, 2) #by multiplying the price by 0.75 this effectively applies a 25% discount -> also as currency is only 2 decimal points reflected in cents -> I applied round and set to 2 decimal point through the comma.
        return salePrice #returning the sale price
    
    book_data["Sale Price: Marley Cheema"] = book_data["Prices"].apply(salePrices) # this line of code is what creates the new column "Sale Price" and applies the function to the entire Prices column to generate values to populate the Sale Price column (Reference to ChatGPT for helping me with syntax for using .apply)

    # Format and print the DataFrame using the html template provided in the templates subdirectory
    return render_template('template.html',  tables=[book_data.to_html(classes='data')], titles=book_data.columns.values)

@app.route("/learn")
def learn():

    #All I had to do here was add my statement to a String variable -> dynamically created in python of one thing I learned in this course
    learning = "Through ENSF 692, I learned so much about how to effectively manipulate and look at data through hierchial indexing in Pandas Dataframes. While I was familiar with \n" \
    "Pandas prior to this class, I had never used multilevel indexing before. I can certainly see how much it helps with sorting and \n"\
    "slicing and ultimately making data and subsequent analysis so much easier! Excited to apply it \n" \
    "in future projects! Best, Marley."
    # Return a string the describes one thing you learned in ENSF 692.
    return learning #returning my string to be outputted

if __name__ == "__main__":
    app.run(debug=True)
