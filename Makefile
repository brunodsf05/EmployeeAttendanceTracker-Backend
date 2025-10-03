# COMMANDS ####################################################################

# Initialize and apply database migrations after cloning
init:
	pip install -r requirements.txt
	flask db init
	flask db migrate
	flask db upgrade

# Apply migrations after modifying database models
dbmigrate:
	flask db migrate
	flask db upgrade

# Run the development server
run:
	flask run --host=0.0.0.0 --port=5000



# ALIASES #####################################################################
i: init
m: dbmigrate
r: run