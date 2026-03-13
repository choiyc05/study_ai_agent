## n8n 컨테이너 생성

- `n8nio/n8n:2.7.3` 이미지 변경

```yml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:2.7.3
    container_name: n8n
    environment:
      - N8N_HOST=aiedu.tplinkdns.com
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production
      - WEBHOOK_URL=http://aiedu.tplinkdns.com:[자신PC포트]
      - N8N_SECURE_COOKIE=false
      - TZ=Asia/Seoul
      - GENERIC_TIMEZONE=Asia/Seoul
      - LC_ALL:en_US.UTF-8
    ports:
      - 5678:5678
    volumes:
      - n8n_storage:/home/node/.n8n

volumes:
  n8n_storage:
```

- [접속](http://localhost:5678)

## Discord 메시지 수신

1. `Discord 커뮤니티 노드 설치`
- n8n에서 `Settings → Community nodes → Install a community node`

```bash
n8n-nodes-discord-trigger-new
```

2. Discord Trigger 노드 추가
- `자격 증명 연결` (Discord Bot Token, Application ID, n8n API Key 필요)
- [Discord API](https://discord.com/developers/home)
- OAuth2 권한 URL : `bot`, `applications.commands` (생성된 URL 실행)
- 봇 토큰 생성 : `Privileged Gateway Intents` ( Presence Update, Guild Members, Message Content Intent )
