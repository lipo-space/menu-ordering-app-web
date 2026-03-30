# Vercel 后端部署指南

## 📋 部署步骤

### 1. 创建新的 Vercel 项目（后端）

1. 访问 https://vercel.com/dashboard
2. 点击 **"Add New..."** → **"Project"**
3. 选择 GitHub 仓库：`lipo-space/menu-ordering-app-web`
4. **重要配置**：
   - **Project Name**: `menu-ordering-app-backend`（或其他名称）
   - **Root Directory**: 点击 "Edit"，设置为 `backend`
   - **Framework Preset**: 选择 "Other"

### 2. 环境变量配置

在项目设置中添加以下环境变量：

```
SUPABASE_URL=https://osxdtxgikmsiaaqecabu.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9zeGR0eGdpa21zaWFhcWVjYWJ1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ4NjE5NjMsImV4cCI6MjA5MDQzNzk2M30.hllkw1JiouU3Z5U36LvqA0prYJrPFPiYIbTTZEpMrUc
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9zeGR0eGdpa21zaWFhcWVjYWJ1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NDg2MTk2MywiZXhwIjoyMDkwNDM3OTYzfQ.eZGSADSVQWYM7t43J9KsxfrElmDJ9DB8MOqHjTUXDPw
ALLOWED_ORIGINS=http://localhost:5173,https://menu-ordering-app-web.vercel.app,https://*.vercel.app
ENVIRONMENT=production
```

### 3. 部署

点击 **"Deploy"** 按钮。

### 4. 获取后端 URL

部署成功后，你会得到一个 URL，例如：
```
https://menu-ordering-app-backend.vercel.app
```

测试 API：
- 根路径: `https://menu-ordering-app-backend.vercel.app/`
- 菜品列表: `https://menu-ordering-app-backend.vercel.app/api/v1/dishes`

### 5. 更新前端配置

在前端项目（menu-ordering-app-web）的 Vercel 设置中：

**Settings → Environment Variables**

添加或更新：
```
VITE_API_BASE_URL = https://menu-ordering-app-backend.vercel.app/api/v1
```

然后重新部署前端。

## ✅ 验证

1. 访问前端: `https://menu-ordering-app-web.vercel.app`
2. 点击菜品页面
3. 应该能看到菜品列表（不再是空白）

## 🐛 常见问题

### 问题 1: 500 错误 - Supabase 版本冲突

**解决方案**: 我已经降级到 `supabase==2.0.0`，这个版本与 Vercel 兼容。

如果还有问题，检查 Vercel 的函数日志。

### 问题 2: CORS 错误

**解决方案**: 确保 `ALLOWED_ORIGINS` 包含你的前端 URL：
```
ALLOWED_ORIGINS=http://localhost:5173,https://menu-ordering-app-web.vercel.app,https://*.vercel.app
```

### 问题 3: 404 Not Found

**解决方案**:
- 确认 Root Directory 设置为 `backend`
- 确认访问的 URL 路径正确（`/api/v1/dishes`）

## 📊 项目架构

```
GitHub Repository (menu-ordering-app-web)
├── backend/          ← 后端 Vercel 项目
│   ├── main.py
│   ├── api_index.py  (Vercel 入口)
│   ├── vercel.json
│   └── requirements.txt
└── frontend/         ← 前端 Vercel 项目
    ├── src/
    ├── package.json
    └── vercel.json
```

两个独立的 Vercel 项目，共享同一个 GitHub 仓库。

## 🎉 完成！

现在你有：
- ✅ 前端: `https://menu-ordering-app-web.vercel.app`
- ✅ 后端: `https://menu-ordering-app-backend.vercel.app`
- ✅ 数据库: Supabase

每次 push 到 GitHub，两个项目都会自动部署！
