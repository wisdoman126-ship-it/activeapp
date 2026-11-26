

import os
from dotenv import load_dotenv



class generalConfig(object):
    APP_NAME = 'active'
    ADMIN_EMAIL = ''
    SECRET_KEY = 'weaksecuritykey'
    
    
class DevelopmentConfig(generalConfig):
    SECRET_KEY =os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/active'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
    