Getting started with kot1
=====
A library of weather forecast accessing data from the OpenWeatherAPI.


Introduction
----
The library needs internet access and you need to get an API key from https://openweathermap.org/api. Simply sign up, login, and go to API Keys to copy your API key. See the Getting Started section for where to input your API key in the code.

Installing the Library
----------
You can install the package with:

.. code:: bash

    pip install kot1


Using the library
----------

.. code:: python

    # Create a weather object providing the city and the api key which you can get after signing up at https://openweathermap.org/api
    >>> weather = Weather(city = "Madrid", apikey = '26631f0f41b95fb9f5ac0df9a8f43c92')

    # Get the complete weather data for the next 12 hours at a 3-hour resolution, as a dictionary
    >>> weather.next_12h()

    # Get simplified weather data for the next 12 hours at a 3-hour resolution, as a string
    >>> weather.next_12h_simplified()