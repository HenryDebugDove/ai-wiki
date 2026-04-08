# 安全规则

## 1. 安全原则

### 1.1 最小权限原则
- 只授予必要的权限
- 避免使用管理员权限
- 定期审查权限设置
- 遵循权限分离原则

### 1.2 输入验证
- 所有用户输入必须验证
- 使用参数化查询防止 SQL 注入
- 验证所有 API 输入参数
- 限制输入长度和格式

### 1.3 输出编码
- 对所有输出进行适当编码
- 防止 XSS 攻击
- 正确设置 Content-Type 头
- 避免直接拼接 HTML

### 1.4 加密
- 敏感数据必须加密存储
- 使用 HTTPS 传输数据
- 安全存储密码（使用 bcrypt 等算法）
- 定期更新加密密钥

### 1.5 会话管理
- 使用安全的会话标识符
- 设置适当的会话超时
- 防止会话固定攻击
- 正确处理会话销毁

## 2. 禁止写法

### 2.1 SQL 注入风险

**禁止：**
```javascript
// 直接拼接 SQL 语句
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);

// 使用字符串模板拼接
const sql = `INSERT INTO users (name, email) VALUES ('${name}', '${email}')`;
```

**推荐：**
```javascript
// 使用参数化查询
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);

// 使用 ORM
User.create({ name, email });
```

### 2.2 XSS 攻击风险

**禁止：**
```javascript
// 直接插入 HTML
const userInput = '<script>alert("XSS")</script>';
document.getElementById('content').innerHTML = userInput;

// 不安全的模板字符串
const html = `<div>${userInput}</div>`;
```

**推荐：**
```javascript
// 使用 textContent
const userInput = '<script>alert("XSS")</script>';
document.getElementById('content').textContent = userInput;

// 使用安全的模板库
const html = escapeHtml`<div>${userInput}</div>`;
```

### 2.3 敏感信息泄露

**禁止：**
```javascript
// 硬编码 API Key
const apiKey = 'sk-1234567890abcdef';

// 日志中包含敏感信息
console.log('User password:', user.password);

// 错误信息暴露内部细节
try {
  // 操作
} catch (error) {
  res.send({ error: error.message });
}
```

**推荐：**
```javascript
// 使用环境变量
const apiKey = process.env.API_KEY;

// 日志中屏蔽敏感信息
console.log('User login:', user.username);

// 通用错误信息
try {
  // 操作
} catch (error) {
  console.error('Error:', error);
  res.send({ error: '操作失败，请稍后重试' });
}
```

### 2.4 不安全的依赖

**禁止：**
```javascript
// 使用过时的依赖
"dependencies": {
  "lodash": "1.0.0"
}

// 无版本控制的依赖
"dependencies": {
  "axios": "*"
}
```

**推荐：**
```javascript
// 使用最新安全版本
"dependencies": {
  "lodash": "^4.17.21"
}

// 固定版本号
"dependencies": {
  "axios": "0.27.2"
}
```

### 2.5 密码处理

**禁止：**
```javascript
// 明文存储密码
const user = { username: 'admin', password: 'password123' };

// 使用弱加密
const encryptedPassword = btoa(password);

// 密码长度过短
if (password.length < 6) {
  return '密码长度至少 6 位';
}
```

**推荐：**
```javascript
// 使用 bcrypt 加密
const hashedPassword = await bcrypt.hash(password, 10);

// 密码强度检查
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
if (!passwordRegex.test(password)) {
  return '密码至少 8 位，包含大小写字母、数字和特殊字符';
}
```

### 2.6 CORS 配置

**禁止：**
```javascript
// 过于宽松的 CORS 配置
app.use(cors({
  origin: '*',
  credentials: true
}));

// 禁用 CORS
app.use((req, res, next) => {
  res.removeHeader('Access-Control-Allow-Origin');
  next();
});
```

**推荐：**
```javascript
// 合理的 CORS 配置
app.use(cors({
  origin: process.env.NODE_ENV === 'production' ? 'https://example.com' : 'http://localhost:3000',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

### 2.7 认证与授权

**禁止：**
```javascript
// 无认证检查
app.get('/api/admin', (req, res) => {
  res.send('Admin panel');
});

// 基于客户端的授权
if (localStorage.getItem('isAdmin') === 'true') {
  // 管理员操作
}
```

**推荐：**
```javascript
// 使用中间件进行认证
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization;
  if (!token) {
    return res.status(401).send('未授权');
  }
  // 验证 token
  next();
};

app.get('/api/admin', authMiddleware, (req, res) => {
  res.send('Admin panel');
});
```

### 2.8 错误处理

**禁止：**
```javascript
// 忽略错误
try {
  // 操作
} catch (error) {
  // 什么都不做
}

// 全局捕获所有错误
process.on('uncaughtException', (error) => {
  console.log('Error:', error);
});
```

**推荐：**
```javascript
// 适当处理错误
try {
  // 操作
} catch (error) {
  console.error('Error:', error);
  // 处理错误
}

// 合理的错误处理中间件
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('服务器内部错误');
});
```

### 2.9 日志安全

**禁止：**
```javascript
// 记录敏感信息
console.log('User login:', user); // 包含密码

// 无限制的日志级别
if (debug) {
  console.log('Debug info:', sensitiveData);
}
```

**推荐：**
```javascript
// 屏蔽敏感信息
const sanitizedUser = { ...user };
delete sanitizedUser.password;
console.log('User login:', sanitizedUser);

// 基于环境的日志级别
if (process.env.NODE_ENV === 'development') {
  console.log('Debug info:', nonSensitiveData);
}
```

### 2.10 依赖包安全

**禁止：**
```javascript
// 无依赖检查
// package.json 中没有安全脚本

// 使用有已知漏洞的包
"dependencies": {
  "lodash": "4.17.11" // 有原型链污染漏洞
}
```

**推荐：**
```javascript
// 配置安全脚本
"scripts": {
  "security": "npm audit",
  "lint": "eslint ."
}

// 定期更新依赖
// 使用 npm audit 检查漏洞
```

## 3. 安全检查清单

### 3.1 代码审查检查
- [ ] 所有用户输入是否经过验证？
- [ ] 是否使用参数化查询防止 SQL 注入？
- [ ] 是否对输出进行适当编码防止 XSS？
- [ ] 是否安全存储敏感信息？
- [ ] 是否使用 HTTPS 传输数据？
- [ ] 是否有适当的错误处理？
- [ ] 是否设置合理的 CORS 配置？
- [ ] 是否有认证和授权机制？
- [ ] 是否定期检查依赖包安全？
- [ ] 是否有安全的会话管理？

### 3.2 部署检查
- [ ] 生产环境是否禁用调试信息？
- [ ] 是否移除测试代码和后门？
- [ ] 是否配置适当的防火墙规则？
- [ ] 是否启用安全的 HTTP 头部？
- [ ] 是否定期备份数据？
- [ ] 是否有灾难恢复计划？
- [ ] 是否监控安全事件？
- [ ] 是否定期进行安全扫描？

### 3.3 开发流程检查
- [ ] 是否有安全编码培训？
- [ ] 是否将安全测试集成到 CI/CD？
- [ ] 是否有安全事件响应计划？
- [ ] 是否定期更新安全知识？
- [ ] 是否进行安全代码审查？

## 4. 安全工具

### 4.1 代码分析工具
- ESLint 安全插件
- SonarQube
- OWASP ZAP
- Snyk

### 4.2 依赖检查工具
- npm audit
- yarn audit
- dependabot
- WhiteSource

### 4.3 监控工具
- Sentry
- Datadog
- New Relic
- ELK Stack

## 5. 安全事件响应

### 5.1 事件分类
- 数据泄露
- 服务中断
- 恶意攻击
- 内部威胁

### 5.2 响应流程
1. 检测和识别
2. 遏制和隔离
3. 消除威胁
4. 恢复系统
5. 分析和改进

### 5.3 报告机制
- 内部报告流程
- 外部报告要求
- 法律合规要求
- 沟通策略

## 6. 总结

安全是一个持续的过程，需要团队成员的共同努力。通过遵循这些安全规则，我们可以减少安全风险，保护用户数据，维护系统的可靠性和可信度。所有团队成员都应该了解并遵守这些安全规范，并在开发过程中积极关注安全问题。