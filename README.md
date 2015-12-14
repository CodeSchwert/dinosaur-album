# Item Catalogue - Dinosaur Album

The Dinosaur Album is an online scrap book for users to collectively upload and edit information about their favourite dinosaurs. The application was originally built as a Udacity Nandegree project, but turned into a Dino-oriented endeavour for my dinosaur obsessed 3 year old son to use it as a place for learning about different dinosaur species.

## Prerequisites

- Python 2.7.9+
- Flask 0.10+
- SQLAlchemy
- Vagrant 1.7.4+
- Google Account

## Application Files

* application.py
	- Flask application code file. The main Flask web application runs from here.

* client_secrets.json
	- This is not included in the Git repository for security reasons, and needs to be generated for the application using the Google developer console.

* database_model.py
	- Defines the SQLAlchemy database classes.

* loaditems.py
	- Loads a set of 'starter' items into the database.

* /static/js/catalogue.js
	- Client side JavaScript for loading data from the Flask app using AJAX.

* Included Libraries
	- Bootstrap 4 Alpha
	- holder.js (for image place holders)

## Application Setup

Fire up a Vagrant Box using the included Vagrant file at the root of the project folder, then `Vagrant ssh` to log into the VM and navigate to the project folder, `cd /vagrant/catalog`.

Once in the Vagrant project folder, load the starter set of items `python loaditems.py`, then start the application: `python application.py`.

Then point a browser at the local address and port displayed by Flask.

Don't forget to update the `app.secret_key`, `app.debug`, and application port settings if running in a production environment!

## Notes

(maybe later ...)