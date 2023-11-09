docker-compose down

$backendImageExists = docker images backend:latest
if ($backendImageExists) {
    docker image rm backend-backend:latest
}

$frontendImageExists = docker images frontend:latest
if ($frontendImageExists) {
    docker image rm backend-frontend:latest
}

$databaseVolumeExists = docker volume ls --quiet --filter name=database_cs
if ($databaseVolumeExists) {
    docker volume rm backend_database_cs
}

$staticVolumeExists = docker volume ls --quiet --filter name=static_cs
if ($staticVolumeExists) {
    docker volume rm backend_static_cs
}

$mediaVolumeExists = docker volume ls --quiet --filter name=media_cs
if ($mediaVolumeExists) {
    docker volume rm backend_media_cs
}

docker compose up

