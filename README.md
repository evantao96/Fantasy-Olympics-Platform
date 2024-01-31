# Fantasy Olympics Game

## About ##

This project is a web application in which users are able to create an account and
play a simulated Olympic Games with each other. 

In the game, users select up to 10 real Olympic athletes for some set of events. The athletes are each given a performance score by the algorithm. The total scores for each player are compared, and the player with the highest score wins; scores are added to a global leaderboard for players who agree to doing so. 

The game makes use of Olympic data for athletes, events and countries; athlete
biographies from [Wikipedia](https://wikipedia.org/); and weather data from [WeatherUnderground](https://wunderground.com/).

This game provides a platform for fans of the Olympics to engage with their favorite athletes and participate more in Olympics sporting events through fantasy play. The game also encourages Olympics fans to learn about lesser known athletes and events.

## Schema ##

Player 
+----+------+-----------+-------+
| id | name | team_name | ready |
+----+------+-----------+-------+
|  1 | Evan | evantao   |     1|
+----+------+-----------+-------+

## Testing ##

To start the application, run `npm install` in the project directory to install any dependencies, then run: 

`npm start`

## Modules and Architecture ##

- For the frontend, `VueJS` along with `HTML` and `CSS` was used in order to display the
application, as well as the data from the server. 
- Since this is a single-page application, the `Axios` javascript library was used to issue `AJAX` requests to interface with the server.
- For the backend, the `Express` framework on top of `NodeJS` was used to handle connections from clients and send queries to the database.
- Amazon `AWS RDS` was used to host the `MySQL` database and `DynamoDB` as a `NoSQL` database.
