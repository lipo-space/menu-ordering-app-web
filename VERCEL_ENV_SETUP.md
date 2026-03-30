# 🎯 Vercel 环境变量配置（重要！）

## 问题症状

线上环境前端请求 `http://localhost:8002/api/v1/dishes`，导致 CORS 错误。

## 原因

Vercel 没有设置 `VITE_API_BASE_URL` 环境变量，前端使用了默认值（本地地址）。

## 🔧 立即修复（2 分钟）

### 步骤 1: 访问 Vercel Dashboard

1. 打开 https://vercel.com/dashboard
2. 选择你的项目：`menu-ordering-app-web`
3. 点击 **Settings** 标签
4. 点击左侧的 **Environment Variables**

### 步骤 2: 添加/更新环境变量

**关键变量**：

| 变量名 | 值 | 环境 |
|--------|-----|------|
| **`VITE_API_BASE_URL`** | **`/api/v1`** | ✅ Production<br>✅ Preview<br>✅ Development |

**重要**: 值必须是 `/api/v1`（相对路径），**不是** `https://...` 完整 URL！

**其他必需变量**：

```
SUPABASE_URL=https://osxdtxgikmsiaaqecabu.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9zeGR0eGdpa21zaWFhcWVjYWJ1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ4NjE5NjMsImV4cCI6MjA5MDQzNzk2M30.hllkw1JiouU3Z5U36LvqA0prYJrPFPiYIbTTZEpMrUc
SUPABASE_SERVICE_KEY=[你的 service_role key]
ALLOWED_ORIGINS=http://localhost:5173,https://menu-ordering-app-web.vercel.app,https://*.vercel.app
ENVIRONMENT=production

VITE_SUPABASE_URL=https://osxdtxgikmsiaaqecabu.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9zeGR0eGdpa21zaWFhcWVjYWJ1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ4NjE5NjMsImV4cCI6MjA5MDQzNzk2M30.hllkw1JiouU3Z5U36LvqA0prYJrPFPiYIbTTZEpMrUc
```

### 步骤 3: 重新部署

**方法 A: 触发新的部署（推荐）**

1. 点击 **Deployments** 标签
2. 找到最新的部署
3. 点击右侧的 **⋯** 菜单
4. 选择 **Redeploy**
5. 点击 **Redeploy** 确认

**方法 B: Push 一个空提交**

```bash
git commit --allow-empty -m "chore: trigger redeploy with env vars"
git push origin master
```

### 步骤 4: 等待部署完成

等待 2-3 分钟，部署完成后测试。

## ✅ 验证修复

### 1. 测试 API

访问：`https://menu-ordering-app-web.vercel.app/api/v1/dishes`

**期望结果**：返回 JSON 格式的菜品列表（状态码 200）

### 2. 测试前端

访问：`https://menu-ordering-app-web.vercel.app`

1. 打开浏览器开发者工具（F12）
2. 切换到 **Network** 标签
3. 点击菜品页面
4. 查看请求：
   - ✅ 应该看到：`/api/v1/dishes?limit=50&offset=0`（相对路径）
   - ❌ 不应该看到：`http://localhost:8002/...`

### 3. 检查 CORS

- ✅ 不应该有 CORS 错误
- ✅ 应该能看到菜品列表

## 🐛 如果还有问题

### 检查环境变量是否生效

在浏览器控制台运行：

```javascript
console.log(import.meta.env.VITE_API_BASE_URL)
```

**期望输出**: `/api/v1`

如果输出 `undefined` 或 `http://localhost:8002/...`，说明环境变量没生效，需要 Redeploy。

### 查看 Vercel 构建日志

1. Vercel Dashboard → Deployments
2. 点击最新的部署
3. 查看 **Building** 日志
4. 搜索 `VITE_` 确认环境变量是否被注入

### 清除缓存重新部署

1. Settings → General
2. 找到 **Build & Development Settings**
3. 勾选 **Override** for Build Command
4. 添加：`cd frontend && npm install && npm run build`
5. Redeploy

## 📊 架构说明

```
Vercel 部署架构：
┌─────────────────────────────────────────┐
│  https://menu-ordering-app-web.vercel.app
│                                          │
│  ├── /                  → 前端 (Vue 3)   │
│  ├── /dishes            → 前端路由        │
│  └── /api/v1/*          → 后端 (FastAPI) │
│      ├── /api/v1/dishes                  │
│      ├── /api/v1/menus                   │
│      └── /api/v1/combinations            │
└─────────────────────────────────────────┘

前端配置：
- VITE_API_BASE_URL=/api/v1  ← 相对路径！

后端配置：
- SUPABASE_URL=...
- ALLOWED_ORIGINS=...vercel.app
```

## 🎉 完成！

配置完成后，你的应用：
- ✅ 前后端在同一个域名
- ✅ 无 CORS 错误
- ✅ API 请求使用相对路径
- ✅ 自动部署

## 🆘 需要帮助？

如果配置后还有问题，提供：
1. 浏览器控制台的完整错误信息
2. Network 标签中失败请求的详情
3. Vercel 构建日志的截图

我会立即帮你解决！
