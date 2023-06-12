# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Jonathan M. Mauring Jr
# Collaborators (discussion): None
# Time: start: June 11 end:

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # calculate the best fitting line for each degree of polynomial
    models = []
    for deg in degs:
        model = pylab.polyfit(x, y, deg)
        models.append(pylab.array(model))
    
    return models
    

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    mean = sum(y) / len(y)
    error = ((y - estimated) ** 2).sum()
    variability = ((y - mean) ** 2).sum()

    return (1 - (error/variability))
    
    """ Another way of calculating for r2. """
    #mean_error = ((y - estimated) ** 2).sum() / len(y)
    #variance = pylab.var(y)

    #return (1 - (mean_error / variance))

def evaluate_models_on_training(x, y, models, plot_name=None):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        # generate predicted y-values for each models
        estimated_y = pylab.polyval(model, x)

        # calculate coefficient of determination and standar error over slope
        r2 = r_squared(y, estimated_y)
        se_slope = se_over_slope(x, y, estimated_y, model)

        # plot each models
        pylab.plot(x, y, 'b.')
        pylab.plot(x, estimated_y, 'r-')
        pylab.xlabel('Year')
        pylab.ylabel('Temperature in Celsius')
        pylab.title('Fit of degree {}, R2 = {}'.format(len(model) - 1, round(r2, 5)))
        
        if plot_name:
            pylab.savefig(plot_name + '_{}'.format(len(model) - 1))
        else:
            pylab.savefig('graph_model_{}'.format(len(model) - 1))

        if not model is model[-1]:
            pylab.figure()

    

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # get the mean temperature for each year
    yearly_means = []
    for year in years:
        city_means = []
        # get the mean temperature for each city
        for city in multi_cities:
            city_temps = climate.get_yearly_temp(city, year)
            city_mean = city_temps.sum() / len(city_temps)
            city_means.append(city_mean)

        # get the national avg temp
        year_mean = sum(city_means) / len(city_means)
        yearly_means.append(year_mean)

    # convert yearly_means list to pylab.array
    return pylab.array(yearly_means)

    
def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # TODO
    pass

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # TODO
    pass

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # TODO
    pass

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    pass

if __name__ == '__main__':

    # climate data
    climate = Climate('data.csv')
    CITY = 'NEW YORK'
    DEGREE = [1]

    # Part A.4 - I. Daily Temperature
    # generate data sample (daily temp [Jan 10] in New York)
    MONTH = 1
    DAY = 10
    x, y = [], []

    for year in TRAINING_INTERVAL:
        x.append(year)
        y.append(climate.get_daily_temp(CITY, MONTH, DAY, year))

    x = pylab.array(x)
    y = pylab.array(y)

    # fit the data sample to a degree one polynomial
    models = generate_models(x, y, DEGREE)

    # plot the data and the model 
    evaluate_models_on_training(x, y, models, plot_name='daily_temp_NY')


    # Part A.4 - II. Annual Temperature
    # generate data sample (annual temperature in New York)
    x = []
    year_avgs = []

    for year in TRAINING_INTERVAL:
        temperatures = climate.get_yearly_temp(CITY, year)
        year_avgs.append(temperatures.sum() / len(temperatures))
        x.append(year)

    x = pylab.array(x)
    year_avgs = pylab.array(year_avgs)
    
    # fit the data sample to a degree one polynomial
    models = generate_models(x, year_avgs, DEGREE)

    # plot the data and the model
    evaluate_models_on_training(x, year_avgs, models, plot_name='annual_temp_NY')


    # Part B
    # generate data sample
    x = [year for year in TRAINING_INTERVAL]
    yearly_means = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    x = pylab.array(x)
    yearly_means = pylab.array(yearly_means)

    # fit the data sample to a degree one polynomial
    models = generate_models(x, yearly_means, DEGREE)

    # plot the data and the model
    evaluate_models_on_training(x, yearly_means, models, plot_name='national_temp')

    # Part C
    # TODO: replace this line with your code

    # Part D.2
    # TODO: replace this line with your code

    # Part E
    # TODO: replace this line with your code
