# SSR与SSG架构对比及Next.js实战应用

## 核心概念解析

### SSG（静态站点生成）
- **核心特点**：构建时一次性生成静态HTML文件
- **访问流程**：用户请求 → CDN直接返回静态文件
- **类比**：提前做好饭菜，客人来了直接上桌

### SSR（服务端渲染）
- **核心特点**：用户每次访问时实时渲染页面
- **访问流程**：用户请求 → 服务器实时获取数据渲染 → 返回HTML
- **类比**：客人点餐后现做，保证新鲜度

## 对比分析

| 维度 | SSR | SSG |
|------|-----|-----|
| 渲染时机 | 访问时（runtime） | 构建时（build time） |
| 首屏速度 | 较快 | 极快（CDN分发） |
| SEO友好度 | 优秀 | 优秀 |
| 数据实时性 | 极高 | 极低（需重新构建） |
| 服务器压力 | 较高 | 极低 |
| 部署成本 | 较高 | 极低 |
| 开发复杂度 | 中等 | 较低 |

## 适用场景

### SSG适用场景（优先选择）
- 企业官网、品牌营销页
- 技术文档站
- 个人博客、作品集
- 活动页、Landing页

### SSR适用场景（需实时数据）
- 电商站点（商品详情、订单页）
- 后台管理系统
- 用户中心
- 高频更新资讯站

### 混合场景（Next.js特色）
同一项目中不同页面可使用不同渲染模式，如官网用SSG，用户中心用SSR。

## Next.js实战用法

### SSG实现
**核心函数**：`getStaticProps`（构建时执行）

```jsx
// pages/blog.js
export default function Blog({ posts }) {
  return (
    <div>
      <h1>博客列表</h1>
      {posts.map(post => (
        <div key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.content}</p>
        </div>
      ))}
    </div>
  );
}

export async function getStaticProps() {
  const res = await fetch('https://api.example.com/posts');
  const posts = await res.json();
  return {
    props: { posts },
    revalidate: 60, // 增量静态再生
  };
}
```

**动态路由**：搭配 `getStaticPaths`

### SSR实现
**核心函数**：`getServerSideProps`（每次访问执行）

```jsx
// pages/user-center.js
export default function UserCenter({ userInfo }) {
  return (
    <div>
      <h1>个人中心</h1>
      <img src={userInfo.avatar} alt="头像" />
      <p>昵称：{userInfo.nickname}</p>
    </div>
  );
}

export async function getServerSideProps(context) {
  const { cookie } = context.req;
  const res = await fetch('https://api.example.com/user/info', {
    headers: { cookie },
  });
  const userInfo = await res.json();
  return {
    props: { userInfo },
  };
}
```

## 面试记忆点
- `getStaticProps` (+ `getStaticPaths`) → SSG
- `getServerSideProps` → SSR
- 无数据获取函数 → 纯静态页面（SSG）

## 总结
选择渲染模式的核心依据：
- **SSG**：内容更新少，追求性能和低成本
- **SSR**：需要实时数据，动态内容

Next.js的优势在于可根据不同页面需求灵活选择渲染模式，平衡性能与实时性。
