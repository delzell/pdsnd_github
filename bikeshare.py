#%%
import time
import pandas as pd
import numpy as np
import calendar
from tabulate import tabulate

# A dictionary linking city names to their data files
CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

#%%
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    while True:
        city = input("Enter the city name for which you would like to get statistics. \nEnter one of Chicago, New York City, or Washington: ").title()
        if city in ('Chicago', 'New York City', 'Washington'):
            break
        else:
            print("You did not enter a valid input.")
            
    while True:
        month = input("Enter the month name for which you would like to get statistics (through June).\nEnter 'all' for all months: ").title()
        if (month in calendar.month_name[1:7]) or (month == 'All') :
            break
        else:
            print("You did not enter a valid input.")

    while True:
        day = input("Enter the day name for which you would like to get statistics.\nEnter 'all' for all days: ").title()
        if (day in calendar.day_name) or (day == 'All'):
            break
        else:
            print("You did not enter a valid input.")

    print('-'*40)
    return city, month, day

#%%
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

#%%
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most Frequent Month:', calendar.month_name[df['month'].mode()[0]])

    # display the most common day of week
    print('Most Frequent Day:', df['day_of_week'].mode()[0])

    # display the most common start hour
    print('Most Frequent Starting Hour:', df['Start Time'].dt.hour.mode()[0])

#%%
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Frequently Used Start Station:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most Frequently Used End Station:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df["Both Stations"] = "\nStart: " + df["Start Station"] + "\nEnd: " + df["End Station"]
    print('Most Frequently Used Station Combination:', df['Both Stations'].mode()[0])

#%%
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total Travel Time: ",sum(df["Trip Duration"]))

    # display mean travel time
    print("Average Travel Time: ", df["Trip Duration"].mean())

#%%
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nCounts of User Types:\n",df["User Type"].value_counts())

    # Display counts of gender
    try:
        print("\nCounts of Gender:\n",df["Gender"].value_counts())
    except Exception:
        pass

    # Display earliest, most recent, and most common year of birth
    try:
        print("\nEarliest Birth Year: ", df["Birth Year"].min())
        print("Most Recent Birth Year: ", df["Birth Year"].max())
        print("Most Common Birth Year: ", df["Birth Year"].mode()[0])
    except Exception:
        pass

#%%
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
       
        # This code prints the raw data.
        i = 0
        while True:
            display_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
            if display_data.lower() != 'yes':
                break
            if (i + 5) < df.shape[0]:
                print(tabulate(df.iloc[np.arange(0+i,5+i),1:3], headers ="keys"))
                print(tabulate(df.iloc[np.arange(0+i,5+i),3:6], headers ="keys"))
                if (city != 'Washington'):
                    print(tabulate(df.iloc[np.arange(0+i,5+i),6:11], headers ="keys"))
                else:
                    print(tabulate(df.iloc[np.arange(0+i,5+i),6:9], headers ="keys"))
            else:
                print(tabulate(df.iloc[np.arange(0+i,df.shape[0]),1:3], headers ="keys"))
                print(tabulate(df.iloc[np.arange(0+i,df.shape[0]),3:6], headers ="keys"))
                if (city != 'Washington'):
                    print(tabulate(df.iloc[np.arange(0+i,df.shape[0]),6:11], headers ="keys"))
                else:
                    print(tabulate(df.iloc[np.arange(0+i,df.shape[0]),6:9], headers ="keys"))
                print("You have reached the end of the filtered data.")
                break
            i+=5
    
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
