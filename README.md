Leo Kivikunnas 525925

Jaakko Koskela 526050

Henri-Matias Tuomaala 609265 

# wsd18 project
## General description 
An online game store for JavaScript games. The service has two types of users: players and developers. Developers can add their games to the service and set a price for it. Players can buy games on the platform and then play purchased games online.

We plan on implementing all the mandatory features. Additionally we plan on implementing 3rd Party login, RESTful API and our own game.

Authentication will be implemented using Django auth. The site will have email validation after registration. 

For additional features, the 3rd party login will use Google. The RESTful API will provide a list of the available games in our site in a JSON format. Our own game will be a platformer in the style of Super Mario. 

## Models
1. user already found in django
2. player inherit user (name, email, profile_pic, games dict with gamename: json string)
3. dev inherit user (name, email, games, profile_pic, seller_id)
4. game (name, price, link to game, highscore ordered dict) 

## Working practices
We plan on meeting weekly, propably every monday or tuesday. In the weekly meeting, we will present our work from the past week and plan our work for the following week. We are mainly going to work from home, but might arrange some development sessions. 

## Implementation order and timetable
The following timetable sets deadlines for different parts of the site: 
* Testing heroku and other unfamilliar tools and inital commits during the holidays.
* 12.1. basic implementation working. Basic templates implemented and some functionality already exists. 
* 26.1. All templates and functionality done.
* 2.2. Security tested.
* 9.2. The layout and appearance of the site finished started work on additional features.
* 16.2. All additional features implemented and tested. 
* 19.2. Final tweaks and final commit. 
