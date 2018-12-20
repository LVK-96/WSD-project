Leo Kivikunnas 525925

Jaakko Koskela 526050

Henri-Matias Tuomaala 609265

# wsd18 project
## General description
An online game store for JavaScript games. The service has two types of users: players and developers. Developers can add their games to the service and set a price for it. Players can buy games on the platform and then play purchased games online.

We plan on implementing all the mandatory features. Additionally we plan on implementing 3rd Party login, RESTful API and our own game.

Authentication will be implemented using Django auth. The site will have email validation after registration.

We are going to implement basic player functionalities: Players are able to search for games and buy them using Simple Payments. Players are able to play games that they have purchased. Our app adds the name of the game to players games-list when player buys the game from the website. Basic search functionality will be implemented in order for players to find games to buy.

Developers are able to add and manage their own games on the site and set a price for them. Basic security, inventory and statics will be implemented inside the dev.<span></span>py model.

Game/service interactions will be implimented using postMessage as requested. We will keep track of highscores and each players game states with appropriate models. 

For additional features, the 3rd party login will use Google. The RESTful API will provide a list of the available games in our site in a JSON format. Our own game will be a platformer in the style of Super Mario.

## Models
1. User already found in django (username PRIMARY KEY, email, etc.)
2. Player inherit user (profile_pic, owned_games)
3. Dev inherit user (profile_pic, seller_id)

4. Game (name PRIMARY KEY, dev_name, price, link to game, purchases)
5. Highscores (game, username, score)

The games that the user owns are listed in a dictionary in a field in the player model. The key in this dictionary will be the game/name of the game and the value will be the json string representing the current game state for this game and gamer.

The amount of how many games a certain developer has created can be queried

highscores

usernames and emails are unique, username is the primary key
user id -- unique

<img src="model_graph.PNG" alt="Smiley face" height="420" width="420">

## Views

## Templates

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