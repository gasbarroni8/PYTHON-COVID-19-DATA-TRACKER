#This (.py) handles the display of data.
#When user makes a selection on the main.py, they are directed to this script upon the ['Next'] button click.

#For reference, please remember that the countries are associated with an integer value, that is specific to each country.
#Where, [USA = 0, CANADA = 1, FRANCE = 2, U.K = 3, SPAIN = 4, ITALY = 5, WORLDWIDE = 6]

import json
import os
import requests
import fileManager

#Each country is associated with it's own API request url.

#The API documentation for Postman has different 'slug' urls for each country.
countrySlug = {0: "united-states",
               1: "canada",
               2: "france",
               3: "united-kingdom",
               4: "spain",
               5: "italy"}

def display(countryCode):
    slug = countrySlug.get(countryCode)

    #TODO Check to see if data is already written to local json
    #TODO otherwise obtain new data from API


    #Fetch most recent data from Covid19 API and update the JSON directory
    response = requests.get("https://api.covid19api.com/live/country/" + countrySlug.get(countryCode))
    __parseJson(response.json())

    #print(response.text.encode('utf8'))


#Reformats the returned json and organizes information into subdirectories
def __parseJson(data):

    #Get country name
    country = data[0]["Country"]
    __parseCountry(country)

    provinces = []
    [provinces.append(value["Province"]) for value in data if(value["Province"] not in provinces)]

    # dates = []
    # [dates.append(value["Date"]) for value in data if(value["Date"] not in dates)]

def __parseCountry(country):
    #Check if country's directory exists, if not, create it
    fileManager.mkdir(f"JSON/Countries/{country}")

    #Check if countries json file exists, if not, create it
    fileManager.jsonPreset("JSON/countries.json","countries")

    #Load existing countries.json file
    countrieslist = fileManager.readList("JSON/countries.json","countries")

    #Check if the countries list already contains the country file path
    iscontained = False
    for countryinfodict in countrieslist:
        if(countryinfodict["country"] is country): iscontained = True

    #If the country isn't contained append the new country's dict to the countries list
    if not iscontained:
        #Create the json file for the given country
        filename = country.lower().replace(" ","-")
        fileManager.jsonPreset(f"JSON/Countries/{country}/{filename}.json","provinces")

        newinfodict = {"country":country,"file":f"JSON/Countries/{country}/{filename}.json"}
        countrieslist.append(newinfodict)

    #Rewrite the json file
    fileManager.writeList("JSON/countries.json","countries",countrieslist)

def __parseProvinces(provinces):
    pass




display(0)