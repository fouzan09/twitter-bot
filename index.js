const Twit = require('twit');
const fs = require('fs');
const cron = require('node-cron');

const twitterClient = new Twit({
  consumer_key: 'dmE1cTRxN3RlM3F6QURVcWhKX3c6MTpjaQ',
  consumer_secret: 'Io35Y9iFtCft7KQ-JbFL4OZ_tiXCMUNESvdHKuwuCTMkz6xT5u',
  access_token: '3287380992-JZQtvHobNY9eJC8iVPBe9Zwv9HnriMs4WubGNCH',
  access_token_secret: 'PLCJKENp74lqDrBzpdopt1P3GVZ4rKDqjHSA18IuFxRUA',
});

// Schedule the tweet to be sent daily at a specific time  
cron.schedule('0 21 * * *', () => {
  // Read the content from tweets.txt  
  fs.readFile('tweets.txt', 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading tweets.txt:', err);
      return;
    } 

    // Remove leading/trailing whitespaces and line breaks from the tweet content
    const tweetContent = data.trim();

    // Send the tweet
    twitterClient.post('statuses/update', { status: tweetContent }, (err, data, response) => {
      if (err) {
        console.error('Error tweeting:', err);
      } else {
        console.log('Tweeted:', tweetContent);
      }
    });
  }); 
});

console.log('Tweet scheduler started.');
