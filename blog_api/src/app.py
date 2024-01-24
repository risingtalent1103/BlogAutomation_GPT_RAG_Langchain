from flask import Flask
import os
from .config import app_config
from .models import db, bcrypt
from .views.UserView import user_api as user_blueprint # add this line
from .views.CategoryView import category_api as category_blueprint
from .views.BlogpostView import blogpost_api as blogpost_blueprint
from .views.GoldPriceView import goldprice_api as goldprice_blueprint
from .views.SubscriberView import subscriber_api as subscriber_blueprint
from .views.BlogpostView import save_daily_article
from .views.GoldPriceView import save_gold_price
from .views.SubscriberView import get_subscribers
from apscheduler.schedulers.background import BackgroundScheduler
import random
import requests
from flask import send_from_directory

scheduler = BackgroundScheduler()
def create_app(env_name, article_writer):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__, static_folder="static/dist", template_folder="static/dist")
    print('app.py', os.getenv('DATABASE_URL'))
    a = app_config[env_name]
    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)

    db.init_app(app)  # add this line
    app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')  # add this line
    app.register_blueprint(blogpost_blueprint, url_prefix='/api/v1/blogposts')
    app.register_blueprint(category_blueprint, url_prefix='/api/v1/categories')
    app.register_blueprint(subscriber_blueprint, url_prefix='/api/v1/subscribers')
    app.register_blueprint(goldprice_blueprint, url_prefix='/api/v1/goldprices')


    @app.route('/')
    def send_report():
        print (app.static_folder)
        return send_from_directory(app.static_folder, "index.html")
        # return send_from_directory(app.static_folder, path)
        # # return path
    
    @app.route("/assets/<path:path>")
    def send_assets(path):
        return send_from_directory(app.static_folder + "/assets/", path)
    
    @app.route("/images/<path:path>")
    def send_images(path):
        return send_from_directory(app.static_folder + "/images/", path)
    
    @app.route("/icons/<path:path>")
    def send_icons(path):
        return send_from_directory(app.static_folder + "/icons/", path)
        
    @app.route("/opacitybackground/<path:path>")
    def send_opacitybackgrounds(path):
        return send_from_directory(app.static_folder + "/opacitybackground/", path)
        
    @app.route('/<path:path>')
    def send_article(path):
        print (app.static_folder)
        return send_from_directory(app.static_folder, "index.html")
        # return send_from_directory(app.static_folder, path)
        # # return path
    
    categories = ["Gold Mining",
"Gold Investment",
"The art of goldwork",
"Types of gold in jewelry",
"Gold rush",
"Formation of gold deposits",
"Gold standard",
"Different forms of gold",
"Types of gold in jewelry",
"Gold in history"]

    def create_daily_articles():
        with app.app_context():
            random_number = random.randint(0, 9)
            title, summary, article, img_url = article_writer.create_article_openai(categories[random_number])
            if title == None or article == None:
                print('title or article is none')
                return 
            
            data = {"owner_id": 1, "title": title, "contents": article, "category_id": random_number + 1, "rating":0}
            save_daily_article(data)
            print("article created and saved")
    def save_gold_price_per_day():
        with app.app_context():
            api_key = "goldapi-c3a3rlrjb6990-io"
            symbol = "XAU"
            curr = "USD"
            date = ""

            url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"
            
            headers = {
                "x-access-token": api_key,
                "Content-Type": "application/json"
            }
            
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()

                result = response.json()
                print(result['price'])
                
                save_gold_price({'price': result['price']})
                print('gold price successfully saved')
            except requests.exceptions.RequestException as e:
                print("Error:", str(e))
    def send_daily_aritlce():
        with app.app_context():
            subscribers = get_subscribers()
            
    def stop_scheduler():
        scheduler.shutdown()
        return 'Scheduler stopped successfully!'
    def index():
        """
        example endpoint
        """
        return 'Congratulations! Your first endpoint is workin'



    @app.before_first_request
    def setup():
    
        
        # scheduler.add_job(create_daily_articles, 'cron', hour=9)
        # scheduler.add_job(func=create_daily_articles, trigger="interval", hours = 12)
        # scheduler.add_job(func=save_gold_price_per_day, trigger="interval", hours=12)
        # save_gold_price_per_day()
        # scheduler.add_job(send_daily_aritlce, 'cron', hour=10)
        for i in range(30):
            
            create_daily_articles()

        # Start the scheduler
        scheduler.start()
    return app