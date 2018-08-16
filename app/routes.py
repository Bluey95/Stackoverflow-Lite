from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from app import app

@app.route('/')

@app.route('/index')
def index():
    user = {'username': 'Susan Were'}
    return render_template('index.html', title='StackOverflow-Lite', user=user)


@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('questions'))
    return render_template('userlogin.html', title = 'Sign in', error=error)

@app.route('/usersignup')
def usersignup():
    return render_template('usersignup.html', title='Create an account')


@app.route('/questions')
def questions():
    posts = [
        {
            'date': '05/10/2017',
            'author': 'Susan Were',
            'body': 'How to launch any .html file on browser in UWP JS.',
            'answer': '3 answers'

        },
        {
            'date': '06/06/2014',
            'author': 'Michael Jordan',
            'body': 'Python regex, repetition on subgroup',
            'answer': '4 answers'
        },
        {
            'date': '07/05/2016',
            'author': 'Kristy Magner',
            'body': 'Cannot access user model from Devise sessions controller.',
            'answer': '7 answers'
        },
        {
            'date': '08/09/2018',
            'author': 'Bringoff',
            'body': 'Is it possible to show Google App installer dialog from inside native android app?',
            'answer': '5 answers'
        },
        {
            'date': '06/11/2015',
            'author': 'Dorothy Kerubo',
            'body': 'Command HTML/CSS expansion',
            'answer': '2 answers'
        },
        {
            'date': '08/12/2017',
            'author': 'Wayne Buidler',
            'body': 'Android Studio is not installing.',
            'answer': '4 answers'
        },
        {
            'date': '02/03/2018',
            'author': 'Sydney Hill',
            'body': 'Is there a way to generate a controller without a model?',
            'answer': '2 answers'
        },
        {
            'date': '03/04/2017',
            'author': 'Mary Blige',
            'body': 'How do I gradle build offline?',
            'answer': '3 answers'
        },
        {
            'date': '07/05/2016',
            'author': 'Kristy Magner',
            'body': 'Cannot access user model from Devise sessions controller.',
            'answer': '7 answers'
        },
        {
            'date': '08/09/2018',
            'author': 'Bringoff',
            'body': 'Is it possible to show Google App installer dialog from inside native android app?',
            'answer': '7 answers'
        }


    ]
    return render_template('questions.html', title='Questions', posts=posts)

@app.route('/ask')
def ask():
    return render_template('ask.html', title='Ask')

@app.route('/userprofile')
def userprofile():
    userdetails = [
        {
            'name': 'Millicent Were',
            'description': 'Accountant | R | Python',
            'questionscount': '2',
            'answerscount': '3',
            'favouritescount': '4'

        }
    ]

    userquestions = [
        {
            'date': '06/06/2014',
            'author': 'Millicent Were',
            'body': 'Python regex, repetition on subgroup',
            'answer': '2 answers'
        },
        {
            'date': '05/10/2017',
            'author': 'Millicent Were',
            'body': 'How to launch any .html file on browser in UWP JS',
            'answer': '3 answers'
        }
    ]

    useranswers = [
        {
            'date': '07/05/2016',
            'author': 'Kristy Magner',
            'body': 'Cannot access user model from Devise sessions controller.',
            'answer': '7 answers'
        },
        {
            'date': '08/09/2018',
            'author': 'Bringoff',
            'body': 'Is it possible to show Google App installer dialog from inside native android app?',
            'answer': '7 answers'
        }
    ]

    userfavourites = [
        {
            'date': '08/12/2017',
            'author': 'Wayne Buidler',
            'body': 'Android Studio is not installing.',
            'answer': '4 answers'
        },
        {
            'date': '02/03/2018',
            'author': 'Sydney Hill',
            'body': 'Is there a way to generate a controller without a model?',
            'answer': '2 answers'
        }
    ]
    return render_template('userprofile.html', title='Profile', userdetails = userdetails, userquestions = userquestions, userfavourites = userfavourites, useranswers = useranswers)

@app.route('/sortedquestions')
def sortedquestions():
    userdetails = [
        {
            'name': 'Millicent Were',
            'description': 'Accountant | R | Python',
            'questionscount': '2',
            'answerscount': '3',
            'favouritescount': '4'

        }
    ]

    userquestions = [

        {
            'date': '05/10/2017',
            'author': 'Millicent Were',
            'body': 'How to launch any .html file on browser in UWP JS',
            'answer': '3 answers'
        },
        {
            'date': '06/06/2014',
            'author': 'Millicent Were',
            'body': 'Python regex, repetition on subgroup',
            'answer': '2 answers'
        }
        
    ]

    useranswers = [
        {
            'date': '07/05/2016',
            'author': 'Kristy Magner',
            'body': 'Cannot access user model from Devise sessions controller.',
            'answer': '7 answers'
        },
        {
            'date': '08/09/2018',
            'author': 'Bringoff',
            'body': 'Is it possible to show Google App installer dialog from inside native android app?',
            'answer': '7 answers'
        }
    ]

    userfavourites = [
        {
            'date': '08/12/2017',
            'author': 'Wayne Buidler',
            'body': 'Android Studio is not installing.',
            'answer': '4 answers'
        },
        {
            'date': '02/03/2018',
            'author': 'Sydney Hill',
            'body': 'Is there a way to generate a controller without a model?',
            'answer': '2 answers'
        }
    ]
    return render_template('sortedquestions.html', title='Profile', userdetails = userdetails, userquestions = userquestions, userfavourites = userfavourites, useranswers = useranswers)

@app.route('/questionsview')
def questionsview():
    question = { 'main': 'How to launch any .html file on browser in UWP JS',
                 'askedBy': 'Susan Were',
                 'detailed': 'Hi everyone, I actually want to launch any .html file in any browser. I want to Key.html open in the browser. Does anyone know how to go about this?',
                 'answerscount': '3' }
    

    answers = [

        {
            'date': '05/10/2017',
            'answeredBy': 'McKlain Geoffrey',
            'mainAnswer': 'Its not hard to launch a .html file on browser in UWP JS. You are not implementing the core unctionality yet, you are only building the User Interface elements, pages and views!You are to create a pull request to elicit review and feedback for the UI template when you are done working on them.'
        },

        {
            'date': '06/02/2018',
            'answeredBy': 'Michael K',
            'mainAnswer': 'You simply need to follow this guide provided by micrososft. You are not implementing the core unctionality yet, you are only building the User Interface elements, pages and views!You are to create a pull request to elicit review and feedback for the UI template when you are done working on them'

        },

        {
            'date': '06/12/2017',
            'answeredBy': 'Augustine Wandaje',
            'mainAnswer': 'Universal Windows Platform apps are quite essential in hosting. You are not implementing the core unctionality yet, you are only building the User Interface elements, pages and views!You are to create a pull request to elicit review and feedback for the UI template when you are done working on them'

        }
    ]
    return render_template('questionsview.html', title='Question', question = question, answers = answers)

    @app.route('/app/api/v1/questions', methods=['GET'])
    def get_questions():
        posts = [
        {
            'date': '05/10/2017',
            'author': 'Susan Were',
            'body': 'How to launch any .html file on browser in UWP JS.',
            'answer': '3 answers'

        },
        {
            'date': '06/06/2014',
            'author': 'Michael Jordan',
            'body': 'Python regex, repetition on subgroup',
            'answer': '4 answers'
        },
        {
            'date': '07/05/2016',
            'author': 'Kristy Magner',
            'body': 'Cannot access user model from Devise sessions controller.',
            'answer': '7 answers'
        },
        {
            'date': '08/09/2018',
            'author': 'Bringoff',
            'body': 'Is it possible to show Google App installer dialog from inside native android app?',
            'answer': '5 answers'
        },
        {
            'date': '06/11/2015',
            'author': 'Dorothy Kerubo',
            'body': 'Command HTML/CSS expansion',
            'answer': '2 answers'
        },
        {
            'date': '08/12/2017',
            'author': 'Wayne Buidler',
            'body': 'Android Studio is not installing.',
            'answer': '4 answers'
        },
        {
            'date': '02/03/2018',
            'author': 'Sydney Hill',
            'body': 'Is there a way to generate a controller without a model?',
            'answer': '2 answers'
        },
        {
            'date': '03/04/2017',
            'author': 'Mary Blige',
            'body': 'How do I gradle build offline?',
            'answer': '3 answers'
        },
        {
            'date': '07/05/2016',
            'author': 'Kristy Magner',
            'body': 'Cannot access user model from Devise sessions controller.',
            'answer': '7 answers'
        },
        {
            'date': '08/09/2018',
            'author': 'Bringoff',
            'body': 'Is it possible to show Google App installer dialog from inside native android app?',
            'answer': '7 answers'
        }


    ]
    return jsonify({'posts': posts})