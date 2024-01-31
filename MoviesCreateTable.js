var AWS = require("aws-sdk"); 

AWS.config.update({
    accessKeyId: `{process.env.ACCESS_KEY_ID}`,
    secretAccessKey: `{process.env.SECRET_ACCESS_KEY}`,
});

var docClient = new AWS.DynamoDB.DocumentClient(); 

var params = {
    TableName: "Player_Info", 
    Item:{
	"id": 4, 
	"name": "Evan"
	}
}; 

var params2 = {
    TableName: "Player_Info", 
    Key:{
	"name": "Evan", 
	"team_name": "evantao"
	}
}; 

docClient.put(params, function(err, data) {
    if (err) {
	console.error("Unable to create table. Error JSON:", JSON.stringify(err,null,2)); 
    } else {
	console.log("UpdateItem succeeded:", JSON.stringify(data,null,2)); 
    }
}); 
 

docClient.get(params2, function(err, data) {
    if (err) {
	console.error("Unable to create table. Error JSON:", JSON.stringify(err,null,2)); 
    } else {
	console.log("GetItem succeeded:", JSON.stringify(data,null,2)); 
    }
}); 
 