from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo
from secret import username, password

app = Flask(__name__)

# Create connection variable
## (IK) conn = 'mongodb://localhost:27017'
## (IK) conn = f'mongodb+srv://{username}:{password}@ml-mongo-db.p34ii.mongodb.net'
conn = f'mongodb+srv://{username}:{password}@cluster0.p34ii.mongodb.net'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
##(IK)db = client.mars_db
db = client.Cluster0

# Drops collection if available to remove duplicates
db.intro.drop()
db.test.drop() # <----- DELETE
db.feat_img.drop()

# Insert data into the database
db.intro.insert([{'title': '', 'body': '', 'url': "",
    'weather': ""}])

# # Check if second dictionary can be added
# feat_img = db.feat_img
# feat_img.insert_many([{"name": "", "link": ""}])


# Use flask_pymongo to set up mongo connection
##(IK) app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
uri = f'mongodb+srv://{username}:{password}@cluster0.p34ii.mongodb.net/intro'
app.config["MONGO_URI"] = uri
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def index():
    intro = mongo.db.intro.find_one()
    return render_template("index.html", intro=intro)


@app.route("/scrape")
def scraper():
    intro = mongo.db.intro
    intro_data = scrape_mars.scrape()
    intro.update({}, intro_data, upsert=True)
    # return redirect("/", code=302)

    # feat_img = mongo.db.feat_img
    # feat_img_data = scrape_mars.scrape()
    # intro.update({}, intro_data, upsert=True)
    
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
