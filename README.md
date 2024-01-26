# foot-sensor-app
Final project for the Python Programming and Data Visualisation course.

## How to run?

1. Connect to the EE VPN.

2. Build docker container:
```
$ docker build -t foot-sensor-app .
```

3. Run docker container:
```
$ docker run --name foot-sensor-app -d -p 80:8080 foot-sensor-app
```

4. Access the app at `localhost`.

5. To stop the container:
```
$ docker stop foot-sensor-app
```

6. To restart the container:
```
$ docker start foot-sensor-app
```