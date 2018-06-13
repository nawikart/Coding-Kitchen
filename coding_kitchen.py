import data_layer as db

# CodingKitchen
# - Find all the state capitals
# - Find all the states that have exchanges
# - Find all the people who are unemployed
# - Find all the people who are currently part of a club
# - Print out all the states that have rugby teams
# - Find all the companies that have Finance department
# - Create a function that takes in an industry and returns the top five companies by revenue


# STEP 1:
# print(db.get_count_all_item('exchanges'))
# db.populate_all_exchanges()
# db.populate_all_people()
# db.populate_all_employments()
# db.populate_all_clubs()
# db.populate_all_memberships()
# db.populate_all_leagues()
# db.populate_all_departments()
# db.populate_all_companies()


# STEP 2:
db.all_state_capitals()
db.all_states_have_exchanges()
db.all_unemployed_peope(25) # <---- LIMIT 25
db.all_employed_peope(25) # <---- LIMIT 25
db.people_have_active_membership(25) # <---- LIMIT 25
db.states_have_rugby_teams()
db.companies_that_have_finance_department()
db.top_five_companies_by_revenue_for('Timber') #<------ just change 'Timber' to another industry