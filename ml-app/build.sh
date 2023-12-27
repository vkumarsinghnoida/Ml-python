docker build -t myapp .
sh ../push.sh
clear
docker run -it --rm --network=host myapp
