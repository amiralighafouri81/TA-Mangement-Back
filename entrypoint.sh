#!/bin/sh

# Wait for the database to be ready

echo "Waiting for database..."

#while ! python manage.py migrate ; do
while ! python3 -c "import MySQLdb, os; MySQLdb.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), database=os.getenv('DB_NAME')).close()"; do
  echo "Database not ready. Retrying..."
  sleep 10
done
python manage.py migrate

# Start the Django development server
echo "Starting Django server..."
exec python3 manage.py runserver 0.0.0.0:8000

