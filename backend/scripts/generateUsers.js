const falso = require('@ngneat/falso');

const data = [];
for (let i = 0; i < 1000; i++) {
    data.push({
    _id: falso.randNumber({ min: 1000, max: 9999999 }),
    username: falso.randUserName(),
    email: falso.randEmail(),
    has_access: falso.randBoolean(),
    is_authenticated: falso.randBoolean(),
    account_classification: {
        label: falso.rand([
        "bot",
        "human",
        "suspicious"
        ]),
        confidence_score: Number(falso.randFloat({ min: 0.5, max: 1.0 }).toFixed(2))
    },
    created_at: falso.randPastDate({ years: 5 }).toISOString(),
    follower_count: falso.randNumber({ min: 0, max: 1000000 }),
    following_count: falso.randNumber({ min: 0, max: 5000 }),
    tweet_count: falso.randNumber({ min: 0, max: 50000 }),
    engagement_score: Number(falso.randFloat({ min: 0.0, max: 1.0 }).toFixed(2))
    });
}

use('tori-db'); // Select the database
db.users.insertMany(data); // Insert mock users

print("Inserted 10 mock users into MongoDB!");
