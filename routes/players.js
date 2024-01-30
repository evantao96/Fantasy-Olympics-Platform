var express = require('express');
var mysql = require('mysql');
var crypto = require('crypto');
var connection = mysql.createConnection({
    host: 'database-1.c32yscgymlt6.us-east-1.rds.amazonaws.com',
    user: 'evantao',
    password: 'rubyonrails',
    database: 'db1',
    port: '3306'
});
var router = express.Router();

var AWS = require("aws-sdk");

AWS.config.update({
    accessKeyId: "AKIAU6GDZDU357P3X2N4",
    secretAccessKey: "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",
    "region": "us-east-1"
});

var docClient = new AWS.DynamoDB.DocumentClient();

var sortScores = function(a, b) {
    if (a.score === undefined && b.score === undefined) {
        return 0;
    }
    if (a.score === undefined || a.score < b.score) {
        return 1;
    } else if (b.score === undefined || a.score > b.score) {
        return -1;
    }

    return 0;
}

router.get('/', function(req, res, next) {
    query = "SELECT COUNT(id) FROM Player;"
    connection.query(query, function(err, results) {
        if (err) {
            console.log(err);
            res.send({ "success": false });
        } else {
            var num_players = results[0]["COUNT(id)"];
            res.send({ "success": true, "exists": num_players > 0 })
        }
    });
});

router.post('/', function(req, res, next) {
    query = "SELECT count(*) FROM Player where name=? and team_name=?";
    connection.query(query, [req.body.name, req.body.teamName], function(err, results) {
        if (err) {
            console.log(err);
            res.send({ "success": false, "duplicate": false });
        } else if (results[0]["count(*)"] == 1) {
            res.send({ "success": false, "duplicate": true });
        } else {
            query2 = "INSERT INTO Player SET name=?, team_name=?, ready=?;"
            connection.query(query2, [req.body.name, req.body.teamName, true], function(err, results) {
                if (err) {
                    console.log(err);
                    res.send({ "success": false, "duplicate": false });
                } else {
                    res.send({ "success": true, "duplicate": false });
                    var params = {
                        TableName: "Player_Info",
                        Item: {
                            "name": req.body.name,
                            "team_name": req.body.teamName,
                            "passwd": crypto.createHash('md5').update(req.body.passwd).digest('hex')
                        }
                    };

                    docClient.put(params, function(err, data) {
                        if (err) {
                            console.error("Unable to create table. Error JSON:", JSON.stringify(err, null, 2));
                        } else {
                            console.log("UpdateItem succeeded:", JSON.stringify(data, null, 2));
                        }
                    });
                }
            });
        }
    });
});



router.post('/login', function(req, res, next) {
    query = "SELECT name, team_name from Player WHERE name=? and team_name = ?;"
    connection.query(query, [req.body.lname, req.body.lteamName, true], function(err, results) {
        if (err) {
            console.log(err);
            res.send({ "success": false });
        } else if (results[0] == null)
            res.send({ "success": false });
        else {
            var params = {
                TableName: "Player_Info",
                Key: {
                    "name": req.body.lname,
                    "team_name": req.body.lteamName
                }
            };

            docClient.get(params, function(err, data) {
                if (err) {
                    console.error("Unable to get table. Error JSON:", JSON.stringify(err, null, 2));
                } else if (data.Item.passwd === crypto.createHash('md5').update(req.body.lpasswd).digest('hex')) {
                    console.log("GetItem succeeded:", JSON.stringify(data, null, 2));
                    res.send({ "success": true });
                } else res.send({ "success": false });
            });
        }
    });
});

router.get('/scores', function(req, res, next) {
    docClient.scan({ TableName: 'Player_Info' }, function(err, data) {
        if (err) console.log(err);
        else {
            data.Items.sort(sortScores);
            console.log(data);
            res.send({ success: true, players: data.Items })
        }
    });
});

router.get('/scores/clear', function(req, res, next) {
    docClient.scan({ TableName: 'Player_Info' }, function(err, data) {
        if (err) console.log(err);
        else {
            console.log(data);

            // Only clear player scores if there is a score to clear
            if (data.Items.filter(function(el) {
                    return el.score !== undefined;
                }).length > 0) {
                for (var i = 0; i < data.ScannedCount; i++) {
                    var player = data.Items[i];
                    console.log(player);
                    var params = {
                        TableName: "Player_Info",
                        Key: {
                            "name": player.name,
                            "team_name": player.team_name
                        },
                        UpdateExpression: "REMOVE score",
                        ReturnValues: "ALL_NEW"
                    };
                    docClient.update(params, function(err, data) {
                        if (err) console.log(err);
                    });
                }

                docClient.delete({ TableName: "Game_State", Key: { id: 1 } }, function(err, data) {
                    if (err) console.log(err);
                });

                connection.query(`DELETE FROM Player_Drafts_Athlete`, function(err, res) {
                    if (err) console.log(err);
                })
            }

            res.send({ success: true });
        }
    });
})

router.get('/scores/top', function(req, res, next) {
    docClient.scan({ TableName: 'Leaderboard' }, function(err, data) {
        if (err) {
            console.log(err);
            res.send({ success: false });
        } else {
            var topScores = data.Items.slice();
            topScores.sort(sortScores);
            res.send({ success: true, topScores: topScores })
        }
    });
});

module.exports = router;
