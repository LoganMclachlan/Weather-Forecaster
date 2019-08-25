# imported modules to be used in program
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from flask import Flask
import urllib.error
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy as SQLA
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os

# sets up forecaster app
forecaster = Flask(__name__)
forecaster.config["SECRET_KEY"] = os.environ.get("WF_SK")
database = SQLA(forecaster)
forecaster.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
login_manager = LoginManager(forecaster)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
hasher = Bcrypt(forecaster)

forecaster.config["MAIL_SERVER"] = "smtp.gmail.com"
forecaster.config["MAIL_PORT"] = 587
forecaster.config["MAIL_USE_TLS"] = True
forecaster.config["MAIL_USERNAME"] = os.environ.get("ALT_EMAIL_USER")
forecaster.config["MAIL_PASSWORD"] = os.environ.get("ALT_EMAIL_PASS")
mail = Mail(forecaster)

try:
    # url containing weaather forecast
    url = "https://www.bbc.co.uk/weather"
    # opens url and reads its data
    with urlopen(url) as f:
        web_html = f.read()
    # puts the html of the web page into a variable
    web_soup = soup(web_html,"html.parser")
    # finds the specific elements of the html (parts with the forecast)
    weather_data = web_soup.findAll("p", {"class":"wr-c-text-forecast__summary-text gel-long-primer gs-u-mt-"})
    # puts the contents of the wanted elements into a dictionary
    forecast = {"today":weather_data[0].text,"tomorow":weather_data[1].text,"coming up":weather_data[2].text}
    # gets the currant date
except urllib.error.URLError:
    forecast = {"today":"could not connect to internet",
                "tomorow":"could not connect to internet",
                "coming up":"could not connect to internet"}

import Forecaster.routes
