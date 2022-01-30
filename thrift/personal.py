import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify
)

from thrift.db import get_db
from thrift.auth import login_required

bp = Blueprint('personal', __name__, url_prefix='/personal')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def my_account():
	return render_template('features/my_account.html')



@bp.route('/health', methods=('GET', 'POST'))
@login_required
def health():
	print("add health")
	return render_template("features/personal/add_health.html")

@bp.route('/expenditure', methods=('GET', 'POST'))
@login_required
def expenditure():
	if request.method == 'POST':
		message = None
		error = None

		dated = request.form['date']
		primary_type = request.form['primary_type']
		totalAmount = request.form['totalAmount']
		secondary_type = request.form['secondary_type']
		user = g.user['username']
		details = request.form['details']
		details = details[:-1] #removing that last comma
		
		if details == "":
			error = "No items entered."
		if error is None:
			db = get_db()
			db.execute(
				"""
					INSERT INTO personal
					(dated, user, primary_type, secondary_type, amount, details)
					VALUES (?,?,?,?,?,?)
				""",
				(dated, user, primary_type, secondary_type, totalAmount, details))

			db.commit()
			message = "Data inserted!"

			flash(message)
			return redirect(url_for('personal.my_account'))
		if error is not None:
			flash(error)
	return render_template('features/personal/add_expenditure.html')


@bp.route('/income', methods=('GET', 'POST'))
@login_required
def income():
	if request.method == 'POST':
		message = None
		error = None

		dated = request.form['date']
		primary_type = request.form['primary_type']
		amount = request.form['amount']
		secondary_type = request.form['secondary_type']
		user = g.user['username']
		details = request.form['remarks']

		if details == "":
			error = "No items entered."
		if error is None:
			db = get_db()
			db.execute(
				"""
					INSERT INTO personal
					(dated, user, primary_type, secondary_type, amount, details)
					VALUES (?,?,?,?,?,?)
				""",
				(dated, user, primary_type, secondary_type, amount, details))

			db.commit()
			message = "Data inserted!"

			flash(message)
			return redirect(url_for('personal.my_account'))
		if error is not None:
			flash(error)
	return render_template('features/personal/add_income.html')

def fetchBalance(user):
	query = """SELECT COALESCE(SUM(amount),0)
			FROM personal
			WHERE primary_type='Expenditure' 
			AND user='"""+user+"""'
			"""
	db =get_db()
	totalExp = db.execute(query).fetchone()
	db.commit()
	query = """SELECT COALESCE(SUM(amount),0)
			FROM personal
			WHERE primary_type='Income' 
			AND user='"""+user+"""'
			"""
	totalInc = db.execute(query).fetchone()
	db.commit()

	avlblBal = totalInc[0] - totalExp[0]
	bal = str(avlblBal)

	return bal

@bp.route('/view_data', methods=('GET', 'POST'))
@login_required
def view_data():
	if request.method == 'GET':
		service = request.args.get('service')
		db = get_db()
		message = None
		error = None
		data = ''
		data2 = ''
		bal = ''
		query = ''
		query2 = ''
		tableFor = ''
		user = str(g.user['username'])

		if service == 'balance-enquiry':
			tableFor = "Available Balance"
			bal = fetchBalance(user)

		elif service == 'transactions':
			tableFor = "Transactions"
			query = """
					SELECT id, dated, primary_type, secondary_type, amount, details
					FROM personal
					WHERE user ='"""+user+"""' 
					ORDER BY (id) DESC LIMIT 30
					"""
			data = db.execute(query).fetchall()
			db.commit()
			bal = fetchBalance(user)

		elif service == 'insights':
			tableFor = "Insights"
			query = """
					SELECT secondary_type, SUM(amount)
					FROM personal
					WHERE primary_type = 'Expenditure' 
					AND user = '"""+user+"""'
					GROUP BY(secondary_type)
					ORDER BY(SUM(amount)) DESC
					"""
			data = db.execute(query).fetchall()
			db.commit()

			query2 = """
					SELECT secondary_type, SUM(amount)
					FROM personal
					WHERE primary_type = 'Income' 
					AND user = '"""+user+"""'
					GROUP BY(secondary_type)
					ORDER BY(SUM(amount)) DESC
					"""
			data2 = db.execute(query2).fetchall()
			db.commit()

		return render_template('features/personal/view_data.html',
			 bal = bal, data = data, data2 = data2, tableFor = tableFor)

	return render_template('features/personal/view_data.html')

