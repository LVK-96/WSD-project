Leo Kivikunnas 525925

Jaakko Koskela 526050

Henri-Matias Tuomaala 609265

# wsd18 project
## Basic Implemented Features

# Authentication
In our project we implemented basic authentication. Registeration, both as a gamer and a developer, login and logout functionality using djangos existing custom user model extending it to our specific needs using an one to one field to a profile model. In the authentication we used django's authentication backend. In addition to this we implemented email validation for the registered users. All aspects regarding authentication, outlined in the requirements, were implemented and work as they are expected to.
Estimated points: 200p

# Basic Player Functionality
All functionality for buying games, adding games to the store as well as playing these games were implemented. Payment is handled using the mockup payment service. All game to service interaction was implemented on the service side (settings, saving, loading, submitting score and error handling). Security restrictions/access controll was implemented so that a player could view, play and submit highscores only for the games that they had purchased.
The games that are added by the developers are listed in the store and can be filtered using tags that the developer can choose for the game. In addition to this basic search functionality was implemented so that you can search for a game using its name. The search functionality is basic and doesn't support partial matches from the search string to the game name, in other words you can find a game using this search functionality only if you input the exact correct name. Searching for games using words that are mentioned in the game bio is not supported.
All basic functionality was implemented, but the game searching and filtering functionality is basic.
Estimated points: 260p

# Basic Developer Functionalities
Functionality for adding, modifying and removing games were implemented. Basic game inventory and sales statistics were likewise implemented as well as a transaction history. Basic access control and security restrictions were implemented so that a developer could only access and modify their own games. Only users that are not developers can play the games.
Estimated points: 200

# Game/Service Interaction
All interaction between the game and the service were implemented using postmessages(settings, saving, loading, submitting a score, as well as basic error handling) 
Appropriate csrf protection was used as well as origin checks for the Game to service interaction. When the score is submitted the highscore is saved to the highscore table. The highscores are implemented so that an when a user purchases a game an entry specifying that user and that specific game with a score of zero is added to the table. To check whether or not a user has purchased a game the highscore table is checked for an entry for that game and where the owner is that user. Also the highscore table was implemented so that a single user can only have one highscore (the one with the largest score) per one game.
Estimated Points: 200

# Quality of work
The project was split mainly into two applications the user application and the store application. Comments were used where appropriate to make the code more easily understood. Django's framework was utilized well and seperation of concerns between models, views and templates as well as any additional script files was was made clear. Attention was given to the front end by using clear styling and user friendly interaction scheme to make the application easily navigateable for a first time user. Our project could have been separated into more applications, but this was not deemed necessary since the store application seemed very unified.
Estimated Points: 80

# Non-functional Requirements
Our project plan was well thought out and thorough, and the few problems which came apparent when starting to work on the project and through comments that we received on our project plan were quickly taken into account and fixed. Our teams roles were not so well defined, but we divided up clear areas of responsibilities (on what we would work on) every time we met for a programming session. This allowed us to work on separate parts of the project continuously without conflicting with each others work. Our team met more or less regularly to divide up the responsibilities and to discuss and plan our project further as well as to code in a group so that we could discuss ideas and ask for help when needed.
Estimated Points: 180

## Extra Features

# Save/Load and Resolution feature
All functionality for saving and loading the game was implemented on the service side as well as setting the resolution of the iframe window when the game is launched, using the simple message protocol
Estimated Points: 100

# 3rd Party Login
A third party login was implemented using googles gmail to login to the service
Estimated Points: 100

# RESTful API
A RESTul API was implemented. The restful API gives information in the json format. A GET request can be made to the API to retrieve highscores and parameters can be given to the get request to specify which users or games (or both) highscores you want to retireve.
Estimated Points: 100

# Own Game
We implemented a javascript snake game that supports saving the highscore to the service. Due to time constraints, the game-side implementation of the save and load functionality does not work properly due to difficulties in loading up the game state and starting the game up again after receiving it from the service. The game is still fully playable and highscores can be saved to the service. Due to the snake game being implemented for keyboard usage it is not mobile friendly.
Estimated Points: 50

# Mobile Friendly
Our service was made mobile friendly by using bootstrap.
Estimated Points: 40

# Security note
The game is added to the players inventory by adding a row to the highscore table. this might have not been the best idea in hindsight since updating highscores are done in multiple places and this might open up more opportunities for an attacker to expoit mechanics. For example if the attacker is able to spoof the POST message origin header in a way that the message appears to come from the correct origin. However everywhere where a highscore is updated it is checked that the user already has an entry in the highscore table which would mean that the user would already own the game. 



 Where do you feel that you %%%%%%%were successful and where you had most problems.%%%%%%%%%%%% Give sufficient details, this will influence the non-functional points awarded.
%%%%%%How did you divide the work between the team members - who did what?%%%%%%


## instructions for using the application
# Heroku
https://wsd18-store.herokuapp.com/

Instructions how to use your application and link to Heroku where it is deployed.
If a specific account/password (e.g. game developer) is required to try out and test some aspects of the work, please provide the details.

if you use https the example game will not work due to it being ---