# 团队编码规范

## 1. 代码风格

### 1.1 缩进与格式
- 使用 2 个空格进行缩进
- 每行最大长度不超过 120 个字符
- 使用单引号 `'` 而非双引号 `"`
- 语句末尾使用分号 `;`
- 对象和数组使用尾随逗号

**示例：**
```javascript
// 推荐
const user = {
  id: 1,
  name: 'John',
  age: 30,
};

// 不推荐
const user = {
    id: 1,
    name: "John",
    age: 30
};
```

### 1.2 命名规范
- 变量和函数：`camelCase`
- 类和接口：`PascalCase`
- 常量：`UPPER_SNAKE_CASE`
- 文件和目录：`kebab-case`

**示例：**
```javascript
// 推荐
const userName = 'John';
function getUserData() {}
class UserService {}
const MAX_RETRY_COUNT = 3;

// 不推荐
const UserName = 'John';
function get_user_data() {}
class userService {}
const maxRetryCount = 3;
```

### 1.3 注释规范
- 函数和方法需要 JSDoc 注释
- 复杂逻辑需要详细注释
- 代码变更需要注释说明
- 避免无意义的注释

**示例：**
```javascript
/**
 * 获取用户数据
 * @param {number} userId - 用户ID
 * @returns {Promise<Object>} 用户数据
 */
async function getUserData(userId) {
  // 从 API 获取用户信息
  const response = await fetch(`/api/users/${userId}`);
  return response.json();
}
```

## 2. 代码结构

### 2.1 导入顺序
1. 内置模块
2. 第三方模块
3. 本地模块
4. 样式文件

**示例：**
```javascript
// 内置模块
const fs = require('fs');

// 第三方模块
import React from 'react';
import axios from 'axios';

// 本地模块
import UserService from './services/userService';
import { formatDate } from './utils/date';

// 样式文件
import './styles/App.css';
```

### 2.2 函数结构
- 函数长度控制在 50 行以内
- 单个函数只做一件事
- 避免嵌套层级过深（不超过 4 层）
- 使用早期返回（early return）模式

**示例：**
```javascript
// 推荐
function processUserData(user) {
  if (!user) {
    return null;
  }
  
  if (!user.isActive) {
    return { ...user, status: 'inactive' };
  }
  
  return { ...user, status: 'active' };
}

// 不推荐
function processUserData(user) {
  if (user) {
    if (user.isActive) {
      return { ...user, status: 'active' };
    } else {
      return { ...user, status: 'inactive' };
    }
  } else {
    return null;
  }
}
```

## 3. 最佳实践

### 3.1 错误处理
- 使用 try-catch 捕获异常
- 提供有意义的错误信息
- 避免使用 console.log 进行错误处理
- 考虑使用统一的错误处理中间件

**示例：**
```javascript
// 推荐
try {
  const result = await fetchData();
  return result;
} catch (error) {
  console.error('获取数据失败:', error);
  throw new Error('数据获取失败，请稍后重试');
}

// 不推荐
const result = fetchData();
if (result.error) {
  console.log('错误:', result.error);
}
```

### 3.2 性能优化
- 使用箭头函数和 const/let
- 避免不必要的计算和重复渲染
- 使用 memoization 缓存计算结果
- 合理使用 async/await

**示例：**
```javascript
// 推荐
const calculateTotal = useMemo(() => {
  return items.reduce((sum, item) => sum + item.price, 0);
}, [items]);

// 不推荐
function calculateTotal() {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// 每次渲染都会重新计算
const total = calculateTotal();
```

### 3.3 代码可读性
- 使用描述性变量名
- 避免魔法数字和字符串
- 分解复杂逻辑为多个函数
- 使用空行分隔不同逻辑块

**示例：**
```javascript
// 推荐
const MAX_RETRY_COUNT = 3;
const API_TIMEOUT = 5000;

function fetchWithRetry(url, retries = MAX_RETRY_COUNT) {
  // 实现逻辑
}

// 不推荐
function fetchWithRetry(url, retries = 3) {
  // 实现逻辑
}
```

## 4. 版本控制

### 4.1 Git 规范
- 提交信息使用语义化提交格式
- 分支命名遵循 `feature/xxx`、`bugfix/xxx` 格式
- 代码提交前运行 lint 和测试
- 避免提交敏感信息和大文件

**示例：**
```bash
# 推荐
git commit -m "feat: 添加用户登录功能"
git commit -m "fix: 修复表单验证问题"

# 不推荐
git commit -m "修改代码"
git commit -m "fix bug"
```

### 4.2 代码审查
- 每次提交都需要代码审查
- 审查重点包括：代码质量、安全性、性能
- 提出具体的改进建议
- 确保代码符合团队规范

## 5. 文档

### 5.1 项目文档
- 提供 README.md 文件
- 说明项目结构和技术栈
- 提供安装和运行指南
- 记录重要的设计决策

### 5.2 API 文档
- 为每个 API 端点提供文档
- 说明请求参数和返回值
- 提供示例请求和响应
- 记录错误处理方式

## 6. 工具和配置

### 6.1 开发工具
- 使用 VS Code 作为主要编辑器
- 安装推荐的插件
- 配置编辑器格式化规则
- 使用 ESLint 和 Prettier 保持代码风格一致

### 6.2 配置文件
- 统一配置文件格式
- 版本控制配置文件
- 提供默认配置和环境变量说明
- 避免硬编码配置值

## 7. 团队协作

### 7.1 沟通
- 使用统一的沟通工具
- 及时更新项目状态
- 遇到问题及时沟通
- 分享学习资源和最佳实践

### 7.2 代码所有权
- 明确代码责任人和维护者
- 定期代码重构和优化
- 建立代码审查流程
- 鼓励团队成员参与代码改进

## 8. 持续集成

### 8.1 CI/CD 配置
- 配置自动化构建和测试
- 集成代码质量检查
- 自动化部署流程
- 监控构建和部署状态

### 8.2 测试策略
- 编写单元测试和集成测试
- 设定测试覆盖率目标
- 定期运行测试套件
- 确保测试环境与生产环境一致

## 9. 总结

团队编码规范的目的是提高代码质量，减少错误，提高开发效率，促进团队协作。所有团队成员都应该遵守这些规范，并在实践中不断完善和改进。