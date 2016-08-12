from flask import Flask, redirect, url_for, request, flash
from flask import render_template, send_from_directory, Markup
from werkzeug import secure_filename
import get_gpsinfo
from PIL import Image
import glob, os

size = 128, 128

def get_thumbnail(im):

    file = im.split('.')[0]
    im = Image.open(im)
    im.thumbnail(size)
    thumbnail=im.save(file + ".thumbnail", "JPEG")

app = Flask(__name__)

@app.route('/')
def hello(name=None):
    return render_template('main.html', name=name)
    #return 'Hello Idiot'
@app.route('/message')
def mess(name=None):
	return render_template('message.html', name=name)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/imgmap',methods = ['POST', 'GET'])
def login(name=None):
	#return render_template('imgmap.html', name=name)
	if request.method == 'POST':
		rad = request.form['rad']
		img_f = request.files['pic']
		#img_f.save('/media/image.jpg')
		try:
			#img_f.save(secure_filename('static/'+ img_f.filename))
			img_f.save('static/'+ img_f.filename)
			gps_info = get_gpsinfo.get_loc('static/'+ img_f.filename)
		except:
			return render_template('main.html')
		if gps_info == 'A':
			message = Markup('Your Image is not Geo-Tagged. Please Upload a Geo-tagged Image')
			flash(message)
			return redirect(url_for('mess'))

			#return 'Your Image is not Geo-Tagged. Please Upload a Geo-tagged Image'
			
		else:
			get_thumbnail('static/'+ img_f.filename)
			thmb = img_f.filename.split('.')[0] + '.thumbnail'
			return render_template('imgmap.html', name=name,lat=gps_info[0],long=gps_info[1], thmb = thmb, rad=rad)


		#get_gpsinfo.info('/images/image.jpg')
		#return redirect(url_for('imgmap',name = user))
	else:
			return render_template('main.html')
if __name__ == '__main__':
	app.secret_key = 'super secret key'
	app.config['SESSION_TYPE'] = 'filesystem'
   	app.run(debug=True, host='0.0.0.0')