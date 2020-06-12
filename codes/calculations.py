# FUNCTION TO CALCULATE AVERAGE CASSES RECORDED (last day cases/ number of days the infections were reported)
# Input Arguments:
#   -   Dataframe with numbers of interest(confirmed cases/deaths/recovered) per day (grouped by country)
# Output Arguments
#   -   Dataframe with country names and average cases
def average_calculator(df):
    countries = df['Country'].values.tolist()  # extracting name of the countries
    length_countries = len(countries)
    averagecases = []  # list to hold average cases

    # loop to calculate average cases (total reported cases/days)
    for i in range(0, length_countries):
        df_temp = df.loc[i].values.tolist()  # creating dataframe by country
        length_df_temp = len(df_temp)
        nullcasecount = df_temp.count(0)  # accounting for days with 0 reported cases
        n = int((df_temp[length_df_temp - 1] / (length_df_temp - nullcasecount)))  # performing calculation on last column values on.y
        averagecases.append(n)

    data = {'Country': countries, 'average_cases': averagecases}
    df_final = pd.DataFrame(data)

    return df_final


# FUNCTION TO CALCULATE NEW CASES EVERYDAY
#
# Input Arguments:
#   -   Dataframe with numbers of interest(confirmed cases/deaths/recovered) per day (grouped by country)
# Output Parameters:
#   -   DataFrame with new instances of number of interest(confirmed cases/deaths/recovered)
def newinstance_calculator(df):
    countries = df['Country'].values.tolist()  # extracting name of the countries
    dates = df.drop(['Country'], axis=1).columns.values.tolist()  # extracting dates

    length_countries = len(countries) # number of countries
    length_dates = len(dates) # number of days

    count = 0
    index_df_final = []  # list to hold dates required after calculation is complete

    # loop to create list of index
    for i in range(1, length_dates):  # first date is skipped as mandated by the formula we are gonna use
        index_df_final.append(dates[i])

    # loop to calculate new cases
    for i in range(0, length_countries):  # first loop to select rows by country names
        df_temp = df.loc[i].values.tolist()  # creating dataframe by country (first element of the list will be a country name and not a date)
        length_df_temp = len(df_temp)

        newinstance = [] # list to hold new cases

        for j in range(2, length_df_temp): # second loop to iterate through columns (going through dates of a country)
            k = int(df_temp[j]) - int(df_temp[j-1])
            newinstance.append(k)

        if count == 0:
            initial_array = np.array(newinstance)
            count += 1
        else:
            final_array = np.vstack((initial_array, newinstance))
            initial_array = final_array
            count += 1

    df_final = pd.DataFrame(final_array, columns=index_df_final)
    df_final.insert(0, 'Country', countries)

    return df_final


# FUNCTION TO CALCULATE AVERAGE NEW CASES(PROGRESSION)
# Input Parameters:
#   -   Dataframe with numbers of interest(confirmed cases/deaths/recovered) per day (grouped by country)
# Output Parameters:
#   -   Dataframe with progression of number of interst(confirmed cases/deaths/recovered)
def cummulativeaverage_calculator(df):
    countries = df['Country'].values.tolist() # extracting name of the countries
    dates = df.drop(['Country'], axis=1).columns.values.tolist() # extracting dates

    length_countries = len(countries) # number of countries
    length_dates = len(dates) # number of days

    count = 0
    index_df_final = [] # list to hold dates required after calculation is complete

    # loop to create list of index
    for i in range(1, length_dates): # first date is skipped as mandated by the formula we are gonna use
        index_df_final.append(dates[i])

    # loop to calculate new cases
    for i in range(0, length_countries):  # first loop to select rows by country names
        df_temp = df.loc[i].values.tolist()  # creating dataframe by country (first element of the list will be a country name and not a date)
        length_df_temp = len(df_temp)

        n = 0
        totalnewcases = 0
        averagevalue = []
        firstzero = False

        for j in range(2, length_df_temp):  # second loop to iterate through columns (going through dates of a country)
            if (firstzero == False) or (df_temp[j] > 0):
                n += 1
                totalnewcases = totalnewcases + (df_temp[j] - df_temp[j-1]) # calculating total new cases
                k = round(totalnewcases/n, 3)  # calculating average number of cases reported till that day
                averagevalue.append(k)
                firstzero = True
            else:
                k = 0
                averagevalue.append(k)

        if count == 0:
            initial_array = np.array(averagevalue)
            count += 1
        else:
            final_array = np.vstack((initial_array, averagevalue))
            initial_array = final_array
            count += 1

    df_final = pd.DataFrame(final_array, columns=index_df_final)
    df_final.insert(0, 'Country', countries)

    return df_final


# FUNCTION TO CALCULATE GROWTH RATE
#
# Input Arguments:
#   -   Dataframe with numbers of interest(confirmed cases/deaths/recovered) per day (grouped by country)
# Output Parameters:
#   -   DataFrame with growth rate for each each for all countries
def growthrate_calculator(df):
    countries = df['Country'].values.tolist()  # extracting name of the countries
    dates = df.drop(['Country'], axis=1).columns.values.tolist()  # extracting dates

    length_country = len(countries) # number of countries
    length_dates = len(dates) # number of days

    count = 0
    index_df_final = [] # list to hold dates required after calculation is complete

    # loop to create list of index
    for i in range(1, length_dates): # first date is skipped as mandated by the formula we are gonna use
        index_df_final.append(dates[i])

    # loop to calculate new cases
    for i in range(0, length_country):  # first loop to select rows by country names
        df_temp = df.loc[i].values.tolist()  # creating dataframe by country (first element of the list will be a country name and not a date)
        length_df_temp = len(df_temp)

        growthrate = [] # list to hold new cases

        for j in range(2, length_df_temp):  # second loop to iterate through columns (going through dates of a country)
            try:
                k = round(int(df_temp[j])/int(df_temp[j-1]), 3)
            except ZeroDivisionError:
                k = 0

            growthrate.append(k)

        if count == 0:
            initial_array = np.array(growthrate)
            count += 1
        else:
            final_array = np.vstack((initial_array, growthrate))
            initial_array = final_array
            count += 1

    df_final = pd.DataFrame(final_array, columns=index_df_final)
    df_final.insert(0, 'Country', countries)

    return df_final


# MAIN BODY OF THE PROGRAM
# importing libraries
import pandas as pd
import numpy as np


####____________________________________________________ Reading the Databases _________________________________________________________________________###

# Confirmed Casses of Corona Virus (Globally) (Database of John Hopkins University)
df_coronaC_global = pd.read_csv(r'COVID-19-master\COVID-19-master\csse_covid_19_data\csse_covid_19_time_series\time_series_covid19_confirmed_global.csv')

#_________________________________________________________________________________________________________________________________________________________#


###___________________________________________________Operations on Dataframes___________________________________________________________###

# Confirmed Casses of Corona Virus (Globally)
df_coronaC_global = df_coronaC_global.drop(['Province/State', 'Lat', 'Long'], axis=1)  # dropping unnecessary columns
df_coronaC_global = df_coronaC_global.rename(columns={'Country/Region': 'Country'})  # renaming columns for future use
df_coronaC_global = df_coronaC_global.groupby('Country').sum()  # summing up the values for countries
df_coronaC_global.to_csv('coronavirus_confirmedcases.csv')  # writing results to a file to be read later
df_coronaC_global = pd.read_csv('coronavirus_confirmedcases.csv')  # recreating the dataset (nullifying the effects of groupby objects)

#____________________________________________________________________________________________________________________________________________#


###________________________________________________________________Calculations on Dataset _______________________________________________________________________###

df_coronaC_confirmedcases_average = average_calculator(df_coronaC_global)  # average cases reported per day
df_coronaC_newcases = newinstance_calculator(df_coronaC_global)  # occurance of new cases
df_coronaC_newcases_cummulativeaverage = cummulativeaverage_calculator(df_coronaC_newcases)  # cummulative average of new cases reported per day
df_coronaC_newcases_growthrate = growthrate_calculator(df_coronaC_newcases)  # Growth rate of new cases
df_coronaC_newcases_growthrate_cummulativeaverage = cummulativeaverage_calculator(df_coronaC_newcases_growthrate)  # Cummulative Average of Growth Rate of New Cases

#___________________________________________________________________________________________________________________________________________________________________#


#____________________________________________________ Wrtiting Data To file_______________________________________________________#

df_coronaC_confirmedcases_average.to_csv('coronavirus_confirmedcases_average.csv', index=False)
df_coronaC_newcases.to_csv('coronavirus_newcases.csv', index=False)
df_coronaC_newcases_cummulativeaverage.to_csv('coronavirus_newcases_cummulativeaverage.csv', index=False)
df_coronaC_newcases_growthrate.to_csv('coronavirus_newcases_growthrate.csv', index=False)
df_coronaC_newcases_growthrate_cummulativeaverage.to_csv('coronavirus_newcases_growthrate_cummulativeaverage.csv', index=False)

###____________________________________________________________________________________________________________________________###