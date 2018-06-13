import json, requests
from pprint import pprint
import models as mo
from base import DbManager

DB_MANAGER = DbManager()
KK_API = 'http://35.153.66.157/api/{}/{}'

def get_request(url):
    response = requests.get(url)
    return json.loads(response.text)

def get_count_all_item(key):
    n = 0
    for page in range(1, 10):
        url = KK_API.format(key, page)
        try:
            n = n + len(get_request(url))
        except:
            break
            
    if n == 0:
        try:
            url = KK_API.format(key, '')
            n = len(get_request(url))
        except:
            pass

    return n

def get_state(state_url):
    try:
        state = DB_MANAGER.open().query(mo.State).filter(mo.State.api_url == state_url).one()
        return state        
    except:
        try:
            state_obj = get_request(state_url)
            state = mo.State()
            state.parse_json(state_obj)
            state = DB_MANAGER.save(state)
            return state
        except:
            return None

def get_club(club_url):
    try:
        club = DB_MANAGER.open().query(mo.Club).filter(mo.Club.api_url == club_url).one()
        if not club.city:
            city_obj = get_request(club_url)
            club.city = get_city(club_obj['city'])
            club.league = get_league(club_obj['league'])
            DB_MANAGER.save(person)
        return club          
    except:
        try:
            club_obj = get_request(club_url)
            club = mo.Club()
            club.parse_json(club_obj)
            club.city = get_city(club_obj['city'])
            club.league = get_league(club_obj['league'])
            club = DB_MANAGER.save(club)
            return club
        except:
            return None

def get_person(person_url):
    try:
        return DB_MANAGER.open().query(mo.Person).filter(mo.Person.api_url == person_url).one()
    except:
        try:
            person_obj = get_request(person_url)
            person = mo.Person()
            person.parse_json(person_obj)
            person = DB_MANAGER.save(person)
            return person
        except:
            return None   

def get_department(department_url):
    try:
        department = DB_MANAGER.open().query(mo.Department).filter(mo.Department.api_url == department_url).one()
        if not department.company:
            department_obj = get_request(department_url)
            department.company = get_company(department_obj['company'])
            DB_MANAGER.save(department)        
        return department        
    except:
        try:
            department_obj = get_request(department_url)
            department = mo.Department()
            department.parse_json(department_obj)
            department.company = get_company(department_obj['company'])
            department = DB_MANAGER.save(department)
            return department
        except:
            return None

def get_league(league_url):
    try:
        league = DB_MANAGER.open().query(mo.League).filter(mo.League.api_url == league_url).one()
        return league        
    except:
        try:
            league_obj = get_request(league_url)
            league = mo.League()
            league.parse_json(league_obj)
            league = DB_MANAGER.save(league)
            return league
        except:
            return None

def get_company(company_url):
    try:
        company = DB_MANAGER.open().query(mo.Company).filter(mo.Company.api_url == company_url).one()
        return company        
    except:
        try:
            company_obj = get_request(company_url)
            company = mo.Company()
            company.parse_json(company_obj)
            company = DB_MANAGER.save(company)
            return company
        except:
            return None

def get_exchange(exchange_url):
    try:
        exchange = DB_MANAGER.open().query(mo.Exchange).filter(mo.Exchange.api_url == exchange_url).one()
        if not exchange.city:
            exchange_obj = get_request(exchange_url)
            exchange.city = get_city(exchange_obj['city'])
            DB_MANAGER.save(exchange)        
        return exchange        
    except:
        try:
            exchange_obj = get_request(exchange_url)
            exchange = mo.Exchange()
            exchange.parse_json(exchange_obj)
            exchange.city = get_city(exchange_obj['city'])
            exchange = DB_MANAGER.save(exchange)
            return exchange
        except:
            return None

def get_city(city_url):
    try:
        city = DB_MANAGER.open().query(mo.City).filter(mo.City.api_url == city_url).one()
        if not city.state or city.state == None:            
            city_obj = get_request(city_url)
            city.state = get_state(city_obj['state'])
            DB_MANAGER.save(city)
        return city        
    except:
        try:
            city_obj = get_request(city_url)
            city = mo.City()
            city.parse_json(city_obj)
            city.state = get_state(city_obj['state'])
            city = DB_MANAGER.save(city)
            return city
        except:
            return None

def get_membership(person, club):    
    try:
        membership = self.open().query(Membership).filter(Membership.person_id == person.id, Membership.club_id == club.id).one()
    except:
        membership = mo.Membership()
        membership.person = person
        membership.club = club
        DB_MANAGER.save(membership)
        return membership

    return None

def get_employment(person, department):
    try:
        employment = DB_MANAGER.open().query(mo.Employment).filter(mo.Employment.person_id == person.id, mo.Employment.department_id == department.id).one()
    except:
        employment = mo.Employment()
        employment.person = person
        employment.department = department
        DB_MANAGER.save(employment)
        return employment

    return None

def populate_all_people():
    for person_id in range(1, get_count_all_item('people') + 1):
        url = KK_API.format('person', person_id)
        person = get_person(url)
        if person != None:
            print(person.first)    

def populate_all_clubs():
    for club_id in range(1, get_count_all_item('clubs') + 1):
        url = KK_API.format('club', club_id)
        club = get_club(url)
        if club != None:
            print(club.name)  

def populate_all_memberships():
    for person in DB_MANAGER.open().query(mo.Person).filter(mo.Person.current_membership != None).all():
        membership = get_membership(person, get_club(person.current_membership))
        print(membership.person.first, membership.club.name)

def populate_all_employments():
    for person in DB_MANAGER.open().query(mo.Person).filter(mo.Person.current_job != None).all():
        employment = get_employment(person, get_department(person.current_job))
        print(employment.person.first, employment.department.name)

def populate_all_leagues():
    for league_id in range(1, get_count_all_item('leagues') + 1):
        url = KK_API.format('league', league_id)
        league = get_league(url)
        if league != None:
            print(league.name) 

def populate_all_departments():
    for department_id in range(1, get_count_all_item('departments') + 1):
        url = KK_API.format('department', department_id)
        department = get_department(url)
        if department != None:
            print(department.name) 

def populate_all_companies():
    for company_id in range(1, get_count_all_item('companies') + 1):
        url = KK_API.format('company', company_id)
        company = get_company(url)
        if company != None:
            print(company.name) 

def populate_all_cities():
    for city_id in range(1, get_count_all_item('cities') + 1):
        url = KK_API.format('city', city_id)
        city = get_city(url)
        if city != None:
            print(city.name)

def populate_all_exchanges():
    for exchange_id in range(1, get_count_all_item('exchanges') + 1):
        url = KK_API.format('exchange', exchange_id)
        exchange = get_exchange(url)
        if exchange != None:
            print(exchange.name)

def all_state_capitals():
    print('\n\n\t_______Find all the state capitals_______')
    print('\t=========================================')
    print('\t|  city\t\t\t state\t\t')
    print('\t-----------------------------------------')
    for city in DB_MANAGER.open().query(mo.City).all():
        if city.is_capital == 1:
            print('\t|  {}\t\t  {} \t'.format(city.name, city.state.name))
    print('\n\n')

def all_states_have_exchanges():
    # populate_all_exchanges()
    print('\n\n\t__________Find all the states that have exchanges___________')
    print('\t=============================================================')
    print('\t|  exchange\t\t\t\t\t state\t\t')
    print('\t-------------------------------------------------------------')    
    for exchange in DB_MANAGER.open().query(mo.Exchange).all():
        print('\t|  {}\t\t\t  {} \t'.format(exchange.name, exchange.city.state.name))
    print('\n\n')

def all_unemployed_peope(limit):
    # populate_all_people()
    print('\n\n\t__________Find all the people who are unemployed___________ LIMIT: {}'.format(limit))
    print('\t=============================================================')
    print('\t|  Fullname\t\t\t\t\t Gender\t\t')
    print('\t-------------------------------------------------------------')    
    for person in DB_MANAGER.open().query(mo.Person).filter(mo.Person.current_job == None).limit(limit).all():
        print('\t|  {} {}\t\t\t  {} \t'.format(person.first, person.last, person.gender))
    print('\n\n')

def all_employed_peope(limit):
    # populate_all_people()
    print('\n\n\t__________Find all the people who are employed___________ LIMIT: {}'.format(limit))
    print('\t==============================================================================================================')
    print('\t|  Fullname\t\t\t Department\t\t\t\t Company')
    print('\t--------------------------------------------------------------------------------------------------------------')    
    for person in DB_MANAGER.open().query(mo.Person).filter(mo.Person.current_job != None).limit(limit).all():
        for employment in person.employments:
            try:
                company = employment.department.company.name
            except:
                company = None
            print('\t|  {} {}\t\t\t  {} \t\t\t\t {}'.format(person.first, person.last, employment.department.name, company))
    print('\n\n')

def people_have_active_membership(limit):
    # populate_all_people()
    print('\n\n\t___Find all the people who are currently part of a club____ LIMIT: {}'.format(limit))
    print('\t=============================================================')
    print('\t|  Fullname\t\t\t\t\t Club\t\t')
    print('\t-------------------------------------------------------------')    
    for person in DB_MANAGER.open().query(mo.Person).filter(mo.Person.current_membership != None).limit(limit).all():
        for membership in person.memberships:
            print('\t|  {} {}\t\t\t  {} \t'.format(person.first, person.last, membership.club.name))
    print('\n\n')

def states_have_rugby_teams():
    # populate_all_leagues()
    # populate_all_clubs()
    print('\n\n\t_Print out all the states that have RUGBY teams_')
    print('\t===========================================================')
    print('\t|  State\t\t League\t\t')
    print('\t-----------------------------------------------------------')    
    for league in DB_MANAGER.open().query(mo.League).filter(mo.League.sport == 'Rugby').all():
        for club in league.clubs:
            print('\t|  {}\t\t {} \t'.format(club.city.state.name, league.name))
    print('\n\n')

def companies_that_have_finance_department():
    # db.populate_all_departments()
    print('\n\n\t_Find all the companies that have FINANCE department_')
    print('\t===========================================================================')
    print('\t|  Company\t\t\t\t Industry\t\t')
    print('\t---------------------------------------------------------------------------')    
    for department in DB_MANAGER.open().query(mo.Department).filter(mo.Department.name == 'Finance').all():
        if department.company:
            print('\t|  {}\t\t {} \t'.format(department.company.name, department.company.industry))
    print('\n\n')

def top_five_companies_by_revenue_for(industry):
    # populate_all_companies()
    print('\n\n\tCreate a function that takes in an industry and returns the top five companies by revenue_')
    print('\n\tIndustry: {}\n'.format(industry))
    print('\t===========================================================================')
    print('\t|  Company\t\t\t\t Revenue\t\t')
    print('\t---------------------------------------------------------------------------')  
    for company in DB_MANAGER.open().query(mo.Company).filter(mo.Company.industry == industry).order_by(mo.Company.revenue.desc()).limit(5).all():
        print('\t|  {}\t\t\t {} \t'.format(company.name, company.revenue))
    print('\n\n')