import csv
from collections import defaultdict

masterDict = defaultdict(lambda: defaultdict(lambda: -1))
totalKeys = [ # The names of all categories that the output csv files will contain
    'Entity',
    'Total_Deaths',
    'Total_Cases',
    'Population',
    'Continent',
    'Death_per_mill',
    'Population_Density',
    'Cases_per_mill',
    'Cumulative_Pos_Rate',
    'Total_Tests',
    'GDP_Per_Cap',
    'Resp_Death_Rate',
    'Median_Age',
    'Contact_Tracing',
    'INT_Travel_Controls',
    'Physicians_Per_1000_ppl',
    'Percent_Urbanization',
    'Life_Expectancy',
    'HC_Expenditure_Per_Capita',
    'Stay_Home_Req',
    'Gathering_Restrictions',
    'Internal_Movement_Restrict',
    'Tests_per_mill'
]

# Countries to be excluded because they did not have enough information available in the raw datasets
excludeCountries = [
    'ATG', 'ARM', 'COM', 'GNQ', 'GRD', 'GNB', 'HKG', 'OWID_KOS', 'LAO', 'MHL', 'FSM', 'LIE', 'MDV', 'MKD', 'MNE',
    'MCO', 'KNA', 'LCA', 'VCT', 'WSM', 'STP', 'SMR', 'SSD', 'TWN', 'VAT', 'OWID_WRL'
]

# A function to process a csv file and add a selected variable to masterDict
def augmentMasterDict(csv_name, helper, date, dateType):
    colToKeys = {}
    keyToCols = {}
    allCodes = set()
    addedToDict = 0
    with open('./' + csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        line_count = 0
        for row in csv_reader:
            # parse first line
            if line_count == 0:
                for num in range(len(row)):
                    colToKeys[num] = row[num]
                    keyToCols[row[num]] = num
                print(f'column names are{", ".join(row)}')
                line_count += 1
            # parse all other lines
            else:
                line_count += 1
                if row[keyToCols['Code']] == '':
                    continue
                allCodes.add(row[keyToCols['Code']])
                # use date to determine if data from this row should be added to masterDict
                if date in row[keyToCols[dateType]]:
                    addedToDict += 1
                    helper(row, keyToCols)
        print(f'Processed {line_count} lines.')

# A second function to add variables to masterDict, but with slightly different semantics
def augmentMasterDict_countCriteria(csv_name, criteria, data_name, save_name):
    colToKeys = {}
    keyToCols = {}
    allCodes = set()
    addedToDict = 0
    totalCount = defaultdict(lambda: 0)
    criteriaCount = defaultdict(lambda: 0)
    with open('./' + csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        line_count = 0
        for row in csv_reader:
            # parse first line
            if line_count == 0:
                for num in range(len(row)):
                    colToKeys[num] = row[num]
                    keyToCols[row[num]] = num
                print(f'column names are{", ".join(row)}')
                line_count += 1
            # parse all other lines
            else:
                line_count += 1
                if row[keyToCols['Code']] == '':
                    continue
                allCodes.add(row[keyToCols['Code']])
                totalCount[row[keyToCols['Code']]] += 1
                # use criteria to determine if data from this row should be counted
                if row[keyToCols[data_name]] in criteria:
                    criteriaCount[row[keyToCols['Code']]] += 1
        # use counted data to create entries in masterDict
        for code in allCodes:
            masterDict[code][save_name] = float(criteriaCount[code])/totalCount[code]
        print(f'Processed {line_count} lines.')

# helper functions to convert each raw csv file into data for masterDict
def helper_covid_tests_cases_deaths(row, keyToCols):
    thisDict = masterDict[row[keyToCols['Code']]]
    thisDict['Entity'] = row[keyToCols['Entity']]
    if (row[keyToCols['Total confirmed deaths due to COVID-19']] == ''):
        if thisDict['Total_Deaths'] <= 0:
            thisDict['Total_Deaths'] = 0
    else:
        thisDict['Total_Deaths'] = int(row[keyToCols['Total confirmed deaths due to COVID-19']])
    if (row[keyToCols['Total confirmed cases of COVID-19']] == ''):
        if thisDict['Total_Cases'] <= 0:
            thisDict['Total_Cases'] = 0
    else:
        thisDict['Total_Cases'] = int(row[keyToCols['Total confirmed cases of COVID-19']])

def helper_confirmed_deaths_vs_population(row, keyToCols):
    thisDict = masterDict[row[keyToCols['Code']]]
    thisDict['Population'] = int(row[keyToCols['Population in 2020 (UNWPP, 2019)']])
    thisDict['Continent'] = row[keyToCols['Continent']]

def helper_death_rate_vs_pop_density(row, keyToCols):
    thisDict = masterDict[row[keyToCols['Code']]]
    thisDict['Death_per_mill'] = float(row[keyToCols['Total confirmed deaths due to COVID-19 per million people']])
    if (row[keyToCols['Population density (people per sq. km of land area)']] == ''):
        thisDict['Population_Density'] = 0
        # print(row[keyToCols['Code']])
    else:
        thisDict['Population_Density'] = float(row[keyToCols['Population density (people per sq. km of land area)']])

def helper_covid_daily_vs_total_cases_per_million(row, keyToCols):
    thisDict = masterDict[row[keyToCols['Code']]]
    thisDict['Cases_per_mill'] = float(row[keyToCols['Total confirmed cases of COVID-19 per million people']])

def helper_covid_19_positive_rate_bar(row, keyToCols):
    thisDict = masterDict[row[keyToCols['Code']]]
    thisDict['Cumulative_Pos_Rate'] = float(row[keyToCols['cumulative_positivity_rate']])

def helper_full_list_total_tests(row, keyToCols):
    thisDict = masterDict[row[keyToCols['Code']]]
    thisDict['Total_Tests'] = int(row[keyToCols['total_tests']])

def helper_gdb_per_capita_worldbank(row, keyToCols):
    thisDict = masterDict[row[keyToCols['Code']]]
    thisDict['GDP_Per_Cap'] = round(float(row[keyToCols['GDP per capita, PPP (constant 2011 international $)']]))

def helper_respiratory_disease_death_rate(row, keyToCols):
    thisDict = masterDict[row[keyToCols['Code']]]
    thisDict['Resp_Death_Rate'] = float(row[keyToCols['Deaths - Chronic respiratory diseases - Sex: Both - Age: Age-standardized (Rate)']])

def helper_population_growth_median_age(row, keyToCols):
    thisDict = masterDict[row[keyToCols['Code']]]
    thisDict['Median_Age'] = float(row[keyToCols['UN Population Division (Median Age) (2017)']])

def helper_physicians_per_1000_people(row, keyToCols):
    thisDict = masterDict[row[keyToCols['Code']]]
    thisDict['Physicians_Per_1000_ppl'] = float(row[keyToCols['Physicians (per 1,000 people)']])

def helper_urbanization_vs_gdp(row, keyToCols):
    thisDict = masterDict[row[keyToCols['Code']]]
    if row[keyToCols['Urban population (%) long-run to 2016 (OWID)']] != '':
        thisDict['Percent_Urbanization'] = float(row[keyToCols['Urban population (%) long-run to 2016 (OWID)']])

def helper_life_expectancy(row, keyToCols):
    thisDict = masterDict[row[keyToCols['Code']]]
    thisDict['Life_Expectancy'] = float(row[keyToCols['Life expectancy']])

def helper_health_expenditure(row, keyToCols):
    thisDict = masterDict[row[keyToCols['Code']]]
    if row[keyToCols['Health expenditure per capita, PPP (constant 2011 international $)']] != '':
        thisDict['HC_Expenditure_Per_Capita'] = round(float(row[keyToCols['Health expenditure per capita, PPP (constant 2011 international $)']]))

# Adjust total tests with population
def make_test_per_mill():
    for country in masterDict:
        thisDict = masterDict[country]
        if thisDict['Total_Tests'] != -1:
            thisDict['Tests_per_mill'] = thisDict['Total_Tests']/thisDict['Population']

# Function to convert the completed masterDict into a csv file
def makeCSV(filename, exclude, mustIncludeList):
    with open('./' + filename, 'w', newline = '') as csv_file:
        writer = csv.writer(csv_file)
        fstrow = ['Code']
        for elem in totalKeys:
            fstrow.append(elem)
        writer.writerow(fstrow)
        for entry in masterDict:
            if exclude and entry in excludeCountries:
                continue
            include = True
            row = [entry]
            for mustInclude in mustIncludeList:
                if masterDict[entry][mustInclude] == -1:
                    include = False
            if not include:
                continue
            for elem in totalKeys:
                row.append(masterDict[entry][elem])
            writer.writerow(row)

# Main function that makes all helper function calls
def main():
    date = '2021-04'
    augmentMasterDict('covid-tests-cases-deaths.csv', helper_covid_tests_cases_deaths, date, 'Day')
    augmentMasterDict('total-confirmed-deaths-due-to-covid-19-vs-population.csv', helper_confirmed_deaths_vs_population, date, 'Day')
    augmentMasterDict('covid-19-death-rate-vs-population-density.csv', helper_death_rate_vs_pop_density, date, 'Day')
    augmentMasterDict('covid-daily-vs-total-cases-per-million.csv', helper_covid_daily_vs_total_cases_per_million, date, 'Day')
    augmentMasterDict('covid-19-positive-rate-bar.csv', helper_covid_19_positive_rate_bar, date, 'Day')
    augmentMasterDict('full-list-total-tests-for-covid-19.csv', helper_full_list_total_tests, date, 'Day')
    augmentMasterDict('gdp-per-capita-worldbank.csv', helper_gdb_per_capita_worldbank, '201', 'Year')
    augmentMasterDict('respiratory-disease-death-rate.csv', helper_respiratory_disease_death_rate, '2017', 'Year')
    augmentMasterDict('population-growth-rate-vs-median-age.csv', helper_population_growth_median_age, '2020', 'Year')
    augmentMasterDict_countCriteria('covid-contact-tracing.csv', ['2'], 'contact_tracing', 'Contact_Tracing')
    augmentMasterDict_countCriteria('international-travel-covid.csv', ['3', '4'], 'international_travel_controls', 'INT_Travel_Controls')
    augmentMasterDict('physicians-per-1000-people.csv', helper_physicians_per_1000_people, '201', 'Year')
    augmentMasterDict('urbanization-vs-gdp.csv', helper_urbanization_vs_gdp, '201', 'Year')
    augmentMasterDict('life-expectancy.csv', helper_life_expectancy, '201', 'Year')
    augmentMasterDict('life-expectancy-vs-healthcare-expenditure.csv', helper_health_expenditure, '201', 'Year')
    augmentMasterDict_countCriteria('stay-at-home-covid.csv', ['2','3'], 'stay_home_requirements', 'Stay_Home_Req')
    augmentMasterDict_countCriteria('public-gathering-rules-covid.csv', ['4'], 'restriction_gatherings', 'Gathering_Restrictions')
    augmentMasterDict_countCriteria('internal-movement-covid.csv', ['2'], 'restrictions_internal_movements', 'Internal_Movement_Restrict')

    make_test_per_mill()

    makeCSV('data.csv', False, [])
    makeCSV('processed data.csv', True, ['Death_per_mill', 'Cases_per_mill'])
    makeCSV('processed data with testing.csv', True, ['Death_per_mill', 'Cases_per_mill', 'Total_Tests'])


main()