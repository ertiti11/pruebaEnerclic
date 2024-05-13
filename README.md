# How to setup 

## 1. build docker images
```bash
 docker build -t chatserver -f .\Dockerfile_server .
```

```bash
 docker build -t chatclient -f .\Dockerfile_client .
```

## 2. Run the server
```bash
docker run -p 4444:4444 chatserverr
```

## 3. Run the client
```bash
docker run -it chatclient
```