from flask import Flask
import xmltodict
import logging
import socket

app = Flask(__name__)

iss_epoch_data = {}
iss_sighting_data = {}
format_str=f'[%(asctime)s {socket.gethostname()}] %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=format_str)

@app.route('/read_data', methods=['POST'])
def read_data_from_file_into_dict() -> str:
    """
    Reads in 2 XML data files (ISS.OEM_J2K_EPH.xml and XMLsightingData_citiesUSA02.xml) and stores them as 2 global dictionaries accessible by all other routes. Returns a string confirming that all the data has been read from the files.

    Returns:
        output (string): Short string confirming all the XML files have been read and stored into dictionaries.
    """
    logging.info('Data is being read')
    global iss_epoch_data
    global iss_sighting_data

    with open( 'ISS.OEM_J2K_EPH.xml' , 'r') as f:
        iss_epoch_data = xmltodict.parse(f.read())

    with open('XMLsightingData_citiesUSA02.xml' , 'r') as f:
        iss_sighting_data = xmltodict.parse(f.read())

    return f'Data has been read from file\n'

@app.route('/', methods=['GET'])
def help() -> str:
    """
    Outputs a string containing information on how to interact with this application. Details information on how to use each route as well as what each route does and outputs.

    Returns:
        help_txt (string): Large string detailing all useable routes, their purpose, and their outputs.
    """
    logging.info('Outputting information on how to interact with application')
    help_txt = "\n### ISS Sighting Location ###\n\n"
    help_txt = help_txt + "Informational and Management Routes:\n\n"
    help_txt = help_txt + "/                                                      (GET) print this information\n"
    help_txt = help_txt + "/read_data                                             (POST) resets data, reads and loads all data from files\n\n"
    help_txt = help_txt + "Routes for Querying Positional and Velocity Data:\n\n"
    help_txt = help_txt + "/epochs                                                (GET) lists all epochs in positional and velocity data\n"
    help_txt = help_txt + "/epochs/<epoch>                                        (GET) lists all data associated with a specific <epoch> in positional and velocity data\n\n"
    help_txt = help_txt + "Routes for Querying Sighting Data\n\n"
    help_txt = help_txt + "/countries                                             (GET) lists all countries in sighting data\n"
    help_txt = help_txt + "/countries/<country>                                   (GET) lists all data associated with a specific <country> in sighting data\n"
    help_txt = help_txt + "/countries/<country>/regions                           (GET) lists all regions in a specific <country> in sighting data\n"
    help_txt = help_txt + "/countries/<country>/regions/<region>                  (GET) lists all data associated with a specific <region> in a specific <country> in sighting data\n"
    help_txt = help_txt + "/countries/<country>/regions/<region>/cities           (GET) lists all cities in a specific <region> in a specific <country> in sighting data\n"
    help_txt = help_txt + "/countries/<country>/regions/<region>/cities/<city>    (GET) lists all data associated with a specific <city> in a specific <region> in a specific <country> in sighting data\n\n"
    return help_txt

@app.route('/read_data', methods=['GET'])
def read_data_help() -> str:
    """
    Outputs string detailing how to use the /read_data POST method route correctly. Returns information about that route and instructions on how to use it.

    Result:
        help_txt (string): Short string providing instructions on how to use /read_data POST method route correctly.
    """
    logging.warning('Wrong command used')
    help_txt = "\nThis is a route for resetting and laoding stored data. You must perform a POST request to this route to get it to work:\ncurl localhost:5007/read_data -X POST\n\n"
    return help_txt

@app.route('/epochs', methods=['GET'])
def get_all_epochs() -> str:
    """
    Iterates through all state vectors in iss_epoch_data global dictionary, pulling all values associated with 'EPOCH' key in each state vector and storing them in a large string. Returns the string containing all 'EPOCH' values.

    Returns:
        epoch (string): Large string listing all epoch values
    """
    logging.info('Querying epochs route')
    epoch = ""
    for i in range(len(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'])):
        epoch = epoch + iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH'] + '\n'
    return epoch

@app.route('/epochs/<epoch>', methods=['GET'])
def get_epoch_data(epoch: str) -> dict:
    """
    Iterates through all state vectors in iss_epoch_data global dictionary, comparing inputted <epoch> to each value associated with the 'EPOCH' key in each state vector until the values match. Once found, it creates a dictionary containing the positional and velocity data in the same state vector as the matching epoch and returns that dictionary.
    
    Args:
        epoch (string): A string containing the specific epoch value to acquire data of.

    Returns:
        epoch_dict (dictionary): A dictionary containing the positional and velocity data for the specific epoch.
    """
    logging.info('Querying epochs/'+ epoch +' route')
    pos_vel_data = ['X', 'Y', 'Z', 'X_DOT', 'Y_DOT', 'Z_DOT']
    epoch_dict = {}
    for i in range(len(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'])):
        if epoch == iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH']:
            for j in pos_vel_data:
                epoch_dict[j] = iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][i][j]
            break
    return epoch_dict

@app.route('/countries', methods=['GET'])
def get_all_countries() -> dict:
    """
    Iterates through all visible pass in iss_sighting_data global dictionary, pulling all values associated with 'country' key in each visible pass and storing each unique country in a dictionary as a key. Counts how many times a country is found in the entire data set and stores that as the value for the respective country key, returning that dictionary as an output.

    Returns:
        country (dictionary): A dictionary containing all countries in the sighitng data and how many times they show up.
    """
    logging.info('Querying countries route')
    country = {}
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        j = iss_sighting_data['visible_passes']['visible_pass'][i]['country']
        if j in country:
            country[j] += 1
        else:
            country[j] = 1
    return country

@app.route('/countries/<country>', methods=['GET'])
def get_country_data(country: str) -> str:
    """
    Iterates through all visible pass in iss_sighting_data global dictionary, comparing the inputted <country> to each value associated with the 'country' key in each visible pass until the values match. Once found, it creates and outputs a string containing all information associated with that country.

    Args:
        country (string): A string containing the specific country to acquire data of.

    Returns:
        country_data (string): A large string containing all information (sighting data for each visible pass) for the specific country.
    """
    logging.info('Querying countries/'+ country +' route')
    country_data = country + "\n"
    country_info = ['city', 'region', 'spacecraft', 'sighting_date', 'duration_minutes', 'max_elevation', 'enters', 'exits', 'utc_offset', 'utc_time', 'utc_date']
    str_trans = [', ', ': ', ' was spotted on ', ' for ', ' minutes at a max elevation of ', ', entering ', ', exiting ', ', with utc offset: ', ', utc time: ', ', and utc date: ', '']
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        if country == iss_sighting_data['visible_passes']['visible_pass'][i]['country']:
            country_info2 = []
            for k in country_info:
                country_info2.append(iss_sighting_data['visible_passes']['visible_pass'][i][k])
            info_and_trans = [info + trans for info, trans in zip(country_info2, str_trans)]
            for j in info_and_trans:
                country_data = country_data + str(j)
            country_data = country_data + "\n"
    return country_data

@app.route('/countries/<country>/regions', methods=['GET'])
def get_all_regions(country: str) -> dict:
    """
    Iterates through all visible pass in iss_sighting_data global dictionary that include the inputted <country>, pulling all values associated with the 'region' key in each visible pass and storing each unique region in a dictionary as a key. Counts how many times a region is found in the data and stores that as the value for the respective region key, returning that dictionary as an output.

    Args:
        country (string): A string containing the specific country to find the regions of.

    Returns:
        region (dictionary): A dictionary containing all regions in a specific country in the sighitng data and how many times they show up.
    """
    logging.info('Querying countries/'+ country +'/regions route')
    region = {}
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        if country == iss_sighting_data['visible_passes']['visible_pass'][i]['country']:
            j = iss_sighting_data['visible_passes']['visible_pass'][i]['region']
            if j in region:
                region[j] += 1
            else:
                region[j] = 1
    return region

@app.route('/countries/<country>/regions/<region>', methods=['GET'])
def get_region_data(country: str, region: str) -> str:
    """
    Iterates through all visible pass in iss_sighting_data global dictionary that include the inputted <country>, comparing the inputted <region> to each value associated with the 'region' key in each visible pass until the values match. Once found, it creates and outputs a string containing all information associated with that region.

    Args:
        country (string): A string containing the specific country to find the region of.
        region (string): A string containing the specific region in the specific country to acquire data of.

    Returns:
        region_data (string): A large string containing all information (sighting data for each visible pass) for a specific region in a specific country.
    """
    logging.info('Querying countries/'+country+'/regions/'+region+' route')
    region_data = region + ", " + country + "\n"
    region_info = ['city', 'spacecraft', 'sighting_date', 'duration_minutes', 'max_elevation', 'enters', 'exits', 'utc_offset', 'utc_time', 'utc_date']
    str_trans = [': ', ' was spotted on ', ' for ', ' minutes at a max elevation of ', ', entering ', ', exiting ', ', with utc offset: ', ', utc time: ', ', and utc date: ', '']
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        if country == iss_sighting_data['visible_passes']['visible_pass'][i]['country']:
            if region == iss_sighting_data['visible_passes']['visible_pass'][i]['region']:
                region_info2 = []
                for k in region_info:
                    region_info2.append(iss_sighting_data['visible_passes']['visible_pass'][i][k])
                info_and_trans = [info + trans for info, trans in zip(region_info2, str_trans)]
                for j in info_and_trans:
                    region_data = region_data + str(j)
                region_data = region_data + "\n"
    return region_data

@app.route('/countries/<country>/regions/<region>/cities', methods=['GET'])
def get_all_cities(country: str, region: str) -> dict:
    """
    Iterates through all visible pass in iss_sighting_data global dictionary that include the inputted <country> and inputted <region>, pulling all values associated with the 'city' key in each visible pass and storing each unique city in a dictionary as a key. Counts how many times a city is found in the data and stores that as the value for the respective city key, returning that dictionary as an output.

    Args:
        country (string): A string containing the specific country to find the region of.
        region (string): A string containing the specific region in the specific country to find the cities of.

    Returns:
        city (dictionary): A dictionary containing all cities in a specific region of a specific country in the sighting data and how many times they show up.
    """
    logging.info('Querying countries/'+ country +'/regions/'+ region +'/cities route')
    city = {}
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        if country == iss_sighting_data['visible_passes']['visible_pass'][i]['country']:
            if region == iss_sighting_data['visible_passes']['visible_pass'][i]['region']:
                j = iss_sighting_data['visible_passes']['visible_pass'][i]['city']
                if j in city:
                    city[j] += 1
                else:
                    city[j] = 1
    return city

@app.route('/countries/<country>/regions/<region>/cities/<city>', methods=['GET'])
def get_city_data(country: str, region: str, city: str) -> str:
    """
    Iterates through all visible pass in iss_sighting_data global dictionary that include the inputted <country> and inputted <region>, comparing the inputted <city> to each value associated with the 'city' key in each visible pass until the values match. Once found, it creates and outputs a string containing all information associated with that city.

    Args:
        country (string): A string containing the specific country to find the region of.
        region (string): A string containing the specific region to find the city of.
        city (string): A string containing the specific city to acquire data of.

    Returns:
        city_data (string): A large string containing all information (sighting data for each visible pass) for a specific city in a specific region of a specific country.
    """
    logging.info('Querying countries/'+ country +'/regions/'+ region +'/cities/' + city +' route')
    city_data = city + ", " + region + ", " + country + "\n"
    city_info = ['spacecraft', 'sighting_date', 'duration_minutes', 'max_elevation', 'enters', 'exits', 'utc_offset', 'utc_time', 'utc_date']
    str_trans = [' was spotted on ', ' for ', ' minutes at a max elevation of ', ', entering ', ', exiting ', ', with utc offset: ', ', utc time: ', ', and utc date: ', '']
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        if country == iss_sighting_data['visible_passes']['visible_pass'][i]['country']:
            if region == iss_sighting_data['visible_passes']['visible_pass'][i]['region']:
                if city == iss_sighting_data['visible_passes']['visible_pass'][i]['city']:
                    city_info2 = []
                    for k in city_info:
                        city_info2.append(iss_sighting_data['visible_passes']['visible_pass'][i][k])
                    info_and_trans = [info + trans for info, trans in zip(city_info2, str_trans)]
                    for j in info_and_trans:
                        city_data = city_data + str(j)
                    city_data = city_data + "\n"
    return city_data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
