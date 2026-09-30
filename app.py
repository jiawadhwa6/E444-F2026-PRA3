# from flask import Flask, render_template, session, redirect, url_for
# from forms import NameEmailForm

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'dev-secret-key-123'

# @app.route('/')
# def index():
#     return render_template('index.html', name='Jia')

# @app.route('/form', methods=['GET', 'POST'])
# def form_page():
#     form = NameEmailForm()
#     if form.validate_on_submit():
#         session['name'] = form.name.data
#         session['email'] = form.email.data
#         return redirect(url_for('result'))
#     return render_template('form.html', form=form)

# @app.route('/result')
# def result():
#     name = session.get('name', 'Stranger')
#     email = session.get('email', '')
#     return render_template('result.html', name=name, email=email)

# if __name__ == '__main__':
#     app.run(debug=True,  host='0.0.0.0')

from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from forms import NameEmailForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-123'

@app.route('/')
def index():
    return render_template('index.html', name='Jia')

@app.route('/form', methods=['GET', 'POST'])
def form_page():
    form = NameEmailForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['email'] = form.email.data
        session['chat_history'] = []  # Initialize chat history
        return redirect(url_for('chat_page'))
    return render_template('form.html', form=form)

@app.route('/chat')
def chat_page():
    if 'name' not in session:
        return redirect(url_for('form_page'))
    return render_template('chat.html', name=session['name'])

@app.route('/chat', methods=['POST'])
def chat():
    if 'name' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    message = request.json.get('message', '').strip()
    if not message:
        return jsonify({'reply': ''})
    
    # Get chat history from session
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    chat_history = session['chat_history']
    user_name = session.get('name', '')
    
    # Chatbot logic with memory
    reply = ''
    
    # Extract user information from message
    if 'my name is' in message.lower():
        # Extract name from message like "My name is Alice"
        parts = message.lower().split('my name is')
        if len(parts) > 1:
            extracted_name = parts[1].strip().strip('.')
            session['chat_name'] = extracted_name
            reply = f"Nice to meet you, {extracted_name}!"
    
    elif 'what is my name' in message.lower() or 'who am i' in message.lower():
        if 'chat_name' in session:
            reply = f"Your name is {session['chat_name']}."
        else:
            reply = f"Your name is {user_name}."
    
    elif 'hello' in message.lower():
        if 'chat_name' in session:
            reply = f"Hello {session['chat_name']}! How can I help?"
        else:
            reply = f"Hello {user_name}! How can I help?"
    
    elif 'my email' in message.lower() or 'my utoft email' in message.lower():
        session['chat_email'] = session.get('email', '')
        reply = f"I've noted your email: {session['chat_email']}"
    
    elif 'what is my email' in message.lower():
        if 'chat_email' in session:
            reply = f"Your email is {session['chat_email']}."
        else:
            reply = f"Your email is {session.get('email', 'unknown')}."
    
    else:
        reply = "I don't understand. Try telling me your name or asking what your name is!"
    
    # Store in chat history
    chat_history.append({'user': message, 'bot': reply})
    session['chat_history'] = chat_history
    
    return jsonify({'reply': reply})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)