"""
    Usage: ./bikeshare_2.py 
    Author:
        Kyra Coyne
    Date:
        20-11-2021
"""
print('\nStarting bikeshare analysis program. We are just getting things set up for you!')

import time
import pandas as pd
import numpy as np

print('If you wish to exit at any time, use the keyboard interrupt signal (ctrl+c)')
print('Initialising datasets...')
# Python will read the file from the current directory. Ensure your files are in same dir as this script
c_df = pd.read_csv('./chicago.csv')
ny_df = pd.read_csv('./new_york_city.csv')
w_df = pd.read_csv('./washington.csv')

print('Initialisation complete')
print('-'*40)

## Variables we want globally available for use in more than one function
months = ('none', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december')
month_dict = dict(zip(months,(list(range(0,13)))))
month_dict_inverse = {k: v for v, k in month_dict.items()} # For easy lookup with the retrieved numeric month value, reverse our month dictionary

## User input here decides which database to query and how
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!\n')

    ## User input for city (chicago, new york city, washington)
    cities = {'chicago', 'new york city', 'washington'}
    city_choice_msg = 'Which city data would you like to explore?\nChoose between Chicago, New York City, and Washington: '
    city = input(city_choice_msg).lower()
    # Control for invalid user input and prompt them to retry if invalid
    while city not in cities:
        print("\n\nInvalid entry. You entered: " + city)
        print("Please enter a valid city name from the list specified.\n")
        city = input(city_choice_msg).lower()

    ##  Maybe want to offer year, day or month options for exploration? Or specific date ?
    ## User input for month (all, january, february, ... , june)
    months_str = ', '.join([month for month in months]).title()
    months_choice_msg = "Which month would you like to explore? \n\nAvailable options:\n" + months_str + "\n\nPlease select month: "
    month = input(months_choice_msg).lower()
    # Control for invalid user input and prompt them to retry if invalid
    while month not in months:
        print("\n\nInvalid entry. You entered: " + month)
        print("Please enter a valid month from the list specified.\n")
        month = input(months_choice_msg).lower()

    ## User input for day of week (all, monday, tuesday, ... sunday)
    days = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    #day_choice_str = "Would you like to explore a specific day of the week? Select all if not.\n Options are:\n" + .join([day for day in days]).title() + "\n\nPlease select day: "
    day_str = ', '.join([day for day in days]).title()
    day_choice_str = "\nWould you like to explore a specific day of the week? Select all if not.\nOptions are:\n" + day_str + "\n\nPlease select day: "
    day = input(day_choice_str).lower()
    # Control for invalid user input and prompt them to retry if invalid
    while day not in days:
        print("\n\nInvalid entry. You entered: " + day)
        print("Please enter a valid day from the list specified.\n")
        day = input(day_choice_str).lower()

    print('\nStatistics will be created using the following parameters: ' + city + ', ' + month + ', ' + day)
    print('-'*40)
    return city, month, day

## Felt ineffiecient to use load_data each time the user wanted to change parameters
## Loading data at start and then allow filtering and interrogation of desired dataset
def filter_data(city, month, day):
    """
    Filter data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    ## Get appropriate dataframe based on city selected by user
    df = {'chicago': c_df, 'new york city': ny_df, 'washington': w_df}.get(city)

    ## Output raw data for user if requested
    view_raw_data = input('Would you like to see the raw data first (y or n): ').lower()[0]

    while view_raw_data not in ('y','n'):
        print("\n\nInvalid entry. You entered: " + raw_data)
        view_raw_data = input('Would you like to see the raw data first (y or n): ').lower()[0]

    if view_raw_data == 'y':
        start_row, end_row = (0, 4)
        while view_raw_data == 'y' and end_row <= df.shape[0]:
            print(df.loc[start_row:end_row])
            start_row, end_row = (start_row+5, end_row+5)
            view_raw_data = input('Would you like to see more raw data (y or n)? ').lower()[0]
            if view_raw_data != 'y':
                break

    ## Convert start and end time columns so we can easily filter for day and month
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['End Time']=pd.to_datetime(df['End Time'])
    df['Month'] = pd.DatetimeIndex(df['Start Time']).month
    df['Day Of Week'] = pd.DatetimeIndex(df['Start Time']).strftime('%A') # Used in time_stats
    df['Start Hour'] = df['Start Time'].dt.hour # Used in time_stats
    df['Trip'] = df['Start Station'] + " - " + df['End Station'] #Used in station_stats

    ## Apply required filter
    if month != 'none':
        df = df.loc[df['Month'] == month_dict.get(month)]
    if day != 'all':
        df = df.loc[df['Day Of Week'] == day.title(),:]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        (df) The argument is the filtered dataframe created from filter_data function
    """
    print('\n\nCalculating The Most Frequent Times of Travel...\n')
    print('Note: If you selected to filter by a single month/day, the most common function is only looking at the data in your selection.\n')
    start_time = time.time()

    # value_counts will return in desc order by count - take first entry to get most common
    most_common_month = df['Month'].mode().values[0]
    most_common_month = month_dict_inverse[most_common_month].title()
    print('The most common month is: ' + str(most_common_month))

    # display the most common day of week
    most_common_day = df['Day Of Week'].mode().values[0]
    print('The most common month is: ' + most_common_day)

    # display the most common start hour
    most_common_hour = df['Start Hour'].mode().values[0]
    print('The most common start hour is: ' + str(most_common_hour) + ':00')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        (df) The argument is the filtered dataframe created from filter_data function

    The filter_data function also pre creates the Trip column for this function
    """

    print('\n\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode().values[0]
    print('The most common start station is: ' + most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode().values[0]
    print('The most common end station is: ' + most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_trip = df['Trip'].mode().values[0]
    print('The most trip is between these two stations: ' + most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is shown below (rounded to two decimal places)')
    print('Total time in seconds: ' + str(total_travel_time))
    print('Total time in minutes: ' + str(round(total_travel_time/60, 2)))
    print('Total time in hours: ' + str((round(total_travel_time/60/60, 2))))
    print('Total time in days: ' + str((round(total_travel_time/60/60/24, 2))))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nThe mean travel time is shown below')
    print('Mean time in seconds: ' + str(round(mean_travel_time, 2)))
    print('Mean time in minutes: ' + str(round(mean_travel_time/60, 2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The count per user type is shown below:')
    print(df['User Type'].value_counts())

    # Display counts of gender
    print('\nThe count per gender is shown below:')
    print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    print('\nThe oldest user\'s have the year of birth: ' + str(int(df['Birth Year'].min())))
    print('The youngest user\'s have the year of birth: ' + str(int(df['Birth Year'].max())))
    print('The most common user year of birth is: ' + str(int(df['Birth Year'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """
    This will execute each of the functions above.
    There is no input as the user input is taken from get_filters on city and if they have desired month and day filters.
    The Washington dataset does not have the data to support user_stats, so this is only calculated for NYC and Chicago
    """
    while True:
        print('Running main function')
        city, month, day = get_filters()
        df = filter_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)

        if city in ('new york city', 'chicago'):
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
