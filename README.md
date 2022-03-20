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
- In that same directory on your command line terminal, execute the command `wget` followed by the link you just copied that you can paste by right clicking. Alternatively, you can also execute the command:
```
wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA02.xml
```

### Building the Container from Dockerfile

In order to build the container from a Dockerfile, we're going to need to add 2 new files to our directory:

#### Dockerfile:
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

#### requirements.txt:

A simple text file that the Dockerfile uses on execution.
- Touch a file named "requirements.txt" into your directory by inputting `touch requirements.txt`
- Open the newly created file with a text editor with `vim requirements.txt`
- Add the following line of code and exit out of the file: `Flask==2.0.3`

Once those files have been added to your directory, you can build the container by running the following command:
```
docker build -t <username>/<code>:<version> .
```
NOTE: Be sure to replace `<username>` with your Docker Hub username, `<code>` with the name of your code, and `<version>` with the name of your version of choice.

Once built, you can then run the docker container you just built by executing the command:
```
docker run --name "container-name" -d -p <port#>:5000 <username>/<code>:<version>
```
NOTE: Be sure to replace `<port#>` with your own port number and `"container-name"` with a name of your choice

Finally, you can push your working container into Docker hub with:
```
docker push <username>/<code>:<version>
```
Once all of that is done, you have now successfully built and ran your container.

Alternatively, you can compress the commands done above (after creating the Dockerfile and requirements.txt file) into one by creating a Makefile:
#### Makefile:
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

You can then run the commands under build, run, and push by executing `make all`

By doing so, you have now successfully built and ran your container.

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

### Pulling a Working Container from Docker Hub
To pull a working container from Docker hub, simply execute the command:
```
docker pull <username>/<code>:<version>
```

Now that you have successfully pulled the container, you can run it using the command used in the previous section under __Building the Container from Dockerfile__

###


###

### Citations (MLA)

Goodwin, S. (n.d.). ISS_COORDS_2022-02-13. NASA. https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml Retrieved March 17, 2022, from https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq

Goodwin, S. (n.d.). XMLsightingData_citiesUSA02. NASA. Retrieved March 17, 2022, from https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA02.xml
