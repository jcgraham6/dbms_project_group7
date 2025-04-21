from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
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
               
    except oracledb.DatabaseError as e:
        raise
        

def update_data(sql, data):
    '''
    Documentation: https://python-oracledb.readthedocs.io/en/latest/user_guide/batch_statement.html

    '''
    try:

        con = connect_to_db()
        cursor = con.cursor()

        cursor.executemany(sql, data)

        con.commit()
        cursor.close()
               
    except oracledb.DatabaseError as e:
        raise
        

# Create instance
app = Flask(__name__)

# Secret key for session
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST']) # Route is the place to go (/ represents the base url or the homepage)
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Pull username and password from DB
        real_password = fetch_data('SELECT PASSWORD FROM ACCOUNT WHERE USERNAME = :1',[username])

        # Validate credentials
        if  password == real_password['PASSWORD'][0]:
            session['user'] = username
            return redirect(url_for('home')) 
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/home')
def home():

    return render_template('DailyPick.html')

@app.route('/profile', methods = ['GET','POST'])
def profile():
    try:

        # Get the user email from session
        username = session.get('user')

        if not username:
            return "Unauthorized", 401  # Or redirect to login

        account_sql = '''
            SELECT username, phone, paypref
            FROM ACCOUNT
            WHERE username = :1
        '''

        df = fetch_data(account_sql, [(username)])
# Account has no ties to the preferences table

        if request.method == 'POST':

            diet = request.form.get('diet')
            brand = request.form.get('brand')
            budget = request.form.get('budget')

            pref_sql = '''
            SELECT * FROM PREFERENCES WHERE USERNAME = :1
            '''

            pref_df = fetch_data(pref_sql, [(username)])
        
            if pref_df.empty == True:
                insert_sql = '''
                INSERT INTO PREFERENCES (username, max_budget, dietaryrestric, prefbrands)
                VALUES (:1, :2, :3, :4)
                '''

                insert_data(insert_sql, [(username, budget, diet, brand)])

                flash("Preferences saved successfully!", "success")

            
            else:
                update_sql = '''
                UPDATE PREFERENCES SET
                max_budget = :1, 
                dietaryrestric = :2, 
                prefbrands = :3
                WHERE USERNAME = :4
                '''

                update_data(update_sql, [(budget, diet, brand, username)])

                flash("Preferences saved successfully!", "success")



        return render_template('Account.html',
                               username=df['USERNAME'].iloc[0],
                               phone=df['PHONE'].iloc[0],
                               credit_card= df['PAYPREF'].iloc[0])
    

    except oracledb.DatabaseError as e:
        print(f"Database Error: {e}")
        return "Internal Server Error", 500


@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    if request.method == 'POST':
        try:
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            phone = request.form['phone']
            saveditem = request.form['saveditem']
            paypref = request.form['paypref']

            insert_sql = '''
            INSERT INTO ACCOUNT (createDate, phone, password, email, username, saveditem, paypref)
            VALUES (CURRENT_DATE, :1, :2, :3, :4, :5, :6)
            '''

            insert_data(insert_sql, [(phone, password, email, username, saveditem, paypref)]) 
            return redirect(url_for('login'))  # Redirect to login

        except KeyError as e:
            print(f"KeyError: Missing fields for {str(e)}")
            return "Missing data", 400

    # Render the CreateAccount form
    return render_template('CreateAccount.html')


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



@app.route('/go_to_signin')
def go_to_signin():
    # This route will redirect the user to the signin page
    return redirect(url_for('signin'))

@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        message=request.form['message']
        conn=connect_to_db()
        cur=conn.cursor()
        cur.execute("INSERT INTO contactus (name, email, message) VALUES(%s, %s, %s)", (name , email, message))
        conn.commit()
        cur.close()
        return render_template('thankyou.html')
    return render_template('contactus.html')

@app.route('/product/<int:commodityID>')
def product_detail(commodityID):
    custID=session.get('custID') #Fetch from session
    conn=connect_to_db()
    cursor=conn.cursor()
    cursor.execute("SELECT name, price FROM commodity_store WHERE commodityID=:id",[commodityID])
    product=cursor.fetchone()

    #Fetch Reviews
    cursor.execute("""SELECT m.memberName, r.rating, r.comment, TO_CHAR(r.reviewDate, 'YYYY-MM-DD') FROM REVIEW r JOIN customer c ON r.custID=c.custID JOIN member m ON c.custID = m.custID WHERE r.commodityID=:id ORDER BY r.reviewDate DESC""", [commodityID])
    reviews=cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('product_detail.html', product=product, reviews=reviews)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    if 'custID' not in session:
        return redirect('/SignIn')
    commodityID=request.form['commodityID']
    custID=request.form['custID']
    rating=request.form['rating']
    comment=request.form['comment']
    conn=connect_to_db()
    cursor=conn.cursor()
    cursor.execute("""INSERT INTO Review(reviewID, commodityID, custID, rating, comment, reviewDate) VALUES (review_seq.NEXTVAL, :commodityID, :custID, :rating, :comment, SYSDATE)""", [commodityID , custID, rating, comment])
    conn.commit()
    cursor.close()
    conn.close()
    return render_template(f'/product/{commodityID}')
if __name__ == '__main__':
    app.run(debug=True)
