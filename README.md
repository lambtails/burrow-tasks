# Burrow Tasks

To-do list tool built using Python, SQLite and Flask/Django. 

<img width="274" height="232" alt="screenshot of burrow tasks" src="https://github.com/user-attachments/assets/bc5532cc-97eb-44cc-a9c6-1890328bff36" />

## Purpose

Designed to be lightweight and simple for deployment to a small VPS, so I can access my tasks from all my devices over the internet. 

### Implementation notes

This application doesn't have any security features, instead I'm using mTLS to restrict client access to this server on my VPS, so that only myself or anyone with the cert can access it.

This project is very much a proof of concept to see what I can achieve with a minimal server setup, and lacks most of the features you'd expect to see in a task management app. 
That said, it's been much easier to see and manage my tasks with this than any other tool I've tried. I'm hoping for it to eventually replace my Obsidian + SyncThing setup for task management.

## Getting started

This project assumes you have a basic knowledge of python and git.

1. Download the repository
2. Setup a python virtual environment `python -m venv .venv`
3. Set your source to the virtual environment `source .venv/bin/activate`
4. Install requirements `python -m pip install -r requirements.txt`
5. Run `flask -A app.py run` to start the server and create an empty database

By default, the application will be at http://127.0.0.1:5000

Have fun!
