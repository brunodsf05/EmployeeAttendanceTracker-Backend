# Cachea las credenciales de git
cache_git:
	git config --local credential.helper store

# Lee el repositorio y realiza las migraciones de la base de datos
pull:
	git pull origin main

# Solo realizar las migraciones de la base de datos
update:
	flask db migrate
	flask db upgrade

# Alias
c: cache_git
p: pull
u: update