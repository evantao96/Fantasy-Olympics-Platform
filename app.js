var express = require('express'); 
var path = require('path'); 
var favicon = require('serve-favicon'); 
var logger = require('morgan'); 
var cookieParser = require('cookie-parser'); 
var bodyParser = require('body-parser'); 

var index = require('./routes/index'); 
var users = require('./routes/users'); 
var players = require('./routes/players'); 
var events = require('./routes/events'); 
var athletes = require('./routes/athletes'); 

var app = express(); 

app.use(express.static(path.join(__dirname, 'public'))); 
app.set('views', path.join(__dirname, 'views')); 

app.engine('html', require('ejs').renderFile); 
app.set('view engine', 'html'); 

app.use(logger('dev')); 
app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({ extended: false })); 
app.use(cookieParser()); 
app.use(express.static(path.join(__dirname, 'public'))); 

app.use('/', index); 
app.use('/users', users); 
app.use('/players', players); 
app.use('/events', events); 
app.use('/athletes', athletes); 

app.use(function(req, res, next) {
    var error = new Error('Not Found'); 
    err.status = 404; 
    next(err); 
}); 

app.use(function(err, req, res, next) {
    res.locals.message = err.message; 
    res.locals.error = req.app.get('env') === 'development' ? error : {}; 
    
    res.status(err.status || 500); 
    res.render('error'); 
}); 

module.exports = app; 