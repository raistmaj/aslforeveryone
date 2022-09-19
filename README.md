## Requirements

Run ```pip3 install ``` of the following packages

- scipy
- six
- numpy
- pandas
- matplotlib
- sklearn
- asyncio
- websockets
- seaborn
- keras
- opencv-python
- IPython
- livelossplot
- Pillow (for images)
- tensorflow (Run ```pip3 install tensorflow-macos``` if you are using an M1/M2 chip or if you are using gpu ```pip3 install tensorflow-gpu```)
- protobuf, (this is a bit messed up and you may need to down grade ```pip3 install protobuf==3.19.4```)

## Streaming service

nginx with rtmp module

```brew tap denji/nginx```
```brew install nginx-full --with-rtmp-module```

Update config with the following section

```
rtmp {
        server {
                listen 1935;
                chunk_size 4096;
                allow publish 127.0.0.1;
                deny publish all;

                application show {
                        live on;
                        record off;
                }
        }
}
```

Run it (you may need to modify the configuration file because of the pid file)

```
nginx -c /opt/homebrew/etc/nginx/nginx.conf
```

## Forward data from ffmepg to rtmp

```ffmpeg -re -i STREAM_ADDRESS -c:v libx264 -c:a aac -f flv rtmp://localhost/show/stream```