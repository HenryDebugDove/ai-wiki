# WebSocket 保活 + 自动重连（一次讲清楚）

这篇把你刚刚问的 **WebSocket 保活 + 自动重连** 全部整理到一起，方便以后直接查。

---

# 一、WebSocket 是什么

**WebSocket = 浏览器和服务器的长连接通信**

和 HTTP 的区别：

| 对比           | WebSocket        | HTTP         |
| -------------- | ---------------- | ------------ |
| 连接方式       | 长连接           | 短连接       |
| 实时性         | 很高             | 较低         |
| 服务器主动推送 | 可以             | 不可以       |
| 使用场景       | 聊天、推送、游戏 | 普通接口请求 |

---

# 二、WebSocket 保活是什么

**WebSocket 保活 = 防止连接断开**

因为：

* 网络会断
* 浏览器会断
* 服务器会断
* 网关会断

所以需要：

👉 定时发 **心跳包**

---

# 三、WebSocket 保活原理

最常见做法：

| 客户端 | 服务端 |
| ------ | ------ |
| ping   | pong   |

流程：

```
客户端 → ping → 服务器
客户端 ← pong ← 服务器
```

每 30 秒发一次

---

# 四、为什么要 WebSocket 保活

举几个业务例子 👇

### 1️⃣ 聊天系统

比如：

* 在线客服
* 聊天系统
* IM系统

如果没有保活：

```
用户挂机10分钟
↓
连接断开
↓
收不到消息
```

---

### 2️⃣ 实时行情

比如：

* 股票
* 币价
* 黄金

必须保持实时连接

---

### 3️⃣ 在线游戏

比如：

* 棋牌游戏
* 对战游戏

不能断线

---

# 五、WebSocket 自动重连是什么

**自动重连 = 连接断开后自动重新连接**

例如：

```
网络断开
↓
WebSocket断开
↓
自动重新连接
↓
恢复通信
```

---

# 六、为什么需要自动重连

常见断线原因：

| 原因       | 说明       |
| ---------- | ---------- |
| 网络波动   | WiFi断开   |
| 服务器重启 | 服务更新   |
| 浏览器休眠 | 页面挂后台 |
| 代理超时   | 网关断开   |

所以：

👉 必须自动重连

---

# 七、保活 vs 自动重连

| 功能     | 保活     | 自动重连 |
| -------- | -------- | -------- |
| 作用     | 防止断线 | 断线恢复 |
| 是否必须 | 推荐     | 推荐     |
| 使用时机 | 连接中   | 断线后   |
| 企业级   | 必须     | 必须     |

---

# 八、企业级完整方案

真实项目一般这样：

```
WebSocket
   ↓
心跳检测
   ↓
断线检测
   ↓
自动重连
   ↓
恢复订阅
```

---

# 九、WebSocket 保活代码（前端）

```javascript
const ws = new WebSocket("ws://localhost:8080");

ws.onopen = () => {

    setInterval(() => {
        ws.send("ping");
    }, 30000);

};

ws.onmessage = (e) => {
    console.log(e.data);
};
```

---

# 十、自动重连代码

```javascript
let ws;

function connect() {

    ws = new WebSocket("ws://localhost:8080");

    ws.onopen = () => {
        console.log("连接成功");
    };

    ws.onclose = () => {
        setTimeout(connect, 3000);
    };

}

connect();
```

---

# 十一、生产级（保活 + 自动重连）

推荐用这个 👇

```javascript
let ws;
let timer;

function connect() {

    ws = new WebSocket("ws://localhost:8080");

    ws.onopen = () => {
        startHeartbeat();
    };

    ws.onclose = () => {
        stopHeartbeat();
        reconnect();
    };

}

function startHeartbeat() {

    timer = setInterval(() => {
        ws.send("ping");
    }, 30000);

}

function stopHeartbeat() {
    clearInterval(timer);
}

function reconnect() {

    setTimeout(() => {
        connect();
    }, 3000);

}

connect();
```

---

# 十二、企业级优化（指数退避）

防止疯狂重连

```javascript
let time = 1000;

function reconnect() {

    setTimeout(() => {

        connect();

        time *= 2;

        if (time > 30000) {
            time = 30000;
        }

    }, time);

}
```

---

# 十三、常见业务场景

| 场景     | 是否需要 |
| -------- | -------- |
| 聊天系统 | 必须     |
| 实时行情 | 必须     |
| 推送系统 | 推荐     |
| 在线游戏 | 必须     |
| 监控系统 | 推荐     |

---

# 十四、支持哪些语言

| 语言       | 支持 |
| ---------- | ---- |
| JavaScript | ✅   |
| Java       | ✅   |
| Python     | ✅   |
| Go         | ✅   |
| C#         | ✅   |
| Node.js    | ✅   |
| PHP        | ✅   |

---

# 十五、面试回答模板

面试官问：

**WebSocket 如何保证稳定？**

可以这样回答：

```
使用心跳机制保证连接不断开  
使用自动重连恢复断线  
使用指数退避防止频繁重连  
```

---

# 十六、推荐最佳实践

企业级推荐：

| 功能         | 是否推荐   |
| ------------ | ---------- |
| 心跳保活     | ⭐⭐⭐⭐⭐ |
| 自动重连     | ⭐⭐⭐⭐⭐ |
| 指数退避     | ⭐⭐⭐⭐   |
| 最大重连次数 | ⭐⭐⭐⭐   |

---

# 十七、一句话总结

**WebSocket稳定方案 = 保活 + 自动重连 + 心跳机制**

---
