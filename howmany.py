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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city= input('please enter city name : ')
        if city not in ('new york city', 'chicago','washington'):
           print('not a valid response')
        else: 
           break   
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month= input('please enter a month : ')
        if month not in ('january', 'february','march','april','may','june'):
            print('not a valid response')
        else: 
             break 

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day= input('please enter a day : ')
        if day not in ('monday', 'tuesday','wednesday','thursday','friday','saturday'):
            print('not a valid response')
        else: 
            break    
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df=df.dropna(axis = 0, how ='any')
    df=df.dropna().reset_index(drop=True)
    print(df)
    

    # convert the Start Time column t9=o datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        # filter by month to create the new dataframe
        df = df[df['month']== month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']== day.title()]
    

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('most common month: ',df['month'].median())

    # TO DO: display the most common day of week
    print('most common day of the week: ',df['day_of_week'].median())

    # TO DO: display the most common start hour
    print('most common hour: ',df['Start Time'].dt.hour.median())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print(df['Start Station'].value_counts().idxmax())

    # TO DO: display most commonly used end station
    print(df['End Station'].value_counts().idxmax())
    # TO DO: display most frequent combination of start station and end station trip
    print('most common combination of start and stop:',df.groupby(['Start Station'])['End Station'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('total travel time: ',df['Trip Duration'].sum().sum())

    # TO DO: display mean travel time
    print('mean travel time: ',df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    countusert=df['User Type'].value_counts()
    print('counts of user types :',countusert)

    # TO DO: Display counts of gender
    print('counts od gender:',df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
    print('earliest year of birth:',df['Birth Year'].min(),' most recent year of birth:',df['Birth Year'].max(),'most common year of birth:',df['Birth Year'].median())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()