import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    city = input ("Would you Like to see data for Chicago, New York, or Washington? \n")
    while city.lower() not in ["chicago", "new york", "washington"]:
        city = input ("Please enter a valid city name: Chicago, New York, or Washington \n")
    city = city.lower()

    time_filter = input ("Would you Like to filter the data by month, day, both, or not at all? Type 'none' for no time filter. \n")
    while time_filter.lower() not in ["month", "day", "both", "none"]:
        time_filter = input ("Please enter a valid filter: month, day, both or none. \n")

    if time_filter.lower() == "month":
        month = input ("Which month? January, February, March, April, May or June? \n")
        while month.lower() not in ["january", "february", "march", "april", "may", "june"]:
            month = input ("Please enter a valid month name: January, February, March, April, May or June \n")
        day = "all"
        month = month.lower()
    elif time_filter.lower() == "day":
        day = input ("Which day? Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday or Friday? \n")
        while day.lower() not in ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]:
            day = input ("Please enter a valid day name: Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday or Friday \n")
        month = "all"
        day = day.lower()
    elif time_filter.lower() == "both":
        month = input ("Which month? January, February, March, April, May or June? \n")
        while month.lower() not in ["january", "february", "march", "april", "may", "june"]:
            month = input ("Please enter a valid month name: January, February, March, April, May or June \n")
        day = input ("Which day? Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday or Friday? \n")
        while day.lower() not in ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]:
            day = input ("Please enter a valid day name: Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday or Friday \n")
        month = month.lower()
        day = day.lower()
    else:
        month = "all"
        day = "all"


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
    df['Start Time'] = pd.to_datetime(df["Start Time"])
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day:', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station']+ "," + df['End Station']
    start = df['trip'].mode()[0].split(",")[0]
    end = df['trip'].mode()[0].split(",")[1]
    print ("The most frequent trip is from: '{}' to '{}'" .format(start,end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = sum (df['Trip Duration'])
    print('Total Travel Time:', total_travel_time/3600, " hours")
    # display mean travel time
    mean_travel_time = total_travel_time / len(df['Trip Duration'])
    print ('Mean Travel Time:', mean_travel_time/60, " minutes")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    try:
        user_gender = df['Gender'].value_counts()
        print(user_gender)
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = min(df['Birth Year'])
        most_recent_birth_year = max(df['Birth Year'])
        most_common_birth_year = df['Birth Year'].mode()[0]
        print ('Most Recent Birth Year:', int(most_recent_birth_year))
        print ('Earliest Birth Year:', int(earliest_birth_year))
        print ('Most Common Birth Year:', int(most_common_birth_year))
    except:
        print ("There are no gender or Birth Year data available for Washington")


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
        x = 0
        y = 5
        while True:
            raw_data = input ('\nWould you like to load 5 rows of the data? Enter yes or no.\n')
            if raw_data.lower() != 'yes':
                break

            print (df.iloc[x:y,0:7])
            x += 5
            y += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
