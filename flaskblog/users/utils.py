from PIL import Image
import secrets, os
import smtplib, ssl
from email.mime.text import MIMEText
from flask import url_for, current_app



def save_picture(form_picture):
	random_hex = secrets.token_hex(8) #randomize img name so that it doesn't collide with existing image of the same original name
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) # full path of image
	
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn

def send_reset_email(user):
	sender = current_app.config['MAIL_USERNAME']
	password = current_app.config['MAIL_PASSWORD']
	receiver = user.email
	subject =  'Password Reset'
	port = current_app.config['MAIL_PORT']

	context = ssl.create_default_context()
	token = user.get_reset_token()

	body = f'''To reset password, please clink the link below:
	{url_for('users.reset_token', token=token, _external=True)}

	If you didn't make this requrst, kindly ignore this message.
	'''

	message = MIMEText(body)
	message['From'] = sender
	message['To'] = receiver
	message['Subject'] = subject
	message['Bcc'] = receiver
	
	text = message.as_string()
	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		server.login("timsnoreplyautomatedbot@gmail.com", password)
		server.sendmail(sender, receiver, text)
