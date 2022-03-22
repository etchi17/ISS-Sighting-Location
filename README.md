# Querying Data on ISS Locations Around the World

In this project, we are given two data sets to work with, one containing the positonal and velocity data of the ISS and the other containing sighting data of the ISS from specific citiess in the United States. Our goal is to better sort and represent the data stored by using a Flask application to query and return information from the ISS data set. We would then aim to containerize the Flask application by making a Docker image from a Dockerfile that we would execute using a Makefile. We also made a unit test to test all of the functions and routes used in the Flask application to ensure that they worked correctly. All of these steps exist to allow us to better sort and analyze large and complex sets of data. With the evergrowing prevalence of large data sets, having to sift through it all could pose a daunting, yet important task. Thus we aim to facilitate this task by providing methods that breakdown the data sets layer by layer, improving the user's understanding and accessibilty of them.

## Downloading Original Data

In order to start using this application, you're first going to need the data sets to work with. In this project we specifically work with two data sets:

### ISS Positional and Velocity Data:
- This can be downloaded by first visiting https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq
- Right click the `XML` button below the header "Public Distribution File" and click on "Copy link address"
- In a separate directory on your command line terminal, execute the command `wget` followed by the link you just copied that you can paste by right clicking. Alternatively, you can also execute the command:
```    
wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml
```

### ISS Sighting Data:
- This data can also be downloaded by visiting https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq
- Right click the `XML` button below the header "XMLsightingData_citiesUSA02" and click on "Copy link address"
- In that same directory on your command line terminal, execute the command `wget` followed by the link you just copied that you can paste by right clicking. Alternatively, you can also execute the command:
```
wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA02.xml
```

## Building the Container from Dockerfile

1. In order to build the container from a Dockerfile, we're going to need to add 2 new files to our directory:

	### Dockerfile:
	- This file is already included in the repository, but if you would like to create your own...
	- Touch a file named "Dockerfile" into your directory by executing `touch Dockerfile`
	- Go in and edit the newly created file with a text editor of your choice (vim was used as the text editor of choice) by executing `vim Dockerfile`
	- Once inside enter the following lines of code to complete building the Dockerfile:
	```
	FROM python:3.9

	RUN pip3 install --user xmltodict
	RUN mkdir /app
	WORKDIR /app
	COPY requirements.txt /app/requirements.txt
	RUN pip install -r /app/requirements.txt
	COPY . /app

	ENTRYPOINT ["python"]
	CMD ["app.py"]
	```

	### requirements.txt:
	- Touch a file named "requirements.txt" into your directory by inputting `touch requirements.txt`
	- Open the newly created file with a text editor with `vim requirements.txt`
	- Add the following line of code and exit out of the file: `Flask==2.0.3`

2. Once those files have been added to your directory, you can build the container by running the following command:
	```
	docker build -t <username>/<code>:<version> .
	```
	NOTE: Be sure to replace `<username>` with your Docker Hub username, `<code>` with the name of your code, and `<version>` with the name of your version of choice.

3. Once built, you can then run the docker container you just built by executing the command:
	```
	docker run --name "container-name" -d -p <port#>:5000 <username>/<code>:<version>
	```
	NOTE: Be sure to replace `<port#>` with your own port number and `"container-name"` with a name of your choice

5. Finally, you can push your working container into Docker hub with:
	```
	docker push <username>/<code>:<version>
	```

Alternatively, you can compress the commands done above (after creating the Dockerfile and requirements.txt file) into one:

2. Create a Makefile:

	### Makefile:
	- This file is also already included in the repository, but if you would like to create your own...
	- Touch a file named "Makefile" into your directory by executing `touch Makefile`
	- Go in and edit the newly created file with a text editor of your choice by executing `vim Makefile`
	- Once inside enter the following lines of code to complete building the Makefile:
	```
	#NAME ?= <username>

	all: build run push

	images:
		docker images | grep <username>

	ps:
		docker ps -a | grep <username>

	build:
		docker build -t <username>/<code>:<version> .

	run:
		docker run --name "iss-sighting-location" -d -p <port#>:5000 <username>/<code>:<version>

	push:
		docker push <username>/<code>:<version>
	```

3. You can then run the commands under build, run, and push by executing `make all`. By doing so, you have now successfully built and ran your container. 

You can check if it is up and running with `docker ps -a`, which should output a table of the format displayed below.
```
CONTAINER ID   IMAGE                         COMMAND           CREATED         STATUS             PORTS                                             NAMES
(Container ID) <username>/<code>:<version>   "python app.py"   (time created)  Up (time created)  0.0.0.0:<port#>->5000/tcp, :::<port#>->5000/tcp   "container-name"
```
You should see your container with the name you gave it on the table generated with the STATUS as Up and the port you assigned it.

If any of the above is not found, you can try to debug it using: 
```
docker logs "container-name"
```

## Pulling a Working Container from Docker Hub

1. To pull a working container from Docker hub, simply execute the command:
	```
	docker pull <username>/<code>:<version>
	```

2. Now that you have successfully pulled the container, you can run it using the command used in the previous section under __Building the Container from Dockerfile__

## Interacting with Routes in Application

1. Start off by executing the command `curl localhost:5007/` to return a string containing all routes in the Flask application, how to use them, and their expected outputs:
```
### ISS Sighting Location ###

Informational and Management Routes:

/                                                      (GET) print this information
/read_data                                             (POST) resets data, reads and loads all data from files

Routes for Querying Positional and Velocity Data:

/epochs                                                (GET) lists all epochs in positional and velocity data
/epochs/<epoch>                                        (GET) lists all data associated with a specific <epoch> in positional and velocity data

Routes for Querying Sighting Data

/countries                                             (GET) lists all countries in sighting data
/countries/<country>                                   (GET) lists all data associated with a specific <country> in sighting data
/countries/<country>/regions                           (GET) lists all regions in a specific <country> in sighting data
/countries/<country>/regions/<region>                  (GET) lists all data associated with a specific <region> in a specific <country> in sighting data
/countries/<country>/regions/<region>/cities           (GET) lists all cities in a specific <region> in a specific <country> in sighting data
/countries/<country>/regions/<region>/cities/<city>    (GET) lists all data associated with a specific <city> in a specific <region> in a specific <country> in sighting data
```

2. Before you can use any of the routes to query the data, you have to read in the data first with: `curl localhost:5007/read_data -X POST`

3. After doing so, you can now utilize the routes to query data by entering them after `curl localhost:5007/`

### Example
Input: `curl localhost:5007/countries/United_States/regions/California/cities/Los_Angeles`

Output:
```
Los_Angeles, California, United_States
ISS was spotted on Tue Feb 15/05:45 AM for 4 minutes at a max elevation of 15, entering 10 above SSE, exiting 10 above E, with utc offset: -8.0, utc time: 13:45, and utc date: Feb 15, 2022
ISS was spotted on Thu Feb 17/05:44 AM for 7 minutes at a max elevation of 52, entering 10 above SSW, exiting 10 above ENE, with utc offset: -8.0, utc time: 13:44, and utc date: Feb 17, 2022
ISS was spotted on Fri Feb 18/04:58 AM for 5 minutes at a max elevation of 26, entering 16 above S, exiting 10 above ENE, with utc offset: -8.0, utc time: 12:58, and utc date: Feb 18, 2022
ISS was spotted on Sat Feb 19/04:12 AM for 1 minutes at a max elevation of 13, entering 13 above ESE, exiting 10 above E, with utc offset: -8.0, utc time: 12:12, and utc date: Feb 19, 2022
ISS was spotted on Sat Feb 19/05:45 AM for 6 minutes at a max elevation of 42, entering 15 above WSW, exiting 10 above NNE, with utc offset: -8.0, utc time: 13:45, and utc date: Feb 19, 2022
ISS was spotted on Sun Feb 20/05:00 AM for 3 minutes at a max elevation of 74, entering 74 above NNE, exiting 10 above NE, with utc offset: -8.0, utc time: 13:00, and utc date: Feb 20, 2022
ISS was spotted on Mon Feb 21/04:14 AM for 1 minutes at a max elevation of 15, entering 15 above ENE, exiting 10 above ENE, with utc offset: -8.0, utc time: 12:14, and utc date: Feb 21, 2022
ISS was spotted on Mon Feb 21/05:47 AM for 4 minutes at a max elevation of 17, entering 13 above WNW, exiting 10 above NNE, with utc offset: -8.0, utc time: 13:47, and utc date: Feb 21, 2022
ISS was spotted on Tue Feb 22/05:01 AM for 2 minutes at a max elevation of 22, entering 22 above N, exiting 10 above NNE, with utc offset: -8.0, utc time: 13:01, and utc date: Feb 22, 2022
ISS was spotted on Wed Feb 23/04:15 AM for < 1 minutes at a max elevation of 10, entering 10 above NE, exiting 10 above NE, with utc offset: -8.0, utc time: 12:15, and utc date: Feb 23, 2022
ISS was spotted on Thu Feb 24/05:01 AM for < 1 minutes at a max elevation of 11, entering 11 above N, exiting 10 above N, with utc offset: -8.0, utc time: 13:01, and utc date: Feb 24, 2022
```

## Interpreting Return Values

#### Routes:
1. `/`
	1. Returns a large string detailing all routes in the Flask application, how to use them, and the information they return
	2. Output shown in beginning of __Interacting with Routes in Application__

2. `/read_data`
	1. Returns a short string indicating the successful completion of reading the two data sets
	2. Output: `Data has been read from file`
	
3. `/epochs`
 	1. Returns a large string listing all epochs in positional and velocity data
 	2. Output:
 	```
 	...
	2022-057T11:12:56.869Z
	2022-057T11:16:56.869Z
   	2022-057T11:20:56.869Z
	2022-057T11:24:56.869Z
	2022-057T11:28:56.869Z
	2022-057T11:32:56.869Z
	2022-057T11:36:56.869Z
	2022-057T11:40:56.869Z
	2022-057T11:44:56.869Z
	2022-057T11:48:56.869Z
	2022-057T11:52:56.869Z
	2022-057T11:56:56.869Z
	2022-057T12:00:00.000Z
	```

4. `/epochs/<epoch>`
	1. Returns a dictionary listing all positional (X, Y, Z) and velocity (X_DOT, Y_DOT, Z_DOT) data for a specific epoch
	2. Output for `/epochs/2022-057T12:00:00.000Z`: 
	```
	{
	  "X": {
	    "#text": "6626.5027288478996",
	    "@units": "km"
	  },
	  "X_DOT": {
	    "#text": "-0.48760287876274999",
	    "@units": "km/s"
	  },
	  "Y": {
	    "#text": "-824.23928357807699",
	    "@units": "km"
	  },
	  "Y_DOT": {
	    "#text": "4.9312583060242199",
	    "@units": "km/s"
	  },
	  "Z": {
	    "#text": "-1255.3633426653601",
	    "@units": "km"
	  },
	  "Z_DOT": {
	    "#text": "-5.8454326130222896",
	    "@units": "km/s"
	  }
	}
	```
	
5. `/countries`
 	1. Returns a dictionary listing all countries in the sighting data as the key with the number of sightings in that country as the value
 	2. Output:
 	```
	{
	  "United_States": 5476
	}
	```
	
6. `/countries/<country>`
	1. Returns a large string listing all the data associated with a specific country in the sighting data
	2. Output for `/countries/United_States`:
	```
	...
	New_Port_Richey, Florida: ISS was spotted on Sat Feb 19/05:39 AM for 3 minutes at a max elevation of 67, entering 67 above N, exiting 10 above NE, with utc offset: -5.0, utc time: 10:39, and utc date: Feb 19, 2022
	New_Port_Richey, Florida: ISS was spotted on Sun Feb 20/04:54 AM for < 1 minutes at a max elevation of 12, entering 12 above NE, exiting 10 above NE, with utc offset: -5.0, utc time: 09:54, and utc date: Feb 20, 2022
	New_Port_Richey, Florida: ISS was spotted on Sun Feb 20/06:27 AM for 2 minutes at a max elevation of 12, entering 11 above WNW, exiting 10 above NNW, with utc offset: -5.0, utc time: 11:27, and utc date: Feb 20, 2022
	New_Port_Richey, Florida: ISS was spotted on Mon Feb 21/05:41 AM for 1 minutes at a max elevation of 15, entering 15 above N, exiting 10 above N, with utc offset: -5.0, utc time: 10:41, and utc date: Feb 21, 2022
	New_Smyrna_Beach, Florida: ISS was spotted on Mon Feb 14/06:25 AM for 4 minutes at a max elevation of 16, entering 10 above SSE, exiting 10 above E, with utc offset: -5.0, utc time: 11:25, and utc date: Feb 14, 2022
	New_Smyrna_Beach, Florida: ISS was spotted on Wed Feb 16/06:24 AM for 7 minutes at a max elevation of 64, entering 10 above SSW, exiting 10 above NE, with utc offset: -5.0, utc time: 11:24, and utc date: Feb 16, 2022
	New_Smyrna_Beach, Florida: ISS was spotted on Thu Feb 17/05:37 AM for 6 minutes at a max elevation of 29, entering 11 above S, exiting 10 above ENE, with utc offset: -5.0, utc time: 10:37, and utc date: Feb 17, 2022
	New_Smyrna_Beach, Florida: ISS was spotted on Fri Feb 18/04:52 AM for 2 minutes at a max elevation of 15, entering 15 above ESE, exiting 10 above E, with utc offset: -5.0, utc time: 09:52, and utc date: Feb 18, 2022
	New_Smyrna_Beach, Florida: ISS was spotted on Fri Feb 18/06:25 AM for 6 minutes at a max elevation of 31, entering 10 above WSW, exiting 10 above NNE, with utc offset: -5.0, utc time: 11:25, and utc date: Feb 18, 2022
	New_Smyrna_Beach, Florida: ISS was spotted on Sat Feb 19/05:40 AM for 3 minutes at a max elevation of 63, entering 63 above NW, exiting 10 above NE, with utc offset: -5.0, utc time: 10:40, and utc date: Feb 19, 2022
	New_Smyrna_Beach, Florida: ISS was spotted on Sun Feb 20/04:54 AM for 1 minutes at a max elevation of 16, entering 16 above NE, exiting 10 above NE, with utc offset: -5.0, utc time: 09:54, and utc date: Feb 20, 2022
	New_Smyrna_Beach, Florida: ISS was spotted on Sun Feb 20/06:27 AM for 2 minutes at a max elevation of 11, entering 10 above NW, exiting 10 above NNW, with utc offset: -5.0, utc time: 11:27, and utc date: Feb 20, 2022
	New_Smyrna_Beach, Florida: ISS was spotted on Mon Feb 21/05:41 AM for 1 minutes at a max elevation of 17, entering 17 above NNW, exiting 10 above N, with utc offset: -5.0, utc time: 10:41, and utc date: Feb 21, 2022
	```
	
7. `/countries/<country>/regions` 
	1. Returns a dictionary listing all regions in the sighting data for a specified country as the key with the number of sightings in that region as the value
 	2. Output for `/countries/United_States/regions`:
 	```
	{
	  "California": 1702,
	  "Colorado": 1173,
	  "Connecticut": 657,
	  "DC": 1060,
	  "Delaware": 100,
	  "Florida": 784
	}
	```
	
8. `/countries/<country>/regions/<region>` 
	1. Returns a large string listing all the data associated with a specific region in a specific country in the sighting data
	2. Output for `/countries/United_States/regions/California`:
	```
	...
	Yuba_City: ISS was spotted on Wed Feb 23/05:48 AM for 4 minutes at a max elevation of 21, entering 18 above NW, exiting 10 above NNE, with utc offset: -8.0, utc time: 13:48, and utc date: Feb 23, 2022
	Yuba_City: ISS was spotted on Thu Feb 24/05:01 AM for 2 minutes at a max elevation of 25, entering 25 above N, exiting 10 above NE, with utc offset: -8.0, utc time: 13:01, and utc date: Feb 24, 2022
	Yuba_City: ISS was spotted on Fri Feb 25/04:15 AM for < 1 minutes at a max elevation of 10, entering 10 above NE, exiting 10 above NE, with utc offset: -8.0, utc time: 12:15, and utc date: Feb 25, 2022
	Yuba_City: ISS was spotted on Fri Feb 25/05:48 AM for 3 minutes at a max elevation of 13, entering 11 above NW, exiting 10 above NNE, with utc offset: -8.0, utc time: 13:48, and utc date: Feb 25, 2022
	Yucca_Valley: ISS was spotted on Tue Feb 15/05:45 AM for 5 minutes at a max elevation of 18, entering 10 above S, exiting 10 above E, with utc offset: -8.0, utc time: 13:45, and utc date: Feb 15, 2022
	Yucca_Valley: ISS was spotted on Thu Feb 17/05:45 AM for 7 minutes at a max elevation of 64, entering 10 above SW, exiting 10 above NE, with utc offset: -8.0, utc time: 13:45, and utc date: Feb 17, 2022
	Yucca_Valley: ISS was spotted on Fri Feb 18/04:58 AM for 5 minutes at a max elevation of 31, entering 17 above S, exiting 10 above ENE, with utc offset: -8.0, utc time: 12:58, and utc date: Feb 18, 2022
	Yucca_Valley: ISS was spotted on Sat Feb 19/04:12 AM for 1 minutes at a max elevation of 16, entering 16 above ESE, exiting 10 above E, with utc offset: -8.0, utc time: 12:12, and utc date: Feb 19, 2022
	Yucca_Valley: ISS was spotted on Sat Feb 19/05:45 AM for 6 minutes at a max elevation of 36, entering 12 above WSW, exiting 10 above NNE, with utc offset: -8.0, utc time: 13:45, and utc date: Feb 19, 2022
	Yucca_Valley: ISS was spotted on Sun Feb 20/05:00 AM for 3 minutes at a max elevation of 69, entering 68 above NW, exiting 10 above NE, with utc offset: -8.0, utc time: 13:00, and utc date: Feb 20, 2022
	Yucca_Valley: ISS was spotted on Mon Feb 21/04:14 AM for 1 minutes at a max elevation of 19, entering 19 above ENE, exiting 10 above NE, with utc offset: -8.0, utc time: 12:14, and utc date: Feb 21, 2022
	Yucca_Valley: ISS was spotted on Mon Feb 21/05:47 AM for 4 minutes at a max elevation of 15, entering 11 above WNW, exiting 10 above N, with utc offset: -8.0, utc time: 13:47, and utc date: Feb 21, 2022
	Yucca_Valley: ISS was spotted on Tue Feb 22/05:01 AM for 2 minutes at a max elevation of 21, entering 21 above NNW, exiting 10 above NNE, with utc offset: -8.0, utc time: 13:01, and utc date: Feb 22, 2022
	Yucca_Valley: ISS was spotted on Wed Feb 23/04:15 AM for < 1 minutes at a max elevation of 11, entering 11 above NNE, exiting 10 above NNE, with utc offset: -8.0, utc time: 12:15, and utc date: Feb 23, 2022
	Yucca_Valley: ISS was spotted on Thu Feb 24/05:01 AM for < 1 minutes at a max elevation of 10, entering 10 above NNW, exiting 10 above N, with utc offset: -8.0, utc time: 13:01, and utc date: Feb 24, 2022
	```
9. `/countries/<country>/regions/<region>/cities`
	1. Returns a dictionary listing all cities in the sighting data for a specified region in a specified country as the key with the number of sightings in that city as the value
 	2. Output for `/countries/United_States/regions/California/cities`:
 	```
	{
	  "Lemoore": 11,
	  "Livermore": 11,
	  "Lompoc": 10,
	  "Long_Beach": 11,
	  "Los_Altos": 11,
	  "Los_Angeles": 11,
	  "Los_Gatos": 10,
	  "Madera": 10,
	  "Magalia": 12,
	  "Manteca": 12,
	  "Manzanar_National_Historic_Site": 13,
	  "Marina": 10,
	  ...
	}
	
10. `/countries/<country>/regions/<region>/cities/<city>`
	1. Returns a large string listing all the data associated with a specific city in a specific region of a specific country in the sighting data
	2. Output for `/countries/United_States/regions/California/cities/Los_Angeles` shown as example at end of __Interacting with Routes in Application__
	

## Citations (MLA)

Goodwin, S. (n.d.). ISS_COORDS_2022-02-13. NASA. https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml Retrieved March 17, 2022, from https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq

Goodwin, S. (n.d.). XMLsightingData_citiesUSA02. NASA. Retrieved March 17, 2022, from https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA02.xml
