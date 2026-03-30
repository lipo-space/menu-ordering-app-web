# 🎯 单项目部署配置完成！

## ✅ 已完成

我已经配置好前后端在同一个 Vercel 项目中部署：
- **前端**: Vue 3 应用 → `https://menu-ordering-app-web.vercel.app`
- **后端**: FastAPI 应用 → `https://menu-ordering-app-web.vercel.app/api/v1/*`

## 📋 你需要做的（2分钟）

### 1. 在 Vercel 添加环境变量

访问你的 Vercel 项目：**Settings → Environment Variables**

添加以下环境变量：

```
SUPABASE_URL=https://osxdtxgikmsiaaqecabu.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9zeGR0eGdpa21zaWFhcWVjYWJ1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ4NjE5NjMsImV4cCI6MjA5MDQzNzk2M30.hllkw1JiouU3Z5U36LvqA0prYJrPFPiYIbTTZEpMrUc
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9zeGR0eGdpa21zaWFhcWVjYWJ1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NDg2MTk2MywiZXhwIjoyMDkwNDM3OTYzfQ.eZGSADSVQWYM7t43J9KsxfrElmDJ9DB8MOqHjTUXDPw
ALLOWED_ORIGINS=http://localhost:5173,https://menu-ordering-app-web.vercel.app,https://*.vercel.app
ENVIRONMENT=production

VITE_API_BASE_URL=/api/v1
VITE_SUPABASE_URL=https://osxdtxgikmsiaaqecabu.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9zeGR0eGdpa21zaWFhcWVjYWJ1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ4NjE5NjMsImV4cCI6MjA5MDQzNzk2M30.hllkw1JiouU3Z5U36LvqA0prYJrPFPiYIbTTZEpMrUc
```

**注意**：`VITE_API_BASE_URL` 应该是 `/api/v1`（相对路径），不是完整 URL！

### 2. 重新部署

1. 在 Vercel Dashboard → **Deployments**
2. 找到最新的部署（正在构建中）
3. 等待完成（大约 2-3 分钟）

或者手动触发：
- 点击最新部署的 **⋯** 菜单
- 选择 **Redeploy**

## ✅ 验证部署

部署完成后测试：

### 1. 测试前端
访问：`https://menu-ordering-app-web.vercel.app`

### 2. 测试 API 根路径
访问：`https://menu-ordering-app-web.vercel.app/api`

应该看到：
```json
{
  "message": "家庭点菜系统 API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### 3. 测试菜品 API
访问：`https://menu-ordering-app-web.vercel.app/api/v1/dishes`

应该返回菜品列表（JSON 格式）

### 4. 测试前端功能
- 点击菜品页面
- 应该能看到菜品列表
- 尝试添加、编辑、删除菜品

## 🎉 完成！

现在你的应用：
- ✅ 前后端在同一个域名下
- ✅ 共享同一个 Vercel 项目
- ✅ API 路径：`/api/v1/*`
- ✅ 前端路径：`/*`
- ✅ 每次 push 自动部署

## 🐛 如果还有问题

打开浏览器开发者工具（F12）：

1. **Console 标签** - 查看错误信息
2. **Network 标签** - 检查 API 请求状态

告诉我具体的错误信息，我会立即帮你解决！

## 📊 项目架构

```
GitHub Repository (menu-ordering-app-web)
├── api/                    ← Vercel Serverless Function
│   ├── index.py           ← FastAPI 入口
│   └── requirements.txt   ← Python 依赖
├── backend/               ← 后端代码（共享）
│   ├── src/
│   └── requirements.txt
├── frontend/              ← 前端代码
│   ├── src/
│   └── package.json
└── vercel.json            ← Vercel 配置（前后端）
```

部署成功后告诉我！🚀
