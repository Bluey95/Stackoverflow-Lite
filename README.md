[![Build Status](https://travis-ci.org/Bluey95/Stackoverflow-Lite.svg?branch=develop)](https://travis-ci.org/Bluey95/Stackoverflow-Lite)  [![Coverage Status](https://coveralls.io/repos/github/Bluey95/Stackoverflow-Lite/badge.svg?branch=challenge_three_latest)](https://coveralls.io/github/Bluey95/Stackoverflow-Lite?branch=challenge_three_latest)

### StackOverflow-lite is a platform where people can ask questions and provide answers. 

1. To view on the browser, visit [here](https://bluey95.github.io/Stackoverflow-Lite/)
* [View Questions](https://bluey95.github.io/Stackoverflow-Lite/)
* [Ask a Question](https://bluey95.github.io/Stackoverflow-Lite/userask.html)
* [View specific Question/Answers](https://bluey95.github.io/Stackoverflow-Lite/viewquestions.html)
* [Profile Page](https://bluey95.github.io/Stackoverflow-Lite/profile.html)
* [Create an account](https://bluey95.github.io/Stackoverflow-Lite/signup.html)
* [Login](https://bluey95.github.io/Stackoverflow-Lite/signin.html)




2. To interact with the api endpoints, visit the link [here]https://stackoverflowlitev3.herokuapp.com/)<br>

## Use the following endpoints to perform the specified tasks
		 
| 	Endpoint                               | Functionality                                                  
| ---------------------------------------------| -----------------------------------------------|
| POST api/v2/auth/registration                | Create a user account                          |          
| POST /api/v2/auth/login                      | Login a user                                   |
| GET api/v2/auth/users                        | Retrieve the registered users                  |
| GET /api/v2/auth/users/<int:id>              | Retrieve a specific registered user            |
| POST /api/v2/questions                       | Create a question                              |
| GET /api/v2/questions                        | Retrieve posted questions                      |
| GET /api/v2/questions<int:id>                | Retrieve a specific posted question and answer |
| POST /api/v2/questions/<int:id>/answer       | Create an answer to a specific question        |
| GET /api/v2/questions/myquestions            | Retrieve specific questions posted by a user   |
| GET /api/v2/questions/mostanswers            | Check for questions with most answers   |
| PUT /api/v2/questions/<int:id>               | Update a specific posted question              |
| DELETE /api/v2/questions/<int:id>            | Delete a specific posted question              |
| PUT /api/v2/questions/<int:id>/answer/<ansid> | Accept a specific answer to a posted question  |
| PUT /api/v2/questions/<int:id>/answer/<ansid> | Edit a specific answer to a posted question    |
| DELETE /api/v2/questions/<int:id>/answer/<ansid> | DELETE a specific answer to a posted question  |
| PUT /api/v2//questions/<int:id>/answer/ansid>/upvote | Upvote an answer to a specific question |
| PUT /api/v2//questions/<int:id>/answer/ansid>/downvote | Downvote an answer to a specific question |
		 

## Application Features

1. Create and Read questions
2. Create and Read answers

<br>

**Users can do the following**

* Users can create an account and log in.
* Users can post questions.
* Users can delete the questions they post.
* Users can post answers.
* Users can view the answers to questions. 
* Users can vote for an answer.
* Users can mark an answer as accepted.
* Users can delete the answers they post.

## How to Test Manually
1. Clone the project to your local machine <br>
		`https://github.com/Bluey95/Stackoverflow-Lite.git`
2. Create Virtual Environment <br>
		`virtualenv venv`
3. Activate Virtual ENvironment<br>
		`source venv/bin/activate`
4. Install Dependencies<br>
		`(venv)$ pip install -r requirements.txt` <br>
		`(venv)$ pip freeze > requirements.txt` <br>
5. Run the app <br>
		`flask run`<br>
6. Run tests <br>
		`pytest`
		<br>
## How to Contribute to this project?

1. Fork the project to your github account.

2. Clone it to your local machine.

3. Create a feature branch from develop branch :

4. git checkout -b `ft-name-of-the-feature`

5. Update and Push the changes to github.

6. git push origin `ft-name-of-the-feature`

7. Create Pull Request to my develop branch as base branch.




