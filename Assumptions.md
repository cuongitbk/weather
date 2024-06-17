# Weather Monitoring project

When there is no more specific requirements, so I assumed some conditions to complete this project as below (Some has 
already been shown on README.md file):

* The stakeholders do not take care of techs, just focus on the results. So we can design system, db architecture,
select our most suitable techs, including:
  * Programming language: Python (From version 3.9);
  * Framework: Django;
  * Database: MySQL;
  * Cache: Redis;
  * LB/API Gateway: Nginx;
  * Logging: ELK, Sentry, Telegram;
  * Deployment: CI/CD with git/gitlab runner (Docker-compose or Docker Swarm).
* There is unclear function `Select Forcast` that could be implemented by some ways:
  * (1) Select more types of forcast: Hourly, Raw data;
  * (2) Select other locations to see forcast information.  

I decided to implement by the 2nd method because I think that it can bring the highest benefits for end-user. 
Let's try to image, `Logan, UT` will be identified as a specific grid point that it's forcast data will present for a resolution 
of about 2.5km x 2.5km. 
However, users do not live in just small area, so we may be interested in other around locations.
Therefore, I tried to get forcast data for `Logan, UT` and all locations which are on same zone with `Logan, UT`
(Distance among `Logan, UT` and these locations is from 3km to 20+km).
[README.md](3.%20Source%20code%2FREADME.md)
By this way, we also can get forcast data for all locations if we want to extend this website for any places in US.

* We do not have information about how often forcast data should be updated. From Weather Service API, we can consider to use 
[Alert APIs](https://www.weather.gov/documentation/services-web-api#/default/alerts_query). However, I used a simpler method
that will update grid point and forcast data as schedule and on demand because the cost is very equivalent while the effect is better:
  * On schedule:
    * Locations will be checked and updated their `grid point` information one a day at 0:15am;
    * Locations will be checked and updated their `forcast period` information each 30 minutes.
  * On demand: When user(s) access page that data needs to get from database instead of cache, we will check the last update
  time of this forcast period and will force update by sending an async task to back-end worker.

Within the combination of two methods, forcast data will be updated in range of 2-30 minutes (It can be changed based on configuration).
