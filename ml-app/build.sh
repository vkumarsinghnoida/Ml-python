docker build -t myapp .
./push.sh
clear
docker run -it --rm --network=host myapp
