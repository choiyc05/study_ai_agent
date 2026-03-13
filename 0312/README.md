## postgres 이미지 다운로드
```bash
docker pull postgres:15.17
```

## postgress container 생성
```bash
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=1234 --name pg postgres:15.17
```