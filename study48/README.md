## Spark 구성하기

 - [Spark 다운로드] (https://dlcdn.apache.org/spark/spark-4.1.1/spark-4.1.1-bin-hadoop3.tgz)
 - Dockerfile 생성

```bash
FROM ubuntu:22.04
RUN apt-get update
RUN apt-get -y install wget openjdk-21-jdk

WORKDIR /opt/spark
RUN wget https://dlcdn.apache.org/spark/spark-4.1.1/spark-4.1.1-bin-hadoop3.tgz
# 압축 해제 / 압축 파일 삭제
RUN tar -zxvf spark-4.1.1-bin-hadoop3.tgz
RUN rm spark-4.1.1-bin-hadoop3.tgz

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV SPARK_HOME=/opt/spark/spark-4.1.1-bin-hadoop3
ENV PATH="$PATH:${SPARK_HOME}/bin:${SPARK_HOME}/sbin"
ENV SPARK_NO_DAEMONIZE=true
```

```bash
docker build -t my-spark:0.1 .
```

```bash
source .bashrc
env
```

- Docker container 생성
```bash
docker run -d -it -p 8080:8080 -p 7077:7077 -e SPARK_PUBLIC=localhost --name master my-spark:0.1
```

 - Sparkjps
```
root@97fb07b3bad0:/opt/spark/spark-4.1.1-bin-hadoop3/sbin# bash ./start-master.sh
```


## uv 형식 jupyther 알아보기

- 프로젝트 생성 / jupyter 모듈 설치 / 실행

```bash
uv init .
uv add --dev ipykernel
uv run --with jupyter jupyter lab
```

 - docker container 내 파일 복사
```bash
docker cp sample.txt master:/opt/spark/data/
docker cp (복사할 파일명 또는 절대 경로) (컨테이너명):(복사할 위치)
```