# SGBDA_PROJECT_2

docker-compose up -d

-- give the container some time

docker cp ddl.cql cassandra:/tmp/ddl.cql
docker exec -it cassandra cqlsh -f /tmp/ddl.cql    

pip install -r requirements.txt
--creation de la base de donnés
py script.py 

docker cp dml.cql cassandra:/tmp/dml.cql
docker exec -it cassandra cqlsh -f /tmp/dml.cql    
