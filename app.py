# Importing Dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

#Create Flask App.
app=Flask(__name__,template_folder='templates')

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create first App Route.
@app.route("/")

# Creating first view and assigning mongo database data to the mars variable.
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

#Creating Second App Route
@app.route("/scrape")

# Creating Second View
def scrape():
    # Assigning mongo data to the mars variable
    mars = mongo.db.mars

    # Performing the imported scraping.py's scape_all function.
    mars_data = scraping.scrape_all()
    # Updating the mongo database.
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"

# Creating the code to run the Flask app when this file is run.
if __name__ == "__main__":
   app.run()
