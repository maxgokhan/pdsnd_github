import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please type a city name of them: chicago, new york city, washington ?")
        city = city.lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("Invalid city name! Please type a city name of them: chicago, new york city, washington")
    # get user input for month (all, january, february, ... , june)
    while True:    
        month = input("Please type a specific month name or type 'all' to reach results of six months ?")
        month = month.lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("invalid month name! Please type a specific month name or type 'all' to reach results of six months")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please type a specific day name or type 'all' to reach all results ?")
        day = day.lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print("invalid month name! Please type a specific day name or type 'all' to reach all results")
    print('-'*50)
    return city, month, day


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
    # load related city file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name           
    
    # Calculate Combined Stations and Trip Durations
    df['Combined Stations'] = df['Start Station'] + ' to ' +  df['End Station']           
    
    df['Trip Duration'] = (df['End Time'] - df['Start Time']).dt.seconds    
    
    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':       
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    
    print('\nResult of the Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    comman_month = df['month'].mode()[0]
    print('Result of the Most Comman Start Month:', comman_month, "\n")
    
    comman_day_of_week = df['day_of_week'].mode()[0]
    print('Result of the Most Comman Start Day of Week:', comman_day_of_week, "\n")

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    comman_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', comman_hour, "\n")
    
    print("\nThis took %s seconds." % (time.time() - start_time), "\n")
    
    print('-'*50)


def station_stats(df):
    
    print('\nMost Popular Stations and Trip...\n')
    start_time = time.time()
      
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station, "\n")    
    
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station, "\n")
    
    df['Combined Stations'] = df['Start Station'] + " " + df['End Station']
    popular_combined_station = df['Combined Stations'].mode()[0]
    print('Result of the Most Comman Combined Station:', popular_combined_station, "\n")

    print("\nThis process took %s seconds." % (time.time() - start_time), "\n")
    
    print('-'*50)

def trip_duration_stats(df):    

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()    
    
    total_travel_time = df['Trip Duration'].sum()/3600
    print("Total Travel Duration Time: {} hours".format(total_travel_time), "\n")
    
    mean_of_travel_time = df['Trip Duration'].mean() / 60
    print("Mean Travel Duration Time: {} minutes".format(mean_of_travel_time), "\n")

    print("\nThis took %s seconds." % (time.time() - start_time), "\n")
    
    print('-'*50)

def user_stats(df,city):    

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    user_types = df["User Type"].value_counts()
    print(user_types)    
    
    if city != 'washington':
            gender = df["Gender"].value_counts()
            print(gender)            
            
            earliest_year_birth = df["Birth Year"].max()
            most_recent_year_birth = df["Birth Year"].min()
            common_year_birth = df["Birth Year"].mode()[0]
            
            print("Earliest Birth Year: {}".format(int(earliest_year_birth)))
            print("Recent Birth Year: {}".format(int(most_recent_year_birth)))
            print("Common Birth Year: {}".format(int(common_year_birth)))

            print("\nThis took %s seconds." % (time.time() - start_time))
        
    x = 1
    while True:
        raw = input('\Do you want to see any raw data? Enter yes or no.\n')
        if raw.lower() == 'yes':
            print(df[x:x+5])
            x = x+5
        else:
            break
            
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nDo you want to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
	