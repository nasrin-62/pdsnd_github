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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input("Please enter 'chicago', 'new york city' or 'washington': ")
        city = city.lower()
        if cities.count(city) >= 1:
            print("Your chosen city is {}!".format(city))
            break
        else:
            print("{} is not a valid city".format(city))

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march' ,'april', 'may', 'june']
    while True:
        month = input("Please enter the month of interest from january to june or 'all': ")
        month = month.lower()
        if months.count(month) >= 1:
            print("Your chosen month is {}!".format(month))
            break
        else:
            print("{} is not a valid month".format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Please enter the day of the week of interest (eg. 'monday') or 'all': ")
        day = day.lower()
        if days.count(day) >= 1:
            print("Your chosen day is {}!".format(day))
            break
        else:
            print("{} is not a valid day".format(day))

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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    df['day'] = df['Start Time'].dt.day_name()
    popular_day = df['day'].mode()[0]
    print('Most Popular Day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    df['start_station'] = df['Start Station']
    popular_start_station = df['start_station'].mode()[0]
    print('Most Popular Start station:', popular_start_station)

    # display most commonly used end station
    df['end_station'] = df['End Station']
    popular_end_station = df['end_station'].mode()[0]
    print('Most Popular End station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['combined_station'] = df['Start Station'] + ' to '+ df['End Station']
    popular_combined_station = df['combined_station'].mode()[0]
    print('Most Popular Trip is from', popular_combined_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['total_travel_time'] = pd.to_datetime(df['End Time'],format='%Y-%m-%d %H:%M:%S') - pd.to_datetime(df['Start Time'],format= '%Y-%m-%d %H:%M:%S')
    df['total_travel_time_minutes']=df['total_travel_time']/np.timedelta64(1,'m')
    total_travel_time_minutes = int(df['total_travel_time_minutes'].sum())
    print('Total travel time is', total_travel_time_minutes, 'minutes')

    # display mean travel time
    total_travel_time_minutes = round(df['total_travel_time_minutes'].mean(),2)
    print('Mean travel time is', total_travel_time_minutes, 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    if city == 'washington':
        print('There is no gender or birth year data for washington')
    else:
        # Display counts of gender
        genders = df['Gender'].value_counts()
        print(genders)

        # Display earliest, most recent, and most common year (mode) of birth
        most_recent_yob = int(df['Birth Year'].max())
        print('Most Recent Birth Year is', most_recent_yob)

        earliest_yob = int(df['Birth Year'].min())
        print('Earliest Birth Year is', earliest_yob)

        mode_yob = int(df['Birth Year'].mode())
        print('Most Common Birth Year is', mode_yob)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Asks user whether they want to see 5 lines of raw data and displays 5 rows of data.
    Continues to display 5 rows until the user decidesto exit.
    Returns:
        5 rows of raw data continuously, upon user request
    """
    # het user input ('yes' or 'no')
    yesnos = ['yes', 'no']
    #initialise row counter
    start = 0
    while True:
        if start == 0:
            yesno = input("Do you want to see 5 rows of raw data? Enter 'yes' or 'no': ")
        else:
            yesno = input("Do you want to see 5 more rows of raw data? Enter 'yes' or 'no': ")
        yesno = yesno.lower()
        if yesnos.count(yesno) >= 1:
            print("You has select value is {}!".format(yesno))
            #If user choses to exit, then exit
            if yesno == 'no':
                break
            #if user choses to display 5 rows, do so
            else:
                end = start + 5
                print(df.iloc[start:end])
                start = start + 5
        #error if user enters a value other than 'yes' or 'no'
        else:
            print("{} is not a valid value".format(yesno))

    return yesno


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        yesno = raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	   main()
