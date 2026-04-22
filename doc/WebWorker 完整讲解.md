# WebWorker 完整讲解

## 1. WebWorker 是什么？

**定义**：
WebWorker 是 **HTML5 提供的浏览器后台线程技术**，允许 JavaScript 在**主线程之外**创建独立的后台线程，执行耗时计算、数据处理等任务，**不阻塞页面渲染和用户交互**。

核心作用：**解决 JS 单线程阻塞页面卡顿的问题**。

---

## 2. 优缺点（表格）

| 优点                            | 缺点                                             |
| ------------------------------- | ------------------------------------------------ |
| 不阻塞 UI，页面流畅不卡顿       | 不能直接操作 DOM（document、window、元素都不行） |
| 充分利用 CPU 多核，提升计算性能 | 线程间通信需要数据拷贝（大数据会有性能开销）     |
| 适合大量数据处理、复杂计算      | 有内存限制，不能无限创建 Worker                  |
| 原生支持，无需第三方库          | 不支持 localStorage、cookie 等主线程 API         |
| 兼容所有现代浏览器              | 部分低版本 IE 不支持（IE10+）                    |

---

## 3. 业务场景（表格）

| 场景分类      | 具体业务使用场景                                     |
| ------------- | ---------------------------------------------------- |
| 大数据处理    | Excel/CSV 大量数据解析、表格导出、百万条数据筛选排序 |
| 加密计算      | 前端 AES/RSA 加密、密码哈希、文件加密                |
| 图像/视频处理 | 图片压缩、滤镜处理、Canvas 像素计算                  |
| 实时计算      | 股票行情计算、游戏物理引擎、图表大数据渲染           |
| 定时任务      | 后台轮询、日志上报、定时数据同步                     |
| 复杂算法      | 递归计算、数学公式运算、机器学习模型推理             |

---

## 4. 代码示例（可直接运行）

### 主线程代码（页面中）

```javascript
// 1. 创建 WebWorker
const worker = new Worker('worker.js');

// 2. 向 Worker 发送数据
worker.postMessage({ type: 'calculate', data: 1000000000 });

// 3. 接收 Worker 返回的结果
worker.onmessage = (e) => {
  console.log('计算结果：', e.data);
};

// 4. 监听错误
worker.onerror = (error) => {
  console.log(`Worker 错误：${error.message}`);
};
```

### 后台线程代码（新建文件 worker.js）

```javascript
// 监听主线程消息
self.onmessage = (e) => {
  if (e.data.type === 'calculate') {
    let sum = 0;
    // 模拟超大计算量（会阻塞主线程，但 Worker 中不影响）
    for (let i = 0; i < e.data.data; i++) {
      sum += i;
    }
    // 把结果发回主线程
    self.postMessage(sum);
  }
};
```

---

## 5. 支持的编程语言

WebWorker 本质是**浏览器标准 API**，支持所有**能运行在浏览器中的编程语言**：

| 语言            | 支持情况        | 说明                                    |
| --------------- | --------------- | --------------------------------------- |
| JavaScript      | ✅ 完全原生支持 | 最常用、默认支持                        |
| TypeScript      | ✅ 完全支持     | 需配置 worker 类型，编译为 JS 运行      |
| WebAssembly     | ✅ 完全支持     | C/C++/Rust 编译成 WASM 可在 Worker 运行 |
| Python(Pyodide) | ✅ 支持         | 前端 Python 解释器可跑在 Worker         |
| Dart            | ✅ 支持         | Flutter Web 可用 WebWorker              |
| CoffeeScript    | ✅ 支持         | 编译为 JS 即可使用                      |

---

### 总结

1. **WebWorker = 浏览器后台线程**，让 JS 可以多线程运行
2. **优点**：不卡页面、利用多核；**缺点**：不能操作 DOM、通信有拷贝开销
3. **最常用场景**：大数据处理、文件解析、加密、图片视频处理
4. **支持语言**：JS/TS/WASM 为主，所有浏览器端语言都能用
