var express = require('express');
var mysql = require('mysql');
var connection = mysql.createConnection({
    host: 'database-1.c32yscgymlt6.us-east-1.rds.amazonaws.com',
    user: 'evantao',
    password: 'rubyonrails',
    database: 'db1',
    port: '3306'
});
var async = require('async');
var router = express.Router();

router.get('/', function(req, res, next) {
    connection.query("SELECT nonTable.nonEvents as id, e.name as name FROM (SELECT p.athlete_id as nonAthletes, p.event_id as nonEvents FROM Athlete_Participates p, Athlete a WHERE a.id = p.athlete_id and a.bio <> 'N/A' and (a.country_id = 'USA' OR a.country_id = 'URS' OR a.country_id = 'GBR' OR a.country_id = 'FRA' OR a.country_id = 'GER' OR a.country_id = 'ITA' OR a.country_id = 'SWE' OR a.country_id = 'AUS' OR a.country_id = 'HUN' OR a.country_id = 'NED' OR a.country_id = 'JPN' OR a.country_id = 'CAN' OR a.country_id = 'CHN' OR a.country_id = 'RUS' OR a.country_id = 'NOR' OR a.country_id = 'DEN' OR a.country_id = 'ROU' OR a.country_id = 'POL' OR a.country_id = 'KOR' OR a.country_id = 'ESP')) as nonTable, Event e WHERE nonTable.nonEvents = e.id and e.id > 0 GROUP BY nonEvents HAVING count(nonAthletes) > 0", function(err, rows, fields) {
    if (err) {
        console.log(err);
        res.send({ "success": false });
    } else {
        res.send({ "events": rows, "success": true });
    }
}); 
});

module.exports = router;
