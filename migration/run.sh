python src/spacetelescope/manage.py reset_db --noinput
python src/spacetelescope/manage.py syncdb --noinput
python src/spacetelescope/manage.py satchmo_load_l10n
python src/spacetelescope/manage.py loaddata menus
python src/spacetelescope/manage.py loaddata taxonomy
python src/spacetelescope/manage.py loaddata shop
python src/spacetelescope/manage.py loaddata shipping
python src/spacetelescope/manage.py loaddata pages
python src/spacetelescope/manage.py loaddata release_types
python migration/import.py