var express = require('express');
var mysql = require('mysql');
var connection = mysql.createConnection({
    host: 'cis550project-mysql.cbhtjg5oqf7i.us-east-2.rds.amazonaws.com',
    user: 'apoth',
    password: 'susandavidson',
    port: '3306',
    database: 'olympics'
});
var AWS = require("aws-sdk");
AWS.config.update({
    accessKeyId: "AKIAJ5WMW63CXERVBTCA",
    secretAccessKey: "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",
    "region": "us-east-2"
});
var docClient = new AWS.DynamoDB.DocumentClient();
var async = require('async');
var router = express.Router();

var temp;
var humd;

var isEmpty = function(obj) {
    for (var key in obj) {
        if (obj.hasOwnProperty(key))
            return false;
    }
    return true;
}

router.post('/', function(req, res, next) {
    var chosenEvents = JSON.parse(req.body.chosenEvents);
    console.log(chosenEvents);
    async.map(chosenEvents, getAthletes, function(err, data) {
        if (err) {
            console.log(err);
            res.send({ success: false });
        } else {
            docClient.get({ TableName: "Game_State", Key: { 'id': 1 } }, function(err, state) {
                if (err) {
                    console.error("Error:", JSON.stringify(err, null, 2));
                    res.send({ success: false });
                } else {
                    res.send({
                        success: true,
                        payload: data,
                        location: {
                            city: state.Item.city,
                            country: state.Item.country
                        },
                        date: {
                            day: state.Item.day,
                            month: state.Item.month,
                            year: state.Item.year
                        },
                        weather: {
                            temp: state.Item.temperature,
                            humd: state.Item.humd
                        }
                    });
                }
            });
        }
    });
});

var getAthletes = function(id, callback) {
    connection.query(`SELECT id, name, bio FROM indAthlete
        INNER JOIN Athlete_Participates
        ON indAthlete.id=Athlete_Participates.athlete_id
        WHERE Athlete_Participates.event_id= ? AND
        (country_id = 'USA'
        OR country_id = 'URS' OR country_id = 'GBR' OR country_id = 'FRA'
        OR country_id = 'GER' OR country_id = 'ITA' OR country_id = 'SWE'
        OR country_id = 'AUS' OR country_id = 'HUN' OR country_id = 'NED'
        OR country_id = 'JPN' OR country_id = 'CAN' OR country_id = 'CHN'
        OR country_id = 'RUS' OR country_id = 'NOR' OR country_id = 'DEN'
        OR country_id = 'ROU' OR country_id = 'POL' OR country_id = 'KOR'
        OR country_id = 'ESP')
        AND bio <> 'N/A'
        AND indAthlete.id NOT IN ( SELECT athlete_id FROM Player_Drafts_Athlete )`, [id],
        function(err, athletes, fields) {
            connection.query(`SELECT name FROM Event WHERE id = ?`, [id], function(err, rows, fields) {
                callback(err, { eventId: id, eventName: rows[0].name, athletes: athletes });
            })
        });
}

/* POST Athlete score */
router.post('/scores', function(req, res, next) {
    var chosenAthletes = JSON.parse(req.body.chosenAthletes);
    var name = req.body.name;
    var teamName = req.body.teamName;
    var pub = req.body.public;

    connection.query(`SELECT id FROM Player WHERE name=? AND team_name=?`, [name, teamName],
        function(err, results) {
            if (err) {
                console.log(err);
                res.send({ success: false })
            } else {
                var playerId = results[0].id
                async.each(chosenAthletes, function(ids, callback) {
                    connection.query(`INSERT INTO Player_Drafts_Athlete
                    SET athlete_id=?, event_id=?, player_id=?`, [ids.athleteId, ids.eventId, playerId],
                        function(err, res) {
                            if (err) {
                                var athleteId = ids.athleteId;
                                callback({ error: err, athleteId: athleteId });
                            } else {
                                callback(err);
                            }
                        })
                }, function(err) {
                    if (err) {
                        console.log(err.error);
                        connection.query(`SELECT name FROM indAthlete WHERE id=?`, [err.athleteId], function(err, results) {
                            if (err) {
                                res.send({ success: false });
                            } else {
                                console.log(results);
                                res.send({ success: false, athlete: results[0].name })
                            }
                        });
                    } else {
                        async.map(chosenAthletes, getScore, function(err, scores) {
                            if (err) {
                                console.log(err);
                                res.send({ "success": false })
                            } else {
                                console.log(scores);

                                p_score = 0;
                                for (var i = 0; i < scores.length; i++) {
                                    p_score += scores[i].points;
                                }

                                console.log(p_score);
                                var params = {
                                    TableName: "Player_Info",
                                    Key: {
                                        "name": name,
                                        "team_name": teamName
                                    },
                                    UpdateExpression: "SET score = :score",
                                    ExpressionAttributeValues: {
                                        ":score": p_score
                                    },
                                    ReturnValues: "ALL_NEW"
                                };

                                docClient.update(params, function(err, data) {
                                    if (err) {
                                        console.error("Unable to update table. Error JSON:", JSON.stringify(err, null, 2));
                                    } else {
                                        console.log("UpdateItem succeeded:", JSON.stringify(data, null, 2));
                                    }
                                });

                                if (pub) {
                                    docClient.scan({ TableName: 'Leaderboard' }, function(err, data) {
                                        if (err) console.log(err);
                                        else {
                                            console.log(data);
                                            var highScores = data.Items.slice();

                                            // Delete all high scores
                                            async.each(highScores, function(highScore, callback) {
                                                docClient.delete({
                                                    TableName: 'Leaderboard',
                                                    Key: { rank: highScores.rank }
                                                }, function(err, data) {
                                                    callback(err);
                                                });
                                            }, function(err) {
                                                highScores.push({ rank: 0, team_name: teamName, score: p_score })
                                                highScores.sort(function(a, b) {
                                                    if (a.score < b.score) {
                                                        return 1;
                                                    } else if (a.score > b.score) {
                                                        return -1;
                                                    }

                                                    return 0;
                                                });

                                                // Find new Top 10
                                                highScores = highScores.slice(0, 10);

                                                // Add Top 10 to Leaderboard
                                                for (var i = 1; i <= highScores.length; i++) {
                                                    var rank = i;
                                                    docClient.put({
                                                        TableName: 'Leaderboard',
                                                        Item: {
                                                            rank: rank,
                                                            team_name: highScores[rank - 1].team_name,
                                                            score: highScores[rank - 1].score
                                                        }
                                                    }, function(err, data) {
                                                        if (err) console.log(err);
                                                    });
                                                }
                                            });
                                        }
                                    });
                                }
                                res.send({ "scores": scores, "success": true });
                            }
                        });
                    }
                });
            }
        });
});


var getScore = function(ids, callback) {

    console.log(temp);
    console.log(humd);

    connection.query(`SELECT p.medal, a.name, c.weather, e.name as ename 
        FROM indAthlete a 
        INNER JOIN Athlete_Participates p
        ON p.athlete_id=a.id
        INNER JOIN Country c
        ON c.id=a.country_id
        INNER JOIN Event e
        ON e.id=p.event_id
        WHERE athlete_id=? AND event_id=?`, [ids.athleteId, ids.eventId], function(err, rows, fields) {
        var medal = rows[0].medal;
        var points = Math.ceil(Math.random() * (medal * 10 + 5)) + 5;

        var clim;

        if ((temp / 60.1) > (humd / 69.5)) {
            if (temp > 60.1) clim = 'hot';
            else clim = 'cold';
        } else {
            if (humd > 69.5) clim = 'wet';
            else clim = 'dry';
        }

        if (rows[0].weather = clim) {
            points += Math.ceil(Math.random() * 5);
        } else {
            points += Math.floor(Math.random() * 5) - 2;
        }

        callback(err, { name: rows[0].name, points: points, ename: rows[0].ename });
    });
}



router.get('/weather', function(req, res, next) {
    docClient.get({ TableName: "Game_State", Key: { 'id': 1 } }, function(err, data) {
        if (err) {
            console.error("Error:", JSON.stringify(err, null, 2));
            res.send({ success: false });
            return;
        } else {
            var day;
            var month;
            var year;
            var city;
            var country;

            if (isEmpty(data)) {
                day = Math.ceil(Math.random() * 28);
                month = Math.random() > 0.5 ? 1 : 6;
                year = Math.ceil(Math.random() * 2) + 2013;
                cities = [
                    ["Athens", "Greece"],
                    // ["London", "United Kingdom"],
                    ["Paris", "France"],
                    // ["St Louis", "United States"],
                    ["Stockholm", "Sweden"],
                    ["Amsterdam", "Netherlands"],
                    ["Berlin", "Germany"],
                    ["Helsinki", "Finland"],
                    ["Melbourne", "Australia"],
                    ["Rome", "Italy"],
                    ["Seoul", "South Korea"],
                    ["Barcelona", "Spain"],
                    ["Beijing", "China"]
                ];
                cityCountry = cities[Math.floor(Math.random() * cities.length)];
                city = cityCountry[0];
                country = cityCountry[1];

                docClient.put({
                    TableName: "Game_State",
                    Item: { "id": 1, "month": month, "day": day, "year": year, "city": city, "country": country }
                }, function(err, data) {
                    if (err) { console.error("Error:", JSON.stringify(err, null, 2)); }
                });
            } else {
                day = data.Item.day;
                month = data.Item.month;
                year = data.Item.year;
                city = data.Item.city;
                country = data.Item.country;
            }

            console.log(day);
            console.log(month);
            console.log(year);
            console.log(city);
            console.log(country);

            connection.query(`SELECT Temp, Humidity from Weather
                WHERE city=? AND country=? AND day=? AND month=? AND year=?`, [city, country, day, month, year],
                function(err, rows, fields) {
                    console.log(rows[0]);
                    temp = rows[0].Temp;
                    humd = rows[0].Humidity;

                    docClient.update({
                        TableName: "Game_State",
                        Key: {
                            "id": 1
                        },
                        UpdateExpression: "SET temperature = :temperature",
                        ExpressionAttributeValues: {
                            ":temperature": temp
                        },
                        ReturnValues: "ALL_NEW"
                    }, function(err, data) {
                        if (err) console.log(err);
                        docClient.update({
                            TableName: "Game_State",
                            Key: {
                                "id": 1
                            },
                            UpdateExpression: "SET humd = :humd",
                            ExpressionAttributeValues: {
                                ":humd": humd
                            },
                            ReturnValues: "ALL_NEW"
                        }, function(err, data) {
                            if (err) console.log(err);
                        });
                    });
                    res.send({
                        success: true,
                        location: {
                            city: city,
                            country: country
                        },
                        date: {
                            day: day,
                            month: month,
                            year: year
                        },
                        weather: {
                            temp: temp,
                            humd: humd
                        }
                    });
                });
        }
    });
});

module.exports = router;
