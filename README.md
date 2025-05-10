A simple scraper that takes the first page of a popular site with job offers, compares posted offers with ones in database and sends an email with new offers daily.
In the middle of development it became apparent that using Scrapy was an absolute overkill.

I highly doubt anyone will try to get this project to run on his own machine as the repo serves as a portfolio. Anyway, in order to run this you'd need:
  - 2 gmail accounts
  - A gmail App password (https://support.google.com/accounts/answer/185833?hl=en) for the sending email
  - Setting the sending email address as "senderemail" environmental variable, receiving email as "receiveremail" environmental variable, and the app password as "emailerpassword" env variable.

After this and running src/main.py, you should be receiving an email with exciting junior python job offers every 24h!
