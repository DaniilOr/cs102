from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scraputils import *


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class Posts(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    likes = Column(Integer)
    views = Column(Integer)
    label = Column(String)

Base.metadata.create_all(bind=engine)
'''
s = session()

posts = get_wall(domain = 'pn6', count = 1000)
for post in posts:
    n = News(text=post['text'], likes=post['likes'], views=post['views'])
    s.add(n)
    s.commit()
'''
