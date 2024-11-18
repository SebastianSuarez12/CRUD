from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank_accounts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de datos
class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_holder = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, nullable=False)

# Crear base de datos
with app.app_context():
    db.create_all()

# Rutas
@app.route('/')
def index():
    accounts = BankAccount.query.all()
    return render_template('index.html', accounts=accounts)

@app.route('/account/<int:id>')
def details(id):
    account = BankAccount.query.get_or_404(id)
    return render_template('details.html', account=account)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        account_number = request.form['account_number']
        account_holder = request.form['account_holder']
        balance = float(request.form['balance'])

        new_account = BankAccount(account_number=account_number, account_holder=account_holder, balance=balance)
        db.session.add(new_account)
        db.session.commit()
        flash('Cuenta creada con éxito!')
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    account = BankAccount.query.get_or_404(id)

    if request.method == 'POST':
        account.account_number = request.form['account_number']
        account.account_holder = request.form['account_holder']
        account.balance = float(request.form['balance'])

        db.session.commit()
        flash('Cuenta actualizada con éxito!')
        return redirect(url_for('index'))

    return render_template('update.html', account=account)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    account = BankAccount.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    flash('Cuenta eliminada con éxito!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
