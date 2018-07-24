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

    # get user input for city (chicago, new york city, washington).
    city = ''
    while city not in ['chicago', 'new york city', 'washington']:
        city = input('\nEnter city name to explore the data Ex (chicago, new york city, washington): \n')
        city = city.lower().strip()

    # get user input for month (all, january, february, ... , june)
    months = ['january','february','march','april','may','june','all']
    month = ''
    while month not in months:
        month = input('\nEnter a month between January to June or all : \n')
        month = month.lower().strip()
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_in_week = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']
    day = ''
    while day not in day_in_week:
        day = input('\nEnter a day between sunday to saturday or all : \n')
        day = day.lower().strip()
        
    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time']) # converting start time to datetime 
    df['month'] = df['Start Time'].dt.month # extract month from the datetime output being 1 = january so on
    df['day_of_week'] = df['Start Time'].dt.weekday_name # extract day name of the week
    df['hour'] = df['Start Time'].dt.hour # extract hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Calculate & Display statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    
    # Calculate the most common month
    popular_month = df['month'].mode()[0] # returns the numeric value for the month
    popular_month_name = months[popular_month - 1].title() # returns the name of the month
    print('The most popular month of travel is : {}'.format(popular_month_name))

    # Calculate the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most popular day of the week for travel is : {}'.format(popular_day))

    # Calculate the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular start hour is : {}'.format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Calculate & Display statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('This is the most common Start station : {}'.format(popular_start_station))

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('This is the most common End station : {}'.format(popular_end_station))

    # Disply most frequent combination of start station and end station trip
    trip_combination = df.groupby(['Start Station','End Station'])['Trip Duration'].count().idxmax()
    print('This is the most frquent trip from {} to {}'.format(trip_combination[0],trip_combination[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def calculate_time(time_sec):
    """convert time in secs to days hours minutes and seconds"""
    days = time_sec // (3600 * 24)
    hours = time_sec % (3600 * 24) // 3600
    minutes = time_sec % 3600 // 60
    seconds = time_sec % 60
    return ('{} days {} hours {} minutes {} seconds'.format(int(days),int(hours),int(minutes),int(seconds)))

    
def trip_duration_stats(df):
    """Calculate & Display statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is : {}'.format(calculate_time(total_travel_time)))

    # Calculate mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time is : {}'.format(calculate_time(mean_travel_time)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Calculate & Display statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Calculate counts of user types
    user_type = df['User Type'].value_counts()
    print('The count of user types :\n{}'.format(user_type))

    # Calculate counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('\nThe count of user gender :\n{}'.format(gender_count))
    else:
        print('Sorry no data available for Gender')

    # Calculate earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nEarliest year of birth : year', df['Birth Year'].min().astype('int64'))
        print('Recent year of birth : year', df['Birth Year'].max().astype('int64'))
        print('Common year of birth : year', df['Birth Year'].mode()[0].astype('int64'))
    else:
        print('Sorry no data available for year of birth')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Display raw data of Bikeshare for individual user"""
    raw_info = ''
    start = 0
    stop = 5
    while raw_info != 'no':
        raw_info = input('Would you like to see the data for individual users? Enter yes or no.\n')
        if raw_info.lower().strip() == 'yes':
            for i in range(start,stop):
                print('\n{}'.format(df.iloc[i].drop(df.columns[0]).fillna('data not available')))
            start += 5
            stop += 5
        elif raw_info.lower().strip() != 'no':
            print("\nplease enter yes or no \n")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        
        # get user input if they want to run the program again.
        restart = ''
        while restart not in ['yes', 'no']:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            restart = restart.lower().strip()
        
        if restart == 'yes':
            print('\nrestarting program\n')
            
        elif restart == 'no':
            print('\nprogram terminated\n')
            break

if __name__ == "__main__":
    main()
