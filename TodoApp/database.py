from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

######################################### For using sqlite3 ##########################################
######################################### Install dependencies #######################################
#SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'   #os.getenv('DATABASE_URL')  for using the dotenv connection method
#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {'check_same_thread':False})

######################################### For using PostgreSQL #######################################
######################################### Install dependencies #######################################
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin1234@localhost/TodoApplicationDatabase'   
engine = create_engine(SQLALCHEMY_DATABASE_URL)

######################################### For using MySQL ############################################
######################################### Install dependencies #######################################
#SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:admin1234@127.0.0.1:3306/TodoApplicationDatabase'   
#engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()