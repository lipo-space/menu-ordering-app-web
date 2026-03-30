# 🚀 快速部署指南（5 分钟）

## 问题：代码已上传 GitHub，但 Vercel 没有自动部署

### 原因
你需要在 Vercel 上**手动连接** GitHub 仓库并配置构建设置。

### 立即解决

#### 1. 访问 Vercel Dashboard
https://vercel.com/dashboard

#### 2. 导入 GitHub 仓库
1. 点击 **"Add New Project"**
2. 选择 **"Import Git Repository"**
3. 找到 `lipo-space/menu-ordering-app-web`
4. 点击 **"Import"**

#### 3. 配置构建设置

**Framework Preset:** `Vite`

**Root Directory:** `.` (保持默认)

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

#### 4. 添加环境变量

点击 "Environment Variables" 添加：

```
SUPABASE_URL = [你的 Supabase URL]
SUPABASE_ANON_KEY = [你的 Supabase anon key]
SUPABASE_SERVICE_KEY = [你的 Supabase service key]
VITE_API_BASE_URL = /api/v1
VITE_SUPABASE_URL = [你的 Supabase URL]
VITE_SUPABASE_ANON_KEY = [你的 Supabase anon key]
```

#### 5. 点击 "Deploy"

等待 2-3 分钟完成部署。

### ✅ 完成！

部署成功后：
- 你会获得一个 URL（如 `https://menu-ordering-app-web.vercel.app`）
- **以后每次 `git push` 都会自动部署**
- 可以在 Vercel Dashboard 查看部署历史和日志

### 📚 详细文档

查看 `VERCEL_SETUP_GUIDE.md` 获取完整设置指南和故障排查。
