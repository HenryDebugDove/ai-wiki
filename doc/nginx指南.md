# Nginx 完整实用指南

**Nginx 是一款高性能的 Web 服务器与反向代理工具**，主要负责接收外网 HTTP/HTTPS 请求，统一分发、转发到后端服务（如 Next.js、Node、Java、FastAPI 等），同时提供 HTTPS、缓存、限流、安全防护等能力，是项目上线必备的流量入口。


---

## 一、最核心、必须做的 3 件事（上线刚需）

### 1. 反向代理：用域名访问，隐藏端口

#### 解决的问题

- 避免暴露后端真实端口，更安全规范
- 用户只需访问域名，无需记住端口号
- 统一入口，方便后续扩展多项目

#### 操作步骤（宝塔面板可视化）

1. 宝塔 → 网站 → 添加站点
   - 域名：填你的域名（无域名可填服务器IP）
   - 根目录：随便填（会被代理覆盖）
   - PHP 版本：纯静态
   - 数据库：不创建
   - 提交
2. 站点设置 → 反向代理
   - 目标URL：`http://127.0.0.1:3000`（本地内网，不暴露公网）
   - 发送域名：`$host`
   - 勾选：保留源站Host
   - 添加

---

### 2. 配置 HTTPS：免费 SSL 证书

#### 解决的问题

- 浏览器不再提示“不安全”
- 小程序/APP/公众号强制要求 HTTPS
- 数据传输加密，防劫持窃听

#### 操作步骤

1. 站点设置 → SSL
2. 选择 Let’s Encrypt（免费自动续期）
3. 勾选域名 → 申请
4. 开启：强制HTTPS

---

### 3. 解决 单页面（Next.js等）路由刷新 404

#### 解决的问题

Next.js 单页应用刷新子路由会 404，需 Nginx 统一指向入口文件。

```nginx
location / {
    try_files $uri $uri/ /index.html;
    proxy_pass http://127.0.0.1:3000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

---

## 二、Nginx 常用配置模块（直接复制可用）

### 4. 静态资源缓存（加速加载）

```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
    proxy_pass http://127.0.0.1:3000;
}
```

### 5. 接口限流 & 防刷

```nginx
limit_req_zone $binary_remote_addr zone=nextjs:10m rate=10r/s;

server {
    ...
    location / {
        limit_req zone=nextjs burst=20 nodelay;
        ...
    }
}
```

### 6. 一台服务器跑多个项目（域名分发）

```nginx
# 主站
server {
    server_name www.xxx.com;
    location / {
        proxy_pass http://127.0.0.1:3000;
    }
}

# 后台
server {
    server_name admin.xxx.com;
    location / {
        proxy_pass http://127.0.0.1:3001;
    }
}
```

### 7. 负载均衡（多实例高并发）

```nginx
upstream nextjs_backend {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
}

server {
    location / {
        proxy_pass http://nextjs_backend;
    }
}
```

---

## 三、线上安全与优化建议

1. **只开放 80/443/22 端口**，关闭后端端口公网访问
2. 开启**进程守护**，保证 Nginx 崩溃自动重启
3. 后端服务绑定 `127.0.0.1`，不对外暴露
4. 配置 `client_max_body_size 100M;` 支持大文件上传

---

## 四、完整可直接复制的 Nginx 最终配置（Next.js 专用）

```nginx
server {
    listen 80;
    server_name 你的域名;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name 你的域名;

    ssl_certificate 证书路径;
    ssl_certificate_key 私钥路径;

    # 反向代理
    location / {
        try_files $uri $uri/ /index.html;
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 静态缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
        proxy_pass http://127.0.0.1:3000;
    }

    # 安全屏蔽
    location ~ /\. {
        deny all;
        access_log off;
    }
}
```

---

## 五、Nginx 核心价值总结

| 功能        | 作用               | 优先级     |
| ----------- | ------------------ | ---------- |
| 反向代理    | 隐藏端口、统一入口 | ⭐⭐⭐⭐⭐ |
| HTTPS       | 安全、合规         | ⭐⭐⭐⭐⭐ |
| 路由404修复 | Next.js 必需       | ⭐⭐⭐⭐⭐ |
| 静态缓存    | 加速、省流量       | ⭐⭐⭐⭐   |
| 限流防攻击  | 保护服务           | ⭐⭐⭐⭐   |
| 多项目分发  | 一台服务器跑多站   | ⭐⭐⭐     |
| 负载均衡    | 高并发、高可用     | ⭐⭐⭐     |
