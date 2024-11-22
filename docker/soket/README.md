lanciare il docker:
```docker run -it -d --name ssh-socks-proxy -v "$PWD/../../.ssh/spaip_rsa:/root/.ssh/id_rsa" -p 1080:1080 ssh-socks-proxy```
```docker run -it -d --name ssh-socks-proxy -v ~/.ssh/id_rsa:/root/.ssh/id_rsa -e REMOTE_USER=<user> -e REMOTE_IP=<ip> -p 1080:1080 ssh-socks-proxy```
esempio di test:
```lsof -i :1080```
```curl --socks5-hostname localhost:1080 192.168.1.198```
