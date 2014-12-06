
from main import app
from flask import Flask, render_template, request, flash, session, redirect, url_for
import datetime

@app.route('/')
def index():
        return render_template('index.html')




















