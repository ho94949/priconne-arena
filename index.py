from flask import Flask, escape, request, send_from_directory, current_app

def mainpage():
    return send_from_directory('template', 'index.html')

def favicon():
    return send_from_directory('static/images', 'favicon.ico')