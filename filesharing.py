# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 18:07:42 2019

@author: harid
"""
from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'H:/Photos'
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
      return 'file uploaded successfully'
		
if __name__ == '__main__':
   app.run(host="0.0.0.0")