# 🚂 Railway 后端部署指南（3分钟完成）

## 为什么选择 Railway？

- ✅ 原生 Python 支持（没有 Vercel 的兼容性问题）
- ✅ 自动从 GitHub 部署
- ✅ 免费额度充足（$5/月免费）
- ✅ 零配置部署
- ✅ 比 Vercel Python 更稳定

## 快速部署步骤

### 1. 访问 Railway

```bash
# 打开浏览器访问
https://railway.app
```

### 2. 使用 GitHub 登录

点击 **"Start a New Project"** → **"Deploy from GitHub repo"**

### 3. 选择你的仓库

找到并选择：`lipo-space/menu-ordering-app-web`

### 4. 配置项目

Railway 会自动检测到 Python 项目。设置：

**Root Directory**: `backend`

**或者手动配置：**
1. 点击 **"Settings"**
2. **Root Directory** → 设置为 `backend`
3. **Start Command** → `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 5. 添加环境变量

在 Railway 项目中，点击 **"Variables"** 标签，添加：

```
SUPABASE_URL=你的_Supabase_URL
SUPABASE_ANON_KEY=你的_Supabase_anon_key
SUPABASE_SERVICE_KEY=你的_Supabase_service_key
ALLOWED_ORIGINS=https://menu-ordering-app-web.vercel.app,http://localhost:5173
ENVIRONMENT=production
```

### 6. 部署

点击 **"Deploy"** 按钮，等待 1-2 分钟。

### 7. 获取 URL

部署完成后：
1. 点击 **"Settings"**
2. 找到 **"Domains"**
3. 点击 **"Generate Domain"**
4. 你会得到一个 URL，如：`https://menu-ordering-app-web-production.up.railway.app`

## 更新前端配置

### 1. 在 Vercel 添加环境变量

访问你的 Vercel 项目 → Settings → Environment Variables

更新：
```
VITE_API_BASE_URL = https://你的railway地址.up.railway.app/api/v1
```

### 2. 触发重新部署

在 Vercel Dashboard → Deployments → 点击最新部署的 ⋯ 菜单 → Redeploy

## ✅ 验证部署

### 测试后端（Railway）
访问：`https://你的railway地址.up.railway.app/`

应该看到：
```json
{
  "message": "家庭点菜系统 API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### 测试 API（Railway）
访问：`https://你的railway地址.up.railway.app/api/v1/dishes`

应该返回菜品列表（状态码 200）

### 测试前端（Vercel）
访问：`https://menu-ordering-app-web.vercel.app`

应该能正常使用，数据保存到 Supabase！

## 🎉 完成！

现在你有：
- **前端**: `https://menu-ordering-app-web.vercel.app` (Vercel)
- **后端**: `https://xxx.up.railway.app` (Railway)
- **数据库**: Supabase

每次 push 到 GitHub，两个平台都会自动部署！

## 🔧 故障排查

### 问题 1: Railway 部署失败
- 检查 Root Directory 是否设置为 `backend`
- 查看 Railway 的构建日志
- 确认所有环境变量都已添加

### 问题 2: CORS 错误
在 Railway 的 Variables 中添加：
```
ALLOWED_ORIGINS=https://menu-ordering-app-web.vercel.app,https://*.vercel.app
```

### 问题 3: 前端无法连接后端
- 确认 `VITE_API_BASE_URL` 是完整的 Railway URL
- 确认 URL 以 `/api/v1` 结尾
- 检查浏览器控制台的网络请求

## 📊 成本

- **Railway**: $5/月免费额度（足够开发和测试）
- **Vercel**: 免费
- **Supabase**: 免费套餐（500MB 数据库）

总计：**$0/月** 🎉

## 🆘 需要帮助？

如果遇到问题，告诉我：
1. Railway 部署日志的错误信息
2. 我会立即帮你解决！

开始部署吧！只需要 3 分钟！🚀
