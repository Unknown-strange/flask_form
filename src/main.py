import os
import sys
from flask import Flask, request, jsonify, render_template


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, request, jsonify 
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

@app.route('/', methods=['GET'])
def serve_form():
    return render_template('form.html')



@app.route('/submit_application', methods=['POST'])
def submit_application():
    try:
        # Extract form data
        data = request.form
        full_name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        gender = data.get('gender')
        school = data.get('school')
        program = data.get('program')
        level = data.get('level')
        role = data.get('role')
        why_pick_you = data.get('why')
        other_skills = data.get('skills')


        sender_email = 'certacitodheflash@gmail.com'  
        sender_app_password = 'fofa ltsn cfvg yuvj'  
        # --- End of User Action Required ---

        recipient_email = 'futurestructltd@gmail.com'

        if sender_email == 'YOUR_GMAIL_ADDRESS_HERE' or sender_app_password == 'YOUR_ACTUAL_APP_PASSWORD':
            # Return a message indicating that email credentials need to be configured if placeholders are still present
            # This is a safeguard for the user during their setup.
            # In a production environment, you might handle this differently
            return jsonify({'status': 'error', 'message': 'Email credentials not configured in the backend. Please update main.py.'}), 500

        # Create email message
        subject = f"New Internship Application: {full_name}"
        body = f"""A new internship application has been submitted:

        Full Name: {full_name}
        Email: {email}
        Phone Number: {phone}
        Gender: {gender}
        School: {school}
        Program: {program}
        Level: {level}
        Role Interested In: {role}
        Why should we pick you?: {why_pick_you}
        Other skills: {other_skills}
        """
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender_email, sender_app_password)
            smtp_server.sendmail(sender_email, recipient_email, msg.as_string())

        return jsonify({'status': 'success', 'message': 'Application submitted successfully!'}), 200

    except Exception as e:
        print(f"Error processing submission: {e}") # Log error to server console
        return jsonify({'status': 'error', 'message': f'An error occurred: {str(e)}'}), 500

# Keep the existing static file serving for potential future use or if the form is served by Flask
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(app.static_folder, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            # If no index.html, and no specific path, perhaps a welcome message or API docs for the backend
            return jsonify({'message': 'Flask backend is running. Use /submit_application to post form data.'}), 200

if __name__ == '__main__':
    # Note: For deployment, a production WSGI server like Gunicorn should be used instead of Flask's built-in dev server.
    app.run(host='0.0.0.0', port=5000, debug=True) # debug=True is for development, set to False for production

