from flask import Flask, render_template, request, redirect, url_for, session
import oracledb
import pandas as pd
import os

def connect_to_db():

    try:
        
       # cx_Oracle.init_oracle_client()

        dsn = oracledb.makedsn('oracle.wpi.edu', 1521, sid = 'ORCL')

        db = oracledb.connect(user = 'jgraham',
                               password = 'JGRAHAM',
                               dsn = dsn)
        return db
        
    except oracledb.DatabaseError as e:
        raise
    

def fetch_data(sql, params = None):
    '''
    Execute SQL statement to pull data and store in dataframe
    '''
    
    try:
        cursor = connect_to_db().cursor()
        cursor.execute(sql, params or [])
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] # Extract column names
        df = pd.DataFrame(data, columns=columns) # Create dataframe
        cursor.close() # Close connection

        return df

    except oracledb.DatabaseError as e:
        raise
        

def insert_data(sql, data):
    '''
    Documentation: https://python-oracledb.readthedocs.io/en/latest/user_guide/batch_statement.html
    '''

    try:
        con = connect_to_db()
        cursor = con.cursor()

        cursor.executemany(sql, data)

        con.commit()
        cursor.close()
               
    except cx_Oracle.DatabaseError as e:
        raise
        

def update(sql, data):
    '''
    Documentation: https://python-oracledb.readthedocs.io/en/latest/user_guide/batch_statement.html

    '''
    try:

        con = connect_to_db()
        cursor = con.cursor()

        cursor.executemany(sql, data)

        con.commit()
        cursor.close()
               
    except cx_Oracle.DatabaseError as e:
        raise
        

# Create instance
app = Flask(__name__)

# Secret key for session
app.secret_key = os.urandom(24)

@app.route("/") # Route is the place to go (/ represents the base url or the homepage)

def index():
    return render_template('DailyPick.html')


@app.route('/shop', methods=['GET'])
def shop():

    # Connect to db
    conn = connect_to_db()
    cursor = conn.cursor()

    data = cursor.execute("SELECT NAME, PRICE, QUANTITY FROM COMMODITY_STORE")

    search_query = request.args.get('search', '') 

    filtered_data = []

    if search_query:
        filtered_data = [row for row in data if search_query.lower().strip() in row[0].lower()]
    else:
        filtered_data = data

    return render_template('Search.html', data=filtered_data)  # Here, you're passing `filtered_data`



@app.route('/go_to_shop')
def go_to_shop():
    # This route will redirect the user to the shop page
    return redirect(url_for('shop'))


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        product_name = request.form['product_name']
        product_price = float(request.form['price'])
        product_quantity = int(request.form['quantity'])

        # Retrieve the cart from the session (if it exists)
        cart = session.get('cart', [])
        
        # Check if the product is already in the cart
        product_in_cart = False
        for item in cart:
            if item['name'] == product_name:
                item['quantity'] += product_quantity  # Update quantity
                product_in_cart = True
                break
        
        # Add if not in cart
        if not product_in_cart:
            cart.append({
                'name': product_name,
                'price': product_price,
                'quantity': product_quantity
            })

        # Save session
        session['cart'] = cart
        session.modified = True

        # Refresh page
        return redirect(url_for('cart'))

    except KeyError as e:
        print(f"KeyError: Missing form data for {str(e)}")
        return "Missing data", 400
    

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():

    # Product to remove
    product_name = request.form['product_name']
    
    # Get the cart from the session
    cart = session.get('cart', [])

    # Remove item from cart if it exists
    cart = [item for item in cart if item['name'] != product_name]

    # Save
    session['cart'] = cart
    session.modified = True

    # Refresh page
    return redirect(url_for('cart'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():

    # Clear the cart
    session['cart'] = []

    # Refresh page
    return redirect(url_for('cart'))

@app.route('/cart', methods=['GET'])
def cart():
    
    cart = session.get('cart', [])
    return render_template('Cart.html', cart=cart)


@app.route('/signin', methods=['GET'])
def signin():
    
    # Connect to db
    conn = connect_to_db()
    cursor = conn.cursor()

    print('Hello!')

    return render_template('SignIn.html')


@app.route('/go_to_signin')
def go_to_signin():
    # This route will redirect the user to the signin page
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)

