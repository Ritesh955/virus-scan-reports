#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, flash, Response, url_for
app = Flask(__name__)
from flask import jsonify
import requests
import json
import mysql.connector
import time
from werkzeug.utils import secure_filename
from app import app
import os
import urllib.request
from services import query_service
from services import helper_service
from services import email_service
from services import pdf_service

ALLOWED_EXTENSIONS = set(['txt'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        email = request.form['email']
        if file.filename == '' or email == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], app.config['FILE_NAME']+'.txt'))
            flash('File successfully uploaded')
            return redirect(url_for('.get_report', messages=email))
        elif file and not  allowed_file(file.filename):
            flash('Please upload a txt file')
            return redirect(request.url)


@app.route('/get_report', methods=['POST','GET'])
def get_report():
    try:
        file = open(os.path.join(app.config['UPLOAD_FOLDER'], app.config['FILE_NAME']+'.txt'))
        report_file_path = app.config['UPLOAD_FOLDER']+'/report.pdf'
        email = request.args['messages']
        hash_values = [line.strip() for line in file]
        total = len(hash_values)
        counter = 0
        report = []
        for lines in list(helper_service.divide_chunks(hash_values, 4)):
            api_server_hits = 0
            for line in lines:
                try:
                    response = query_service.query_database(line)
                    if 'update_flag' in response.keys() and 'value' in response.keys():
                        report.append(query_service.query_server(response['value'],response['update_flag']))
                        api_server_hits+=1
                    else:
                        report.append(response)
                except Exception as e:
                    print(e)
                    continue
            counter += len(lines)
            if api_server_hits>0:
                time.sleep(60)
            print("Percentage of records processed: {}%".format((counter/total)*100))
        pdf_service.create_report_pdf(report,report_file_path)
        email_service.send_email(app.config['GENERIC_EMAIL'],email,app.config['PASSWD'],'report.pdf',report_file_path)
        return "Please find the report attached in the email sent to: "+ email
    except Exception as e:
        print(e)

@app.errorhandler(404)
def not_found(error=None):
    message = {'status': 404, 'message': 'Not Found: ' + request.url}
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8000, use_reloader=False)
