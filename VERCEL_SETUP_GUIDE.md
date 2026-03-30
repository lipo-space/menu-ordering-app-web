# Vercel 自动部署设置指南

## 🚨 问题诊断

你已经将代码上传到 GitHub，但 Vercel 没有自动部署。这是因为：
1. **还没有在 Vercel 上连接 GitHub 仓库**
2. **需要配置正确的构建设置**

## 📝 完整设置步骤

### 步骤 1: 登录 Vercel 并导入项目

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 **"Add New..."** → **"Project"**
3. 在 **"Import Git Repository"** 部分：
   - 如果是第一次使用，点击 **"Connect to GitHub"**
   - 授权 Vercel 访问你的 GitHub 仓库
   - 找到 `lipo-space/menu-ordering-app-web` 仓库
   - 点击 **"Import"**

### 步骤 2: 配置项目设置

在 **"Configure Project"** 页面：

#### Framework Preset
- 选择 **"Vite"**（用于 Vue 3）

#### Root Directory
- 点击 **"Edit"**
- 设置为 **"."** （根目录）

#### Build and Output Settings

**Build Command:**
```bash
cd frontend && npm install && npm run build
```

**Output Directory:**
```
frontend/dist
```

**Install Command:**
```bash
cd frontend && npm install
```

#### Environment Variables

点击 **"Environment Variables"** 展开，添加以下变量：

| Name | Value |
|------|-------|
| `SUPABASE_URL` | 你的 Supabase 项目 URL |
| `SUPABASE_ANON_KEY` | 你的 Supabase anon key |
| `SUPABASE_SERVICE_KEY` | 你的 Supabase service role key |
| `VITE_API_BASE_URL` | `/api/v1` |
| `VITE_SUPABASE_URL` | 你的 Supabase 项目 URL |
| `VITE_SUPABASE_ANON_KEY` | 你的 Supabase anon key |

### 步骤 3: 部署

1. 点击 **"Deploy"** 按钮
2. 等待构建完成（大约 2-3 分钟）
3. 部署成功后，你会得到一个 URL（例如：`https://menu-ordering-app-web.vercel.app`）

### 步骤 4: 验证自动部署

1. 在 Vercel Dashboard 中，进入你的项目
2. 点击 **"Settings"** → **"Git"**
3. 确认 **"Production Branch"** 设置为 `master`
4. 在 **"Ignored Build Step"** 确保没有设置任何忽略规则

现在，每次你 `git push` 到 `master` 分支，Vercel 会自动部署！

## 🔧 后端 API 部署（重要！）

当前配置只部署了前端。对于后端 API，你有两个选择：

### 选项 A: 使用 Vercel Serverless Functions（推荐）

1. 创建 `api` 目录在项目根目录（我已经创建了 `api/index.py`）
2. 更新 `vercel.json` 配置（见下方）

### 选项 B: 使用独立的 Python 托管平台

将后端部署到：
- **Railway** (https://railway.app)
- **Render** (https://render.com)
- **Fly.io** (https://fly.io)

然后在前端更新 `VITE_API_BASE_URL` 指向后端 URL。

## 📋 更新后的 vercel.json 配置

```json
{
  "version": 2,
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "framework": "vue",
  "functions": {
    "api/**/*.py": {
      "runtime": "python3.11"
    }
  },
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/api/$1"
    }
  ]
}
```

## 🧪 测试部署

部署完成后，测试以下功能：

### 1. 前端访问
- 访问你的 Vercel URL
- 确认页面能正常加载
- 打开浏览器控制台，检查是否有错误

### 2. API 连接
- 访问 `https://your-app.vercel.app/api/`
- 应该看到 FastAPI 的欢迎信息
- 访问 `https://your-app.vercel.app/api/docs`
- 应该看到 API 文档

### 3. 数据库连接
- 尝试创建一个菜品
- 刷新页面，确认数据保存成功
- 检查 Supabase Dashboard 确认数据已存储

## ⚠️ 常见问题

### 问题 1: 构建失败 - "Command not found"

**解决方案:**
```bash
# 确保 frontend/package.json 中的 scripts 正确
npm run build  # 应该能成功
```

### 问题 2: 页面加载但 API 无法访问

**解决方案:**
- 检查 `vercel.json` 中的 `rewrites` 配置
- 确认后端函数正确部署
- 查看 Vercel 的 Functions 日志

### 问题 3: 环境变量未生效

**解决方案:**
1. 在 Vercel Dashboard → Settings → Environment Variables
2. 确认所有变量都已添加
3. 重新部署项目（Settings → Deployments → Redeploy）

### 问题 4: CORS 错误

**解决方案:**
更新 `backend/src/config.py` 中的 `ALLOWED_ORIGINS`：
```python
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://your-app.vercel.app",  # 添加你的 Vercel URL
    "https://*.vercel.app"  # 或者允许所有 Vercel 预览 URL
]
```

## 🎯 下一步

1. **设置自定义域名**（可选）
   - Vercel Dashboard → Settings → Domains
   - 添加你的域名

2. **配置预览部署**
   - 每次 Pull Request 都会自动创建预览 URL
   - 团队成员可以在合并前测试变更

3. **监控和日志**
   - Vercel Dashboard → Deployments
   - 查看每次部署的日志
   - 监控函数执行情况

## ✅ 完成检查清单

- [ ] 在 Vercel 导入 GitHub 仓库
- [ ] 配置正确的构建命令和输出目录
- [ ] 添加所有必需的环境变量
- [ ] 首次部署成功
- [ ] 测试前端页面加载
- [ ] 测试 API 连接
- [ ] 测试数据库操作
- [ ] 确认 `git push` 触发自动部署

## 🎉 成功！

完成以上步骤后，你的项目将实现：
- ✅ 自动部署：每次 push 到 master 都会自动部署
- ✅ 预览部署：每个 PR 都有独立的预览 URL
- ✅ 零停机部署：Vercel 会自动处理流量切换
- ✅ 全球 CDN：静态资源自动分发到全球边缘节点

有问题随时查看 Vercel 的构建日志和函数日志进行调试！
