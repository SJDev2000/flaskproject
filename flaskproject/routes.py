from os import name
from flaskproject import app, db
from flask import request, session, url_for, make_response, flash
from flask.json import jsonify
from flask.templating import render_template
from werkzeug.utils import redirect
import hashlib
from flaskproject.models import UserDetails, Admins , Products,Cart
from datetime import datetime, timedelta
import jwt
from flaskproject.decorator import token_required

@app.route('/')
def home():
    products = Products.query.all()
    return render_template('userHome.html',products = products)

@app.route('/mobiles')
@token_required
def mobile(current_user):
    cart=Cart.query.all()
    users=UserDetails.query.all()
    for u in users:
        if current_user == u.email:
            uid=u.id
    cart2=[]
    for c in cart:
        if uid == c.user_id:
            cart2.append(c)
            
    products = Products.query.all()
    return render_template('mobiles.html',products = products,data=current_user,cart=cart2)

@app.route('/others')
@token_required
def other(current_user):
    cart=Cart.query.all()
    users=UserDetails.query.all()
    for u in users:
        if current_user == u.email:
            uid=u.id
    cart2=[]
    for c in cart:
        if uid == c.user_id:
            cart2.append(c)
            
    products = Products.query.all()
    return render_template('others.html',products = products,data=current_user,cart=cart2)

@app.route('/laptops')
@token_required
def laptop(current_user):
    cart=Cart.query.all()
    users=UserDetails.query.all()
    for u in users:
        if current_user == u.email:
            uid=u.id
    cart2=[]
    for c in cart:
        if uid == c.user_id:
            cart2.append(c)
            
    products = Products.query.all()
    return render_template('laptops.html',products = products,data=current_user,cart=cart2)
    
@app.route('/logout')
@token_required
def logout(current_user):
    products=Products.query.all()
    session.pop("jwt")
    session.clear()
    return render_template('userHome.html',products=products)

@app.route('/register', methods= ["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest() 

        # register the new user to the database
        new_user = UserDetails(username = username, email = email, password = hashedPassword)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest()
        result = UserDetails.query.filter_by(username = username).first()
        if result == None or hashedPassword != result.password:
            return "Invalid email or password"
        token = jwt.encode({'user':result.email, 'exp': datetime.utcnow()+timedelta(minutes=15)}, app.config['SECRET_KEY'])
        session["jwt"] = token
        return redirect(url_for('dashboard'))
    return render_template("login.html")

# @app.route('/editProduct')
# @token_required
# def editProd(current_user):
#     products = Products.query.all()
    
#     return render_template('editProduct.html', data=current_user,products=products)

@app.route('/dashboard')
@token_required
def dashboard(current_user):
    cart=Cart.query.all()
    users=UserDetails.query.all()
    for u in users:
        if current_user == u.email:
            uid=u.id
    cart2=[]
    for c in cart:
        if uid == c.user_id:
            cart2.append(c)
            
    products = Products.query.all()
    return render_template('dashboard.html',products = products,data=current_user,cart=cart2)

@app.route('/addProduct', methods=["GET","POST"])
@token_required
def addProduct(current_user):
    if request.method =="POST":
          prod_name = request.form['name']
          price = request.form['price']
          category = request.form['category']
          desc = request.form['description']
          image = request.form['image']
          new_product = Products(description=desc,price=price, name=prod_name, image=image, category=category)
          db.session.add(new_product)
          db.session.commit()
          return render_template('admin_panel.html')
    return render_template('addProduct.html', data = current_user)

@app.route('/admin', methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        result = Admins.query.filter_by(username = username).first()
        if result == None or password != result.password:
            return "Invalid email or password"
        token = jwt.encode({'user':result.email, 'exp': datetime.utcnow()+timedelta(minutes=15)}, app.config['SECRET_KEY'])
        session["jwt"] = token
        return render_template('admin_panel.html')
    return render_template("admin_login.html")


@app.route('/shipping/<price>',methods=["GET","POST"])
@token_required
def shipping(current_user,price):
    if request.method=="POST":
        user=UserDetails.query.all()
        for u in user:
            if u.email==current_user:
                user_id=u.id
        items = Cart.query.filter_by(user_id=user_id)
        for i in items:
            db.session.delete(i)
        db.session.commit()
        return render_template("Thanks.html")
        
    
    return render_template('shipping.html',price=price)

@app.route('/addCart/<product_id>')
@token_required
def addCart(current_user,product_id):
    user=UserDetails.query.all()
    for u in user:
        if u.email==current_user:
            user_id=u.id
    cart = Cart.query.filter_by(product_id=product_id).first()
    new_item=Cart(user_id=user_id,product_id=product_id,qty=1)
    db.session.add(new_item)
    db.session.commit()
    
    return redirect(url_for('dashboard'))
    
@app.route('/addCartlaptop/<product_id>')
@token_required
def addCart1(current_user,product_id):
    user=UserDetails.query.all()
    for u in user:
        if u.email==current_user:
            user_id=u.id
    #cart = Cart.query.filter_by(product_id=product_id).first()
    new_item=Cart(user_id=user_id,product_id=product_id,qty=1)
    db.session.add(new_item)
    db.session.commit()
    
    cart=Cart.query.all()
    users=UserDetails.query.all()
    for u in users:
        if current_user == u.email:
            uid=u.id
    cart2=[]
    for c in cart:
        if uid == c.user_id:
            cart2.append(c)
            
    products = Products.query.all()
    return render_template('laptops.html',products = products,data=current_user,cart=cart2)
    #return redirect(url_for('laptops'))

@app.route('/addCartmobile/<product_id>')
@token_required
def addCart2(current_user,product_id):
    user=UserDetails.query.all()
    for u in user:
        if u.email==current_user:
            user_id=u.id
    #cart = Cart.query.filter_by(product_id=product_id).first()
    new_item=Cart(user_id=user_id,product_id=product_id,qty=1)
    db.session.add(new_item)
    db.session.commit()
    
    cart=Cart.query.all()
    users=UserDetails.query.all()
    for u in users:
        if current_user == u.email:
            uid=u.id
    cart2=[]
    for c in cart:
        if uid == c.user_id:
            cart2.append(c)
            
    products = Products.query.all()
    return render_template('mobiles.html',products = products,data=current_user,cart=cart2)
    #return redirect(url_for('mobiles'))
    

@app.route('/addCartother/<product_id>')
@token_required
def addCart3(current_user,product_id):
    user=UserDetails.query.all()
    for u in user:
        if u.email==current_user:
            user_id=u.id
    #cart = Cart.query.filter_by(product_id=product_id).first()
    
    new_item=Cart(user_id=user_id,product_id=product_id,qty=1)
    db.session.add(new_item)
    db.session.commit()
    
    cart=Cart.query.all()
    users=UserDetails.query.all()
    for u in users:
        if current_user == u.email:
            uid=u.id
    cart2=[]
    for c in cart:
        if uid == c.user_id:
            cart2.append(c)
            
    products = Products.query.all()
    return render_template('others.html',products = products,data=current_user,cart=cart2)
    #return redirect(url_for('others'))

@app.route('/cart')
@token_required
def cart(current_user):
    count = 0
    price = 0
    user=UserDetails.query.all()
    for u in user:
        if u.email==current_user:
            user_id=u.id
    items = Cart.query.filter_by(user_id=user_id)
    for i in items:
        count = count + 1
        price = price + i.product.price
    return render_template('cart.html',items=items,count=count,price=price)

@app.route('/dashboardnew')
@token_required
def dashnew(current_user):
    
    cart=Cart.query.all()
    
    users=UserDetails.query.all()
    for u in users:
        if current_user == u.email:
            uid=u.id
    cart2=[]
    for c in cart:
        if uid == c.user_id:
            cart2.append(c)
            
    products = Products.query.all()
    return render_template('dashboard.html',products = products,data=current_user,cart=cart2)


# @app.route('/editForm/<product_id>',methods=["GET","POST"])
# def editForm(product_id):
#     if request.method =="POST":
#         prod_name = request.form['name']
#         price = request.form['price']
#         category = request.form['category']
#         desc = request.form['description']
#         image = request.form['image']
#         product=Products.query.all()
#         for p in product:
#             print(p.id)
#             if int(p.id)==int(product_id):
#                 if image!=None:
#                     p.image=image            
                  
#                 if desc!=None:
#                     p.description=desc
                  
#                 if prod_name!=None:
#                     p.name=prod_name
                      
#                 if category!=None:
#                     p.category=category
                  
#                 if price!=None:
#                     p.price=price
                
#                 db.session.commit()
                
#                 return render_template('admin_panel.html')
    
#     return render_template("editForm.html",product_id=product_id)