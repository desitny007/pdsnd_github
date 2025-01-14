import time
import pandas as pd
import numpy as np

# Constants for valid cities, months, and days
VALID_CITIES = ['chicago', 'new york city', 'washington']
VALID_MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
VALID_DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

# Dictionary mapping city names to their corresponding CSV file names
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_user_input(prompt, valid_options):
    """Get user input and validate against valid options."""
    user_input = ''
    while user_input not in valid_options:
        user_input = input(prompt).lower()
        if user_input not in valid_options:
            print("Invalid input. Please try again.")
    return user_input

def get_filters():
    """Asks user to specify a city, month, and day to analyze."""
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = get_user_input("Please enter a city (chicago, new york city, washington): ", VALID_CITIES)
    month = get_user_input("Please enter a month (all, january, february, march, april, may, june): ", VALID_MONTHS)
    day = get_user_input("Please enter a day of the week (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday): ", VALID_DAYS)

    print('-' * 40)
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
    # Load the data for the specified city
    if city == 'chicago':
        df = pd.read_csv('chicago.csv')
    elif city == 'new york city':
        df = pd.read_csv('new_york_city.csv')
    elif city == 'washington':
        df = pd.read_csv('washington.csv')
    else:
        raise ValueError("City not found. Please choose from 'chicago', 'new york city', or 'washington'.")

    # Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from 'Start Time'
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        # Convert month name to month number
        month = month.lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1  # Get month number (1-12)
        df = df[df['month'] == month_index]  # Filter the DataFrame by month

    # Filter by day if applicable
    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day.lower()]  # Filter the DataFrame by day

    return df  # Return the filtered DataFrame


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    month_mode = df['month'].mode()
    if not month_mode.empty:
        most_common_month = month_mode[0]
        print('Most Common Month:', most_common_month)
    else:
        print('No data available to determine the most common month.')

    # Display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', most_common_day)

    # Display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display the most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', most_common_start_station)

    # Display the most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', most_common_end_station)

    # Display the most frequent combination of start station and end station trip
    most_frequent_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Frequent Combination of Start and End Station Trip:', most_frequent_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum() / 60  # Convert to minutes
    print('Total Travel Time:', total_travel_time, 'Minutes')

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 60  # Convert to minutes
    print('Mean Travel Time:', mean_travel_time, 'Minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print("Counts of User Types:\n", user_type_counts)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:\n", gender_counts)
    else:
        print("\nGender data is not available.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        
        print("\nEarliest Year of Birth:", earliest_year)
        print("Most Recent Year of Birth:", most_recent_year)
        print("Most Common Year of Birth:", most_common_year)
    else:
        print("\nBirth Year data is not available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

# Display raw data upon user request
def display_raw_data(df):
    index = 0
    while index < len(df):
        user_input = input("Do you want to see 5 lines of raw data? (yes/no): ").strip().lower()
        if user_input == 'yes':
            # Display the next 5 lines of raw data
            print(df.iloc[index:index + 5])
            index += 5  # Move to the next set of 5 lines
        elif user_input == 'no':
            print("Exiting the data display.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    while True:
        city, month, day = get_filters()  # Get user input for city, month, and day
        df = load_data(city, month, day)  # Load the data for the specified city and filters
        time_stats(df)  # Display time statistics
        station_stats(df)  # Display station statistics
        trip_duration_stats(df)  # Display trip duration statistics
        user_stats(df)  # Display user statistics
        display_raw_data(df)  # Optionally display raw data

        restart = input('\nWould you like to restart? Enter yes or no.\n')  # Ask if the user wants to restart
        if restart.lower() != 'yes':
            break  # Exit the loop if the user does not want to restart

if __name__ == "__main__":
    main()  # Call the main function to start the program
