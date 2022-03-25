from flask import *
from model import *
import re

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'handsome_guy_jin'

@app.route('/', methods=["GET", "POST"])
def index() :
	if 'username' not in session :
		return redirect(url_for('login'))
		
	orders = get_orders_from_db()
	board_cnt = len(orders)
	json_data = json.dumps(orders) # str
	json_data = json.loads(json_data) # list

	return render_template('index.html', board_cnt=board_cnt, json_data=json_data)

@app.route('/login',methods=["GET", "POST"])
def login() :
	if request.method == 'GET' :
		return render_template('login.html')

	elif request.method == 'POST' :
		username = request.form['username']
		password = request.form['password']
		result = user_login(username, password)

		if result :
			session['username'] = username
			return redirect(url_for('index'))
		else :
			flash('Incorrect username or password!')
			return redirect(url_for('login'))
	return 'login'

@app.route('/register',methods=["GET", "POST"])
def register() :
	if request.method == 'GET' :
		return render_template('register.html')

	elif request.method == 'POST' :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		phone = request.form['phone']
		rate = 1.0

		if re.findall("([^\w])", username) :
			return '<script>alert("아이디는 영문, 숫자, _만 사용이 가능합니다."); history.back(-1);</script>'

		result = user_register(username, password, email , phone , rate)

		if result :
			session['username'] = username
			return redirect(url_for('login'))

		else :
			flash('Incorrect username or password!')
			return redirect(url_for('register'))

	return 'register'

@app.route('/write', methods=["GET", "POST"])
def write() :
	if 'username' not in session :
		return render_template('login.html')

	if request.method == 'GET':
		return render_template("write.html")

	if request.method == 'POST':
		locate = request.form['locate']
		title = request.form['title']
		contents = request.form['contents']
		user_status = request.form['user_status']
		username = session['username']

		result = user_write(locate, title, contents, user_status, username)

		if result :
			return redirect(url_for('index'))
		return 'False'

@app.route('/detail_order/<no>')
def detail_order(no):
	return str(get_one_boorder_from_db(no))

@app.route('/api/get_orders/')
def get_orders() :
	orders = get_orders_from_db()
	retval = str(json.dumps(orders))
	return retval



if __name__ == '__main__' :
	app.run(host='0.0.0.0', port='5000', debug=True)
