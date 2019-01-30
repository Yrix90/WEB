from flask import Flask, render_template, request, escape, session
from vsearch import search4letters
from DBcm import DataBaseUse
from checker import check_logged_in

app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'vsearchpasswd',
                          'database': 'vsearchlogDB', }


@app.route('/login', methods=['POST'])
def do_login() -> 'html':
    user_prof = request.form['user_prof']
    user_passwd = request.form['user_passwd']
    title = 'Вы вошли в систему как: ' + user_prof
    # results = str(search4letters(phrase, letters))
    # log_request(request, results)
    session['logged_in'] = True
    return render_template('identifications.html',
                           the_user=user_prof,
                           the_title=title, )


@app.route('/logout', methods=['POST'])
@check_logged_in
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out.'


def log_request(req: 'flask_request', res: str) -> None:
    with DataBaseUse(app.config['dbconfig']) as cursor:
        _SQL = """insert into log
                (phrase, letters, ip, browser_string, results)
                values
                (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res,))


@app.route('/search4', methods=['POST'])
@check_logged_in
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results)


@app.route('/')
def welcome() -> 'html':
    return render_template('login.html',
                           the_title='Welcome to login for search4letters on the web!')


@app.route('/menu', methods=['POST'])
@check_logged_in
def menu() -> 'html':
    return render_template('menu.html',
                           the_title='Welcome to menu for search4letters on the web!')


@app.route('/entry', methods=['POST'])
@check_logged_in
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')


@app.route('/viewlog', methods=['POST'])
@check_logged_in
def view_the_log() -> 'html':
    with DataBaseUse(app.config['dbconfig']) as cursor:
        _SQL = """select phrase, letters, ip, browser_string, results
                from log"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                           the_title='View Log',
                           the_row_titles=titles,
                           the_data=contents)


app.secret_key = 'YouWillNeverGuessMySecretKey'

if __name__ == '__main__':
    app.run(debug=True)
