const falso = require('@ngneat/falso');
const { ObjectId } = require("mongodb");

const data = [];
for (let i = 0; i < 100; i++) {
  data.push({
    _id: new ObjectId(),
    xid: falso.randNumber({ min: 100000, max: 999999 }),
    username: falso.randUserName().replace(/[^a-zA-Z0-9.-]/g, ''),
    email: falso.randEmail(),

    twitter_access_token: falso.randHex({ length: 48 }).join(""),
    twitter_access_token_secret: falso.randHex({ length: 48 }).join(""),
    has_access: falso.randBoolean(),
    is_authenticated: falso.randBoolean(),
    account_classification: {
      label: falso.rand(["bot", "human", "suspicious"]),
      confidence_score: Number(falso.randFloat({ min: 0.5, max: 0.9 }).toFixed(2)),
    },
    created_at: falso.randPastDate({ years: 5 }).toISOString(),
    follower_count: falso.randNumber({ min: 0, max: 1000000 }),
    following_count: falso.randNumber({ min: 0, max: 5000 }),
    tweet_count: falso.randNumber({ min: 0, max: 50000 }),
    engagement_score: Number(falso.randFloat({ min: 0.0, max: 0.9 }).toFixed(2)), // Ensure range [0.0 - 1.0]
  });
}

use("tori-db")
db.users.insertMany(data);
print("Inserted 100 mock users into MongoDB!");
