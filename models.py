from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, func
from base import Base, inverse_relationship, create_tables

class League(Base):
    __tablename__ = 'leagues'
    id = Column(Integer, primary_key=True)

    api_id = Column(Integer, unique=True)
    api_url = Column(String, unique=True)
    name = Column(String)
    sport = Column(String)

    def parse_json(self, data):
        self.api_id = int(data['id'])
        self.api_url = data['api']
        self.name = data['name']
        self.sport = data['sport']

class Club(Base):
    __tablename__ = 'clubs'
    id = Column(Integer, primary_key=True)

    api_id = Column(Integer, unique=True)
    api_url = Column(String, unique=True)
    name = Column(String)
    city_api_url = Column(String)
    league_api_url = Column(String)

    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship('City', backref=inverse_relationship('clubs'))

    league_id = Column(Integer, ForeignKey('leagues.id'))
    league = relationship('League', backref=inverse_relationship('clubs'))        

    def parse_json(self, data):
        self.api_id = int(data['id'])
        self.api_url = data['api']
        self.name = data['name']
        self.city_api_url = data['city']
        self.league_api_url = data['league']

class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)

    api_id = Column(Integer, unique=True)
    api_url = Column(String, unique=True)
    first = Column(String)
    last = Column(String)
    gender = Column(String)
    current_job = Column(String)
    current_membership = Column(String)

    def parse_json(self, data):
        self.api_id = int(data['id'])
        self.api_url = data['api']
        self.first = data['first']
        self.last = data['last']
        self.gender = data['gender']
        self.current_job = data['current_job']
        self.current_membership = data['current_membership']

class Membership(Base):
    __tablename__ = 'memberships'
    id = Column(Integer, primary_key=True)

    club_id = Column(Integer, ForeignKey('clubs.id'))
    club = relationship('Club', backref=inverse_relationship('memberships'))

    person_id = Column(Integer, ForeignKey('people.id'))
    person = relationship('Person', backref=inverse_relationship('memberships'))

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)

    api_id = Column(Integer, unique=True)
    api_url = Column(String, unique=True)
    name = Column(String)
    company_api_url = Column(String)

    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', backref=inverse_relationship('departments'))    

    def parse_json(self, data):
        self.api_id = int(data['id'])
        self.api_url = data['api']
        self.name = data['name']
        self.company_api_url = data['company']

class Employment(Base):
    __tablename__ = 'employments'
    id = Column(Integer, primary_key=True)

    department_id = Column(Integer, ForeignKey('departments.id'))
    department = relationship('Department', backref=inverse_relationship('employments'))

    person_id = Column(Integer, ForeignKey('people.id'))
    person = relationship('Person', backref=inverse_relationship('employments'))

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)

    api_id = Column(Integer, unique=True)
    api_url = Column(String, unique=True)
    name = Column(String)
    industry = Column(String)
    symbol = Column(String)
    revenue = Column(Integer)

    def parse_json(self, data):
        self.api_id = int(data['id'])
        self.api_url = data['api']
        self.name = data['name']
        self.industry = data['industry']
        self.symbol = data['symbol']
        self.revenue = data['revenue']

class Exchange(Base):
    __tablename__ = 'exchanges'
    id = Column(Integer, primary_key=True)

    api_id = Column(Integer, unique=True)
    api_url = Column(String, unique=True)
    name = Column(String)
    city_url = Column(String)
    address = Column(String)

    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship('City', backref=inverse_relationship('exchanges'))

    def parse_json(self, data):
        self.api_id = int(data['id'])
        self.api_url = data['api']
        self.name = data['name']
        self.city_url = data['city']
        self.address = data['address']        

class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)

    api_id = Column(Integer, unique=True)
    api_url = Column(String, unique=True)
    name = Column(String)
    is_capital = Column(Integer)
    population = Column(String)
    zipcode = Column(String)

    state_id = Column(Integer, ForeignKey('states.id'))
    state = relationship('State', backref=inverse_relationship('cities'))

    def parse_json(self, data):
        self.api_id = int(data['id'])
        self.api_url = data['api']
        self.name = data['name']
        self.is_capital = data['is_capital']
        self.population = data['population']
        self.zipcode = data['zipcode']

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)

    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship('City', backref=inverse_relationship('addresses'))

    person_id = Column(Integer, ForeignKey('people.id'))
    person = relationship('Person', backref=inverse_relationship('addresses'))

class Listing(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)

    exchange_id = Column(Integer, ForeignKey('exchanges.id'))
    exchange = relationship('Exchange', backref=inverse_relationship('listings'))   
    
    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', backref=inverse_relationship('listings'))     

class State(Base):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True)

    api_id = Column(Integer, unique=True)
    api_url = Column(String, unique=True)
    name = Column(String)
    abbreviation = Column(String)

    def parse_json(self, data):
        self.api_id = int(data['id'])
        self.api_url = data['api']
        self.name = data['name']
        self.abbreviation = data['abbreviation']



if __name__ is not '__main__':
    create_tables()
