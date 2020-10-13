from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///phones.sqlite', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    phones = relationship("Phone", back_populates="user", cascade="all, delete-orphan")

    def __str__(self):
        return self.name

    @classmethod
    def add(cls, name):
        user = cls(name=name)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def delete(cls, name):
        user = cls(name=name)
        session.query(User).filter(User.name == name).delete()
        session.commit()
        return user

    @classmethod
    def update(cls, old_name, new_name):
        users = session.query(User).all()
        for i in users:
            if i.name == old_name:
                i.name = new_name
        session.commit()
        return User.name

    @classmethod
    def all(cls):
        return session.query(cls).all()


class Phone(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True)
    phone = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="phones")

    def __str__(self):
        return self.phone

    @classmethod
    def add(cls, phone, user):
        phone = cls(phone=phone, user=user)
        session.add(phone)
        session.commit()
        return phone

    @classmethod
    def all(cls):
        return session.query(cls).all()

    @classmethod
    def update(cls, old_phone, new_phone):
        phones = session.query(Phone).all()
        for i in phones:
            if i.phone == old_phone:
                i.phone = new_phone
        session.commit()
        return Phone.phone


Base.metadata.create_all(engine)
