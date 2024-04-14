# importing basic stuff required to create USERS table
from sqlalchemy.orm import declarative_base   # 'declarative_base' helps to create your first class
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import sessionmaker

# name of base model class
Base = declarative_base()

# we will create our USERS table
class User(Base):                 # class name = Singular
    __tablename__ = 'users'       # table name = Plural
    id = Column(Integer, primary_key = True)
    username = Column(String(50), nullable = False)
    email = Column(String(64), unique = True)
    password = Column(String(64), nullable = False)
    created_at = Column(DateTime, default = datetime.now)

    def __str__(self):
        return self.username

# The function below is for the database table which will hold the uploaded files 
class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key = True)
    path = Column(String(255),nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'))  # The user id will let us know that the uploaded file belongs to whom (user)
    created_at = Column(DateTime, default = datetime.now)

    def __str__(self):
        return self.path
    
# more classes for other tables    

#utility functions
def open_db():
    engine =  create_engine('sqlite:///project.db', echo = True)   # echo means to display output
    session = sessionmaker(bind = engine)
    return session()

def add_to_db(object):
    db = open_db()
    db.add(object)
    db.commit()
    db.close()

if __name__ == "__main__":
    #create engine
    # mysql settings
    # database_name = 'projectdb'
    # host = 'localhost'
    # username = 'root'
    # password = 'root'
    # port = 3306
    # engine = engine.create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}')
    # demo
    engine = create_engine('sqlite:///project.db', echo = True)  
    Base.metadata.create_all(engine)
