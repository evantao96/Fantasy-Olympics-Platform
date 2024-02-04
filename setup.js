var AWS = require("aws-sdk")

AWS.config.update({
    accessKeyId: "AKIAU6GDZDU3SZAKDKZB",
    secretAccessKey: "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",
    region: "us-east-1"
});

const dynamoDB = new AWS.DynamoDB({ region: "us-east-1" })

dynamoDB
  .createTable({
    AttributeDefinitions: [
      {
        AttributeName: "name",
        AttributeType: "S"
      },
      {
        AttributeName: "team_name",
        AttributeType: "S"
      }
    ],
    KeySchema: [
      {
        AttributeName: "name",
        KeyType: "HASH"
      },
      {
        AttributeName: "team_name",
        KeyType: "RANGE"
      }
    ],
    BillingMode: "PAY_PER_REQUEST",
    TableName: "Player_Info"
  })
  .promise()
  .then(data => console.log("Success!", data))
  .catch(console.error)

dynamoDB
  .createTable({
    AttributeDefinitions: [
      {
        AttributeName: "id",
        AttributeType: "N"
      }
    ],
    KeySchema: [
      {
        AttributeName: "id",
        KeyType: "HASH"
      },
    ],
    BillingMode: "PAY_PER_REQUEST",
    TableName: "Game_State"
  })
  .promise()
  .then(data => console.log("Success!", data))
  .catch(console.error)

dynamoDB
  .createTable({
    AttributeDefinitions: [
      {
        AttributeName: "rank",
        AttributeType: "N"
      }
    ],
    KeySchema: [
      {
        AttributeName: "rank",
        KeyType: "HASH"
      },
    ],
    BillingMode: "PAY_PER_REQUEST",
    TableName: "Leaderboard"
  })
  .promise()
  .then(data => console.log("Success!", data))
  .catch(console.error)