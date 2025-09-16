For Restore the file 
postgresql command 

psql -h db -p 5432 -U postgres -d emp_db -f /home/atlantick-solutions/Desktop/Ankit Mishra/Employee-Management/Database/emp_db.sql
pg_restore -h localhost -p 5432 -U postgres -d employee_management "/home/atlantick-solutions/Desktop/Ankit Mishra/Employee-Management/Database/emp_db.sql"





Basic Restore Command
bashpsql -h db -p 5432 -U postgres -d employee_management -f your_backup.sql
With Password (will prompt)
bashPGPASSWORD=root psql -h db -p 5432 -U postgres -d employee_management -f your_backup.sql
Alternative Syntax
bashPGPASSWORD=root psql -h db -p 5432 -U postgres employee_management < your_backup.sql
Using Environment Variables
You can also set the password as an environment variable to avoid typing it:
bashexport PGPASSWORD=root
psql -h db -p 5432 -U postgres -d employee_management -f your_backup.sql
Docker Context Commands
If you're running this in a Docker environment (which seems likely given DB_HOST=db), you might need:
From host machine:
bashdocker exec -i your_postgres_container psql -U postgres -d employee_management < your_backup.sql
Copy file to container first:
bashdocker cp your_backup.sql your_postgres_container:/tmp/
docker exec -it your_postgres_container psql -U postgres -d employee_management -f /tmp/your_backup.sql
Notes for Your Setup

Replace your_backup.sql with the actual path to your SQL file
The database employee_management must already exist
If you're connecting from outside Docker, make sure the PostgreSQL container port is exposed
The hostname db suggests you're using Docker Compose with a service named db

Which approach fits your current setup?RetryClaude does not have the ability to run the code it generates yet.