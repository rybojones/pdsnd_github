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
        try:
            city = str(input('Enter the name of the city to filter by.  Choices include: Chicago, New York City or Washington.\nCity : ')).lower()

            # raise an error if the input does not match expected input
            if city not in ['chicago', 'new york city', 'washington']:
                raise ValueError

            #print the selection the user has made
            print('\nYou have selected', city.title(),'\n')

            break
        except:
            print('Not a valid input for city.')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input('Enter the name of the month to filter by.  Choices include: January, February, March, April, May, June or All.\nMonth : ')).lower()

            # raise an error if the input does not match expected input
            if month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
                raise ValueError

            #print the selection the user has made
            print('\nYou have selected', month.title())
            print()

            break
        except:
            print('Not a valid input for month.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day_of_week = str(input('Enter the day of week to filter by.  Choices include: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All.\nDay of Week : ')).lower()

            # raise an error if the input does not match expected input
            if day_of_week not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
                raise ValueError

            #print the selection the user has made
            print('\nYou have selected', day_of_week.title())
            print()

            break
        except:
            print('Not a valid input for day of week.')

    print('-'*40)
    return city, month, day_of_week


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])   #loads correct CSV file even if camelCase is used

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']

        # filter by month to create the new dataframe
        df = df[df['month'] == months.index(month) + 1]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def show_raw_data(df):
    """ Prompt the user a question asking whether or not they would like to see 5 lines of raw data and continues this prompt until the user says 'no' """

    while True:
        # use a for loop in similar fashion as a generator function to repeatedly print the subsequent 5 rows of data for as long as the user inputs 'yes'
        for i in range(0, df.shape[0], 5):
            # get the user input to display the next five rows until the user inputs 'no'
            while True:
                try:
                    raw_input = input('\nWould you like to display 5 lines of raw data? Enter yes or no.\n').lower()

                    # raise an error if the input does not match expected input
                    if raw_input not in ['yes', 'no']:
                        raise ValueError
                    break
                except:
                    print('Not a valid input.')

            # break the while loop if the user chooses not to display the raw data
            if raw_input != 'yes':
                break
            else:
                # print the 'next' five rows of the dataframe
                print(df[i:i + 5])
        break


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    months = ['January', 'February', 'March', 'April', 'May', 'June']

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The month most frequently traveled during:', months[df['month'].mode()[0] - 1])

    # display the most common day of week
    print('The day of week most frequently traveled during:', days_of_week[days_of_week.index(df['day_of_week'].mode()[0])])

    # display the most common start hour
    print('The starting hour most frequently traveled during:', df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('The most commonly used end station:', df['End Station'].mode()[0])

    # create a new column in the dataframe that represents a combination of the 'Start Station' and 'End Station' for each user experience/trip
    df['Station Combo'] = ('Start: ' + df['Start Station'] + ', End: ' + df['End Station'])

    # display most frequent combination of start station and end station trip
    print('The most frequent trip (combination of start station and end station):\n{}'.format(df['Station Combo'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # calculate total travel time in seconds
    total_time = df['Trip Duration'].sum()

    # convert the total travel time (in seconds) to days, hours, minutes, seconds
    days = total_time / (24.0 * 60 * 60)
    hours = (days -int(days)) * 24
    minutes = (hours - int(hours)) * 60
    seconds = (minutes - int(minutes)) * 60

    # display total travel time
    print('Total Travel Time :', int(days), 'days', int(hours), 'hours,', int(minutes), 'minutes', int(seconds), 'seconds')

    # calucalate mean travel time
    mean_time = df['Trip Duration'].mean()

    # convert mean travel time (in seconds) to hours, minutes, seconds
    hours = mean_time / (60.0 * 60.0)
    minutes = (hours - int(hours)) * 60
    seconds = (minutes - int(minutes)) * 60

    # print the mean travel time
    print('Mean Travel Time :', int(hours), 'hours,', int(minutes), 'minutes', int(seconds), 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts for user types:\n{}'.format(df['User Type'].dropna().value_counts()))
    print()

    # Display counts of gender
    # check that there is information on gender in the dataframe
    if 'Gender' in df:
        print('Counts of users by gender:\n{}'.format(df['Gender'].value_counts()))
        print()

    # Display earliest, most recent, and most common year of birth
    # Check that there is information on birth year in the dataframe
    if 'Birth Year' in df:
        print('The earliest year of birth for all users:', int(df['Birth Year'].min()))
        print('The most recent year of birth for all users:', int(df['Birth Year'].max()))
        print('The most common year of birth for all users:', int(df['Birth Year'].dropna().mode()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        show_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # check that the user response is valid
        while True:
            try:
                restart = input('\nWould you like to restart? Enter yes or no.\n')

                # raise an error if the input does not match expected input
                if restart.title() not in ['Yes', 'No']:
                    raise ValueError
                break
            except:
                print('Not a valid input.')

        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
