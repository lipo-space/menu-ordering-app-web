# 部署替代方案

如果 Vercel 部署后端 API 遇到问题，建议采用以下更稳定的方案：

## 🎯 推荐方案：前后端分离部署

### 方案 A: 前端 Vercel + 后端 Railway（最简单）

#### 1. 部署后端到 Railway

```bash
# 安装 Railway CLI
npm install -g @railway/cli

# 登录
railway login

# 初始化项目
railway init

# 部署
railway up
```

在 Railway Dashboard 添加环境变量：
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_KEY`

#### 2. 更新前端配置

修改 `frontend/.env.production`:
```bash
VITE_API_BASE_URL=https://your-app.railway.app/api/v1
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

#### 3. 部署前端到 Vercel

使用简化的 `vercel.json`（仅前端）:
```json
{
  "version": 2,
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "framework": "vue"
}
```

### 方案 B: 前端 Vercel + 后端 Render

#### 1. 部署后端到 Render

1. 访问 https://render.com
2. 创建新的 Web Service
3. 连接 GitHub 仓库
4. 配置：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`

#### 2. 添加环境变量

在 Render Dashboard 添加所有 Supabase 环境变量。

#### 3. 更新前端并部署到 Vercel

同方案 A。

### 方案 C: 全栈部署到 Render

Render 支持 Python + 静态站点，可以一个平台搞定：

1. **后端**: 创建 Web Service（同方案 B）
2. **前端**: 创建 Static Site
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`

## 📊 方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| Vercel 全栈 | 一个平台管理 | Python 支持有限 | ⭐⭐⭐ |
| Vercel + Railway | 部署简单，性能好 | 两个平台 | ⭐⭐⭐⭐⭐ |
| Vercel + Render | 免费额度多 | 两个平台 | ⭐⭐⭐⭐ |
| Render 全栈 | 一个平台 | 配置稍复杂 | ⭐⭐⭐⭐ |

## 🚀 快速决策

- **最简单**: 方案 A（Vercel + Railway）
- **最省钱**: 方案 C（Render 全栈）
- **最稳定**: 方案 A 或 B

## 📝 当前状态

你的代码已经配置好了 Vercel 部署，但后端 API 可能需要调试。

建议：
1. **先尝试当前的 Vercel 配置**
2. 如果失败，**切换到方案 A**（5分钟搞定）

需要帮助切换到其他方案？告诉我，我可以帮你配置！
