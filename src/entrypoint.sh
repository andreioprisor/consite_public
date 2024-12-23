#!/bin/sh
# Exit script in case of error
set -e

echo ">>> Setup DB Migration before container starts <<<"

# Check if database is ready (adjust as per your DB and wait logic)
# This loop waits until mysql can be connected to before proceeding
while mysqladmin -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" ping --silent &> /dev/null; [ $? -ne 0 ];
do
    sleep 1
    echo "Waiting for database to be ready..."
done


echo "Running database migrations..."
npx sequelize db:migrate

echo ">>> DB Migration completed <<<"
eck " >>> Checking if seed data needs to be loaded <<<"

# if [ "$SEED_DATA_ON_START" = "true" ]; then
# 	echo "Running seed data..."
# 	npx sequelize db:seed:all
# 	# set the seed data flag to false
# 	export SEED_DATA_ON_START=false
# 	echo ">>> Seed data loaded <<<"
# fi
# Start the application
echo "Starting the application..."
exec "$@"
