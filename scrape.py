# imports
from flask import Flask, jsonify, request, render_template, flash, make_response
from jinja2 import Template
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup, Comment
import json
import copy
import re
import sys






def scrape_products(url):
   # print "READ scraping the URL: %s" % url
    headers = {'User-Agent':'Mozilla/5.0'}
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    # remove script tags
    [s.extract() for s in soup.findAll('script')]

    name = soup.find('div', class_="product-name").get_text()
    price = soup.find('span', class_="pd-price").get_text()


#    products = []

    prod = {
        "Product url":      url,
        "Name":     name,
        "Price":    price,
    }
#    products.append(prod)

    # return list of products on page
    return prod

#if __name__ == "__main__":
#    # ROOT Web URL to scrape
#    webpage = "https://www.koovs.com/blue-cut-sew-polo-tshirt-with-black-and-white-stripes-110739.html?skuid=1807916"
#   # print("BEGIN scraping categories and products from: %s" % webpage)
#    # First, scrape the categories
#    scrape_products(webpage)




app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f28567d441f2b6176a'

@app.route('/', methods=['GET', 'POST'])
def hello():
    input_text = "https://www.koovs.com/blue-cut-sew-polo-tshirt-with-black-and-white-stripes-110739.html?skuid=1807916"

    # Normal page load calls 'GET'. 'POST' gets called when one of the buttons is pressed
    if request.method == 'POST':
        # Check which button was pressed
        if request.form['submit'] == 'Request':
            input_text = request.form.get("text")

            test(input_text)
            scrape(input_text)

        elif request.form['submit'] == 'Clear':
            input_text = ''

    # Render the HTML template. input_text gets fed into the textarea variable in the template
    return render_template('form.html', textarea=input_text)

@app.route('/test',methods=['GET', 'POST'])
def test(url):
    result = scrape_products(url)
    data = json.dumps(result, sort_keys = True, indent = 4)
#    data = json.dumps(results)
    flash(data)

@app.route('/scrape',methods=['GET', 'POST'])
def scrape_url():
    url = request.args.get("url")
    try:
        results = scrape_products(url)
    except ValueError as e:
        results = { 'error': str(e), 'url': url }
    return jsonify(results)

if __name__ == '__main__':
    app.run()
