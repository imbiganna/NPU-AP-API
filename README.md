# NPU_API_Ver1.0.0
國立澎湖科技大學 校務系統 非官方API

## Requirement
Python 3.7

## Installation

```bash
pip3 install -r requriment.txt
```

## Usage
``` bash
python3 server.py
```

## Using Docker-compose

``` bash
docker pull imbiganna/npuapi:latest
sudo docker run -d --restart=always -p 3000:3000 --name npuapi imbiganna/npuapi:latest
```
