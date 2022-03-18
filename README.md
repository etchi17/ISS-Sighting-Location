## Querying Data on ISS Locations Around the World

In this project, we are given two data sets to work with, one containing the positonal and velocity data of the ISS and the other containing sighting data of the ISS from specific citiess in the United States. Our goal is to better sort and represent the data stored by using a Flask application to query and return information from the ISS data set. We would then aim to containerize the Flask application by making a Docker image from a Dockerfile that we would execute using a Makefile. We also made a unit test to test all of the functions and routes used in the Flask application to ensure that they worked correctly. All of these steps exist to allow us to better sort and analyze large and complex sets of data. With the evergrowing prevalence of large data sets, having to sift through it all could pose a daunting, yet important task. Thus we aim to facilitate this task by providing methods that breakdown the data sets layer by layer, improving the user's understanding and accessibilty of them.

### Downloading Original Data

In order to start using this application, you're first going to need the data sets to work with. In this project we specifically work with two data sets:

#### ISS Positional and Velocity Data:
- This can be downloaded by first visiting https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq
- Right click the `XML` button below the header "Public Distribution File" and click on "Copy link address"
- In a separate directory on your command line terminal, execute the command `wget` followed by the link you just copied that you can paste by right clicking. Alternatively, you can also execute the command:
```    
wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml
```

#### ISS Sighting Data:
- This data can also be downloaded by visiting https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq
- Right click the `XML` button below the header "XMLsightingData_citiesUSA02" and click on "Copy link address"
- In a separate directory on your command line terminal, execute the command `wget` followed by the link you just copied that you can paste by right clicking. Alternatively, you can also execute the command:
```
wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA02.xml
```

### Building the Container fron Dockerfile


###
###
###
###
###
