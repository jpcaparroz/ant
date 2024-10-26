#####
    docker inspect db-ant



#####
    docker run --name db-ant  -e POSTGRES_PASSWORD=5432 -v pgdata:/var/lib/postgresql/data -p 5432 -d postgres
