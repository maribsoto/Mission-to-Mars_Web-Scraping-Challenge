# Import necessary libraries and dependencies
import time
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo

from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import scrape_mars

#################################################
# Database and Flask Setup
#################################################

# create instance of Flask app
app = Flask(__name__)

# Quering the mongo database and correspondent collection
app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Create route that renders index.html template
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    # Return template and data
    return render_template('index.html', mars=mars)


@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    
    # Running the scraping function for all variables
    mars_data = scrape_mars.scrape_all()
    # Updates the collection values and creates a new document 
    mars.update({}, mars_data, upsert=True)
    time.sleep(2)

    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
