# clash_river_race_stats
always over engineer your phone games


In CW1 we had some pretty strict rules around war participation: miss one = demotion, miss another = das boot.
This has gotten harder to manage w/ CW2 unless you're hyper diligent about checking the fame totals each day.
We ususally finish in the first two days so it's really more important for us to check nightly, at midnight; that allows us to decide who to demote/boot.

The old API used to make this easy, but alas another 'challenge' of CW2 -- so here we are.

In this repo is a serverless.yml that'll stand up a dynamoDB table and lambda function that will hit the CRL API and get your clan's current stats and save them to the DB.

The partition key is the clan tag, and sort key is the ISO datetime -- which should make retrieval for analytics pretty straight forward.

Please signup for an API Key at `developer.clashroyale.com` with an IP address of `128.128.128.128` -- this uses the RoyalAPI proxy service so you need to register against their IP.

I setup a cloudwatch event manually in AWS to trigger this lambda automatically at midnight EST -- that's super easy to do once you've deployed this.
https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/RunLambdaSchedule.html

If you goto Cloudwatch and click `create event` it'll walk you through everything -- you'll need to set a cron pattern that matches your timezone's midnight; I trust you can google that.

There are some notes in the code & yml file, the `CR_API_KEY` and `CLAN_TAGS` are set in the function's env vars -- technical from a 'security' standpoint the API KEY should be in KMS, but..... I don't think hacker man cares about your freely available api key.

