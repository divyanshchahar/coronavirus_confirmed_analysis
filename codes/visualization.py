# FUNCTION TO GENERATE HORIZONTAL BAR PLOTS
#
# Input Arguments
#   -   Values for X-axis
#   -   Y-axis Tick Labels
#   -   X-axis Labels
#   -   Y-axis Labels
#   -   Title of the plot
# Output Arguments
#   -   Horizontal Bar plot
def plot_bar_h(x_values, refrence_value, ticklabels_y, label_x, label_y, filename_plt):

    fig, ax = plt.subplots()
    ypos = np.arange(len(x_values))

    ax.barh(ypos, x_values, color=['red', 'green', 'blue', 'cyan', 'orange']) # plotting values
    ax.axvline(refrence_value, linestyle='dashed', color='k', linewidth=0.6, label='Global Average') # Refrence Line
    plt.legend(fontsize=7)

    # X-axis operations
    plt.xticks(fontsize=7) # controlling the foent size of y-tick labells
    ax.set_xlabel(label_x, fontsize=10)

    # Y-axis operations
    ax.invert_yaxis() # inverting the axis
    ax.set_yticks(ypos) # setting y-tick labells
    ax.set_ylabel(label_y, fontsize=10)
    ax.set_yticklabels(ticklabels_y, fontsize=7) # setting y-tick labells

    # Eliminating the spine
    ax.spines['right'].set_visible(False) # eliminating right border
    ax.spines['top'].set_visible(False) # eliminating top border

    # Loop to put up labells
    for i in range(0,len(ypos)):
        plt.text(x=x_values[i], y=ypos[i], s=x_values[i], fontsize=7)

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.savefig(filename_plt, bbox_inches='tight')


# FUNCTION TO PLOT LINE GRAPHS
#
# Input Arguments:
#   -   Values for x-axis
#   -   Values for y-axis
#   -   Labels for Lines
#   -   Labels for x-axis
#   -   Labels for y-axis
#   -   Plot for title
#
# Output Arguments:
#   -   Line Plot
def lineplotter(x_values, y_values, legend_plt, x_label, y_label, filename_plt):
    fig, ax = plt.subplots()

    l = len(x_values)

    # loop to plot all the lines
    for i in range(0, l):
        ax.plot(x_values[i], y_values[i], linewidth=0.9, label=legend_plt[i])

    # Dealing with dates
    date_format = mpl_dates.DateFormatter('%b, %d %y')
    plt.gcf().autofmt_xdate()


    # X-axis Operations
    plt.xticks(fontsize=7)
    ax.set_xlabel(x_label, fontsize=10)
    ax.xaxis.set_major_formatter(date_format)

    # Y-Axis Operations
    plt.yticks(fontsize=7)
    ax.set_ylabel(y_label, fontsize=10)

    # Eliminating the spine
    ax.spines['right'].set_visible(False) # eliminating right border
    ax.spines['top'].set_visible(False) # eliminating top border

    plt.legend(fontsize=7)

    # maximising the graph
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.savefig(filename_plt, bbox_inches='tight')


# FUNCTION TO PLOT LINE GRAPHS (SUBPLOTS)
#
# Input Arguments:
#   -   Number of Rows
#   -   Number of Columns
#   -   Values for x-axis
#   -   Values for y-axis
#   -   Labels for Lines
#   -   Filename to save the Graph
#
# Output Arguments:
#   -   Line Plot
def lineplotter_subplot(r_plt, c_plt, x_values, y_values, legend_plt, filename_plt):

    fig, ax = plt.subplots(r_plt, c_plt, sharex=True) # axis for subplots

    l = len(x_values) # length of the concerned lists

    r = 0 # rows
    c = 0 # columns

    c_pallete = ['red', 'green', 'blue', 'cyan', 'orange']
    l_style = ['solid', 'dashed']

    for j in range(0,l):
        ax[r, c].set_ylim(0, 2) # setting limits of y-axis

        ax[r, c].plot_date(x_values[j], y_values[j], linestyle=l_style[c], marker='None', linewidth=0.9, color=c_pallete[r], label=legend_plt[j])
        ax[r, c].axhline(1, color='k', linewidth=0.3, linestyle='dashed')

        ax[r, c].legend(fontsize=7) # legend

        # Dealing with Dates
        date_format = mpl_dates.DateFormatter('%b, %d %y')
        plt.gcf().autofmt_xdate()
        ax[r, c].xaxis.set_major_formatter(date_format)

        # Eliminating the spine
        ax[r, c].spines['right'].set_visible(False)  # eliminating right border
        ax[r, c].spines['top'].set_visible(False)  # eliminating top border

        # Axis distribution
        r += 1
        if r == r_plt:
            r = 0
            c += 1

    # Zooming the Plots
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.subplots_adjust(left=0.03, right=0.97, top=0.98, bottom=0.08, hspace=0.16, wspace=0.1) # adjusting spaces

    plt.savefig(filename_plt, bbox_inches='tight') # saving plots


# FUNCTION TO STRIP OFF ZEROS
#
# Input Arguments
#   -   Database from which 0 needs to be stripped before first non-zero values
#   -   List of countries for which above mentioned operation needs to be performed
# Output Arguments
#   -   List of Numbers after stripping the zeros (list of lists)
#   -   List of Dates(the dates for which zeros are removed are droped) (list of lists)
def zerostrip(df, filtervalues):
    dates = df.drop(['Country'], axis=1).columns.values.tolist() # extracting dates
    df = df[df.Country.isin(filtervalues)] # filtering required values of the worst hit countries

    x_values = [] # List to hold final values after stripping
    y_values = [] # List to hold final dates after stripping zeros

    for i in filtervalues:
        df_temp = df[df['Country'] == i].values.tolist()
        for k in df_temp:
            l = len(k)
            firstzero = True
            lst1 = []
            lst2 = []
            for p in range(1, l - 2):
                if (firstzero == False) or (k[p] > 0):
                    lst1.append(round(k[p], 3))
                    lst2.append(dates[p - 1])
                    firstzero = False
            x_values.append(lst2)
            y_values.append(lst1)
    return x_values, y_values


# FUNCTION TO CONVERT DATES(STRING VALUES FROM DATABASE) TO DATES(DATES TYPE)
#
# Input Arguments:
#   -   List of Lists with dates as strings
# Output Arguments:
#   -   List of Lists with dates as date/time
def datesorter(listoflist_dates):

    # Correcting for year
    length_listoflist_dates = len(listoflist_dates)
    for i in range(0, length_listoflist_dates): # loop to enter list inside list
        list_dates = listoflist_dates[i]
        length_list_dates = len(list_dates)
        for j in range(0, length_list_dates): # loop to enter individual element inside the list
            element_date = list_dates[j]
            temp_date = element_date.split('/')
            length_temp_date = len(temp_date)
            v = ''
            for k in range(0, length_temp_date):
                if k == length_temp_date-1:
                    temp_date[k] = '20' + temp_date[k]
                else:
                    temp_date[k] = temp_date[k] + '/'
                v = v + temp_date[k]
            element_date = v
            list_dates[j] = element_date

    # # Converting to dates from string
    length_listoflist_dates = len(listoflist_dates)
    for i in range(0, length_listoflist_dates):  # loop to enter list inside list
        list_dates = listoflist_dates[i]
        length_list_dates = len(list_dates)
        for j in range(0, length_list_dates):  # loop to enter individual element inside the list
            element_date = list_dates[j]
            dt = datetime.strptime(element_date, '%m/%d/%Y')
            list_dates[j] = dt

    return listoflist_dates


# FUNCTION TO CLUB VALUES BY COUNTRY
#
# Input Arguments
#   -   List of Values for a certain axis (A list of lists of lists)
#       -   The list contains values in this manner [[[x1c1],[x1c2]], [[x2c1],[x2c2]], [[x3c1],[x3c2]]]
#       -   x represents value
#       -   c represents country
#       -   x1c1 = list of values of fist type for first
#       -   *note* The values are clubbed according to type of values
# Output Arguments
#   -   List of Values for a certain axis ( A list of lists of lists )
#       -   The List contains values in this manner [[[x1c1], [x2c1], [x3c1]], [[x1c2], [x2c2], [x3c2]]]
#       -   The values are clubbed according to country
def listsorter(l):

    l1 = l[0]

    length_l = len(l) # number of values
    length_l1 = len(l1) # number of countries

    lst2 = [] # emplty list to to hold values

    # loop to rearrange distribution of lists
    for i in range(0, length_l1): # first loop to acess different countries
        lst1 = [] # empty list to hold values
        for j in range(0, length_l): # second loop acess different valeus
            a = l[j]
            b = a[i]
            lst1.append(b)
        lst2.append(lst1)
    return lst2


# MAIN BODY OF THE PROGRAM
# Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates
import numpy as np
from datetime import datetime
import statistics as st


####_______________________________________________________ Reading the Database______________________________________________________###

df_coronaC = pd.read_csv('coronavirus_confirmedcases.csv') # confirmed cases of coronavirus
df_coronaC_confirmedcases_average = pd.read_csv('coronavirus_confirmedcases_average.csv') # Average of Confirmed Cases
df_coronaC_newcases = pd.read_csv('coronavirus_newcases.csv') # Confirmed New Cases
df_coronaC_newcases_cummulativeaverage = pd.read_csv('coronavirus_newcases_cummulativeaverage.csv') # Cummulative Average of New Cases
df_coronaC_newcases_growthrate = pd.read_csv('coronavirus_newcases_growthrate.csv') # Growth Rate of New Cases
df_coronaC_newcases_growthrate_cummulativeaverage = pd.read_csv('coronavirus_newcases_growthrate_cummulativeaverage.csv') # Cummulative Average of Growth Rate of New Cases
df_coronaC_newcases_percentgrowth = pd.read_csv('coronavirus_newcases_percentgrowth.csv')
df_coronaC_newcases_percentgrowth_cummulativeaverage = pd.read_csv('coronavirus_newcases_percentgrowth_cummulativeaverage.csv')

#_______________________________________________________________________________________________________________________________________#


###_________________________________________________Creating New Database_and lists__________________________________________________________###

# For Plot 1 - [HORIZONTAL BAR GRAPH] - Countries Worst Affected by Coronavirus (in terms of confirmed cases)
countries = df_coronaC['Country'].values.tolist() # list of countries from original data
dates = df_coronaC.columns.values.tolist() # indexes from original data
lastday = dates[len(dates)-1] # selecting last day entry
lastdaycases = df_coronaC[lastday].values.tolist() # list of cases on last day
globalmean_confirmedcases = int(st.mean(lastdaycases)) # number of cases


data = {'Country': countries, lastday: lastdaycases} # creating dictionary to create DataFrame
df_coronaC_lastday = pd.DataFrame(data) # DataFrame with number of confirmed cases
df_coronaC_worstaffected = df_coronaC_lastday.sort_values(lastday, ascending=False).head(10) # Dataframe of 10 worst affected countries
countries_P1 = df_coronaC_worstaffected['Country'].values.tolist() # list of countries from the the previous DataFrame

# For Plot 2 - [HORIZONTAL BAR GRAPH] - Average Cases Reported Per Day in Countries Worst Affected by Coronavirus
df_temp = df_coronaC_confirmedcases_average[df_coronaC_confirmedcases_average.Country.isin(countries_P1)]
df_temp = df_temp.sort_values('average_cases', ascending=False)
globalmean_averagecases = int(st.mean(df_temp['average_cases'].values.tolist()))

# For Plot 3 - [LINE GRAPH] - Number of Cases in Worst Affected countries
x_values_P3_temp, y_values_P3 = zerostrip(df_coronaC, countries_P1)
x_values_P3 = datesorter(x_values_P3_temp)


# For Plot 4 - [LINE GRAPH] - New Cases in countries Worst Affected by Coronavirus
x_values_P4_temp, y_values_P4 = zerostrip(df_coronaC_newcases, countries_P1)
x_values_P4 = datesorter(x_values_P4_temp)

# For Plot 5 - [LINE GRAPH] - Cummulative Average of New Cases in Worst Hit Countries
x_values_P5_temp, y_values_P5 = zerostrip(df_coronaC_newcases_cummulativeaverage, countries_P1)
x_values_P5 = datesorter(x_values_P5_temp)

# For Plot 6 - [LINE GRAPH] - Growth Rate of New Cases in Worst Affected Countries
x_values_P6_temp, y_values_P6 = zerostrip(df_coronaC_newcases_growthrate, countries_P1)
x_values_P6 = datesorter(x_values_P6_temp)

# For Plot 7 - [LINE GRAPH] - Cummulative Average of Growth Rate of New Cases in Worst Affected Countries
x_values_P7_temp, y_values_P7 = zerostrip(df_coronaC_newcases_growthrate_cummulativeaverage, countries_P1)
x_values_P7 = datesorter(x_values_P7_temp)

# For Plot 8 - LINE GRAPH] - Percentage Growth Rate of Countries Worst Affected by Coronavirus
x_values_P8_temp, y_values_P8 = zerostrip(df_coronaC_newcases_percentgrowth, countries_P1)
x_values_P8 = datesorter(x_values_P8_temp)

# For Plot 9 - [LINE GRAPH] - Cummulative Average of Percent Growth Rate of Countries Worst Affected by Coronavirus
x_values_P9_temp, y_values_P9 = zerostrip(df_coronaC_newcases_growthrate_cummulativeaverage, countries_P1)
x_values_P9 = datesorter(x_values_P9_temp)

#____________________________________________________________________________________________________________________________________#


###______________________________________________________________________________________Plotting the dataset____________________________________________________________________________________________________###

# Plot 1[HORIZONTAL BAR PLOT] - Countries worst affected
plot_bar_h(df_coronaC_worstaffected[lastday].values.tolist(), globalmean_confirmedcases,df_coronaC_worstaffected['Country'].values.tolist(), 'Confirmed Cases', 'Countries', 'plot-1.pdf')

# Plot 2[HORZONTAL BAR PLOT] - AveAverage Cases Reported Per Day in Countries Worst Affected by Coronavirus
plot_bar_h(df_temp['average_cases'].values.tolist(), globalmean_averagecases, df_temp['Country'].values.tolist(), 'Average Cases', 'Countries', 'plot-2.pdf')

# Plot 3[LINE PLOT] - Number of Cases in Worst Affected countries
lineplotter(x_values_P3, y_values_P3, countries_P1, 'Dates', 'Cases', 'plot-3.pdf')

# Plot 4[LINE GRAPH] - New Cases in countries Worst Affected by Coronavirus
lineplotter(x_values_P4, y_values_P4, countries_P1, 'Dates', 'New Cases', 'plot-4.pdf')

# Plot 5[LINE GRAPH] - Cummulative Average of New Cases in Worst Hit Countries
lineplotter(x_values_P5, y_values_P5, countries_P1, 'Dates', 'Moving Average', 'plot-5.pdf')

# Plot 6 - [LINE GRAPH] - Growth Rate of New Cases in Worst Affected Countries
lineplotter_subplot(5, 2, x_values_P6, y_values_P6, countries_P1, 'plot-6.pdf')

# Plot 7 - [LINE GRAPH] - Cummulative Average of Growth Rate of New Cases in Worst Affected Countries
lineplotter_subplot(5, 2, x_values_P7, y_values_P7, countries_P1, 'plot-7.pdf')

# Plot 8 - [LINE GRAPH] - Percentage Growth Rate of Countries Worst Affected by Coronavirus
lineplotter(x_values_P8, y_values_P8, countries_P1, 'Dates', 'Percentage Growth', 'plot-8.pdf')

# Plot 9 - [LINE GRAPH] - Percentage Growth Rate of Countries Worst Affected by Coronavirus
lineplotter(x_values_P9, y_values_P9, countries_P1, 'Dates', 'Moving Average', 'plot-9.pdf')
