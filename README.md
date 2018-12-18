Leo Kivikunnas 525925

Jaakko Koskela

Henri-Matias Tuomaala 

# wsd18 project
An online game store for JavaScript games. The service has two types of users: players and developers. Developers can add their games to the service and set a price for it. Players can buy games on the platform and then play purchased games online.

We plan on implementing all the mandatory features. Additionally we plan on implementing 3rd Party login, RESTful API and our own game.

Authentication will be implemented using Django auth. The site will have email validation after registration. 

For additional features, the 3rd party login will use Google. The RESTful API will provide a list of the available games in our site in a JSON format. Our own game will be a platformer in the style of Super Mario. 

## Models
1. user already found in django (username PRIMARY KEY, email, etc.)
2. player inherit user (profile_pic, games)
3. dev inherit user (profile_pic, games, seller_id)

4. game (name PRIMARY KEY, price, link to game, highscores)
5. highscores (game, username, score)

The games that the user owns are listed in a dictionary in a field in the player model. The key in this dictionary will be the game/name of the game and the value will be the json string representing the current game state for this game and gamer. 

usernames and emails are unique, username is the primary key
user id -- unique 



## Implementation order and timetable:
* 12.1. basic implementation working.
* 19.2. final commit. 


