# Vercel 环境变量配置

## 🔧 必须配置的环境变量

在 Vercel Dashboard 中添加以下环境变量：

### 1. 访问项目设置
1. 打开 https://vercel.com/dashboard
2. 选择你的项目：`menu-ordering-app-web`
3. 点击 **Settings** → **Environment Variables**

### 2. 添加以下变量

| 变量名 | 值 | 环境 |
|--------|-----|------|
| `SUPABASE_URL` | 你的 Supabase 项目 URL | Production, Preview, Development |
| `SUPABASE_ANON_KEY` | 你的 Supabase anon key | Production, Preview, Development |
| `SUPABASE_SERVICE_KEY` | 你的 Supabase service role key | Production, Preview, Development |
| `VITE_SUPABASE_URL` | 你的 Supabase 项目 URL | Production, Preview, Development |
| `VITE_SUPABASE_ANON_KEY` | 你的 Supabase anon key | Production, Preview, Development |

### 3. 获取 Supabase 凭证

1. 访问 https://supabase.com/dashboard
2. 选择你的项目
3. 点击 **Settings** → **API**
4. 复制以下值：
   - **Project URL** → `SUPABASE_URL` 和 `VITE_SUPABASE_URL`
   - **anon public** key → `SUPABASE_ANON_KEY` 和 `VITE_SUPABASE_ANON_KEY`
   - **service_role** key → `SUPABASE_SERVICE_KEY`

### 4. 重新部署

添加环境变量后，需要重新部署：
1. 在 Vercel Dashboard 中
2. 点击 **Deployments**
3. 找到最新的部署
4. 点击右侧的 **⋯** 菜单
5. 选择 **Redeploy**

或者推送一个新的 commit 自动触发部署。

## ✅ 验证配置

部署完成后，测试以下端点：

### API 健康检查
访问：`https://menu-ordering-app-web.vercel.app/api`

应该看到：
```json
{
  "message": "家庭点菜系统 API",
  "version": "1.0.0",
  "docs": "/docs",
  "status": "running"
}
```

### API 文档
访问：`https://menu-ordering-app-web.vercel.app/docs`

应该看到 FastAPI 自动生成的 API 文档。

### 前端应用
访问：`https://menu-ordering-app-web.vercel.app`

应该能正常加载前端页面，并且可以：
- 查看菜品列表
- 创建新菜品
- 数据保存到 Supabase

## 🐛 常见问题

### 问题 1: 307 重定向
**症状**: API 请求返回 307 错误
**解决**: 已在代码中修复（`redirect_slashes=False`）

### 问题 2: CORS 错误
**症状**: 浏览器控制台显示 CORS 错误
**解决**: 确保在 Vercel 添加了所有环境变量，并重新部署

### 问题 3: 500 内部错误
**症状**: API 返回 500 错误
**排查**:
1. 在 Vercel Dashboard → Deployments → Functions 标签查看日志
2. 检查环境变量是否正确设置
3. 确认 Supabase 连接正常

### 问题 4: 前端无法连接后端
**症状**: 页面加载但无法获取数据
**解决**:
- 检查浏览器控制台的网络请求
- 确认 API URL 是相对路径 `/api/v1`
- 检查 Vercel 的 rewrite 配置

## 📝 本地开发

本地开发时，创建 `frontend/.env` 和 `backend/.env`：

### frontend/.env
```bash
VITE_API_BASE_URL=http://localhost:8002/api/v1
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### backend/.env
```bash
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

## 🎉 完成！

配置完成后，你的应用将：
- ✅ 前端和后端在同一个域名下运行
- ✅ API 请求通过 `/api/v1/*` 路径
- ✅ 数据持久化到 Supabase
- ✅ 自动部署（每次 push 到 master）

享受你的全栈应用！🚀
