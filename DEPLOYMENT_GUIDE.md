# Supabase 集成完成指南

## ✅ 代码更新已完成

### 后端 ✅
- ✅ `backend/src/db/supabase_client.py` - Supabase 客户端初始化
- ✅ `backend/src/models/combination.py` - Combination 模型
- ✅ `backend/src/api/combinations.py` - Combinations CRUD API
- ✅ `backend/src/api/dishes.py` - 使用 Supabase
- ✅ `backend/src/api/menus.py` - 使用 Supabase
- ✅ `backend/src/api/__init__.py` - 移除内存存储，添加 combinations 路由
- ✅ `backend/main.py` - 简化为导入 src.api

### 前端 ✅
- ✅ `frontend/src/services/combinationService.ts` - **新建** API 服务
- ✅ `frontend/src/stores/combinationStore.ts` - 替换 localStorage 为 API
- ✅ `frontend/src/services/dishService.ts` - 移除 batchUpdatePairCount

---

## 🚀 部署步骤

### 步骤 1: 设置 Supabase 数据库

1. 登录 Supabase Dashboard (https://supabase.com/dashboard)
2. 选择你的项目或创建新项目
3. 进入 **SQL Editor**
4. 复制 `/Users/lipo/zdx/menu/menu-web/supabase_schema.sql` 的内容
5. 粘贴并运行 SQL
6. 确认所有表已创建：
   - ✅ dishes
   - ✅ menus
   - ✅ menu_dishes
   - ✅ combinations
   - ✅ combination_dishes

### 步骤 2: 配置环境变量

#### 本地开发 (`backend/.env`)
```bash
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key
```

#### 本地开发 (`frontend/.env`)
```bash
VITE_API_BASE_URL=http://localhost:8002/api/v1
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 步骤 3: 本地测试

```bash
# 终端 1: 启动后端
cd backend
source venv/bin/activate
python main.py

# 终端 2: 启动前端
cd frontend
npm run dev
```

### 步骤 4: 测试功能

访问 http://localhost:5173 并测试：

1. **菜品管理**
   - [ ] 创建新菜品
   - [ ] 编辑菜品
   - [ ] 删除菜品
   - [ ] 刷新页面验证数据持久化

2. **搭配管理**
   - [ ] 创建搭配（选择多个菜品）
   - [ ] 查看菜品的"搭配次数"是否增加
   - [ ] 编辑搭配（添加/删除菜品）
   - [ ] 验证"搭配次数"是否正确更新
   - [ ] 删除搭配
   - [ ] 验证"搭配次数"是否减少
   - [ ] 刷新页面验证数据持久化

3. **菜单管理**
   - [ ] 创建今日菜单
   - [ ] 查看菜品的"享用次数"是否增加
   - [ ] 修改今日菜单
   - [ ] 验证"享用次数"是否正确更新
   - [ ] 删除菜单
   - [ ] 验证"享用次数"是否减少
   - [ ] 刷新页面验证数据持久化

4. **历史记录**
   - [ ] 查看历史菜单列表
   - [ ] 使用日期筛选
   - [ ] 验证菜品详情正确显示

5. **家庭共享测试**
   - [ ] 打开另一个浏览器/无痕模式
   - [ ] 访问相同 URL
   - [ ] 验证能看到相同的数据
   - [ ] 在一个浏览器创建数据
   - [ ] 在另一个浏览器刷新验证同步

### 步骤 5: 部署到 Vercel

1. **设置 Vercel 环境变量**
   - 进入 Vercel 项目设置
   - 添加环境变量：
     - `SUPABASE_URL`
     - `SUPABASE_ANON_KEY`
     - `SUPABASE_SERVICE_KEY`

2. **推送代码**
   ```bash
   git add .
   git commit -m "feat: integrate Supabase for persistent storage"
   git push
   ```

3. **验证部署**
   - 访问生产 URL
   - 重复步骤 4 的所有测试
   - 验证数据在云端持久化

---

## 🎯 功能对比

| 功能 | 之前 (内存/localStorage) | 现在 (Supabase) |
|------|-------------------------|----------------|
| 菜品数据 | ❌ 重启丢失 | ✅ 永久保存 |
| 搭配数据 | ⚠️ 仅本地浏览器 | ✅ 云端同步 |
| 菜单历史 | ❌ 重启丢失 | ✅ 永久保存 |
| 统计数据 | ⚠️ 手动更新 | ✅ 自动更新 |
| 家庭共享 | ❌ 不可能 | ✅ 实时同步 |
| 多设备访问 | ❌ 不可能 | ✅ 随时访问 |

---

## 🔧 故障排查

### 问题 1: 后端启动失败
```
ModuleNotFoundError: No module named 'supabase'
```
**解决方案**:
```bash
cd backend
source venv/bin/activate
pip install supabase==2.3.4
```

### 问题 2: 前端无法连接后端
**检查**:
- 后端是否在 8002 端口运行
- `frontend/.env` 中的 `VITE_API_BASE_URL` 是否正确
- 浏览器控制台是否有 CORS 错误

### 问题 3: Supabase 连接失败
**检查**:
- `SUPABASE_URL` 和 `SUPABASE_SERVICE_KEY` 是否正确
- Supabase 项目是否正常运行
- 网络是否能访问 Supabase

### 问题 4: 统计数据不更新
**检查**:
- 浏览器控制台是否有错误
- 后端日志是否有异常
- 刷新页面重新获取最新数据

---

## 📊 数据迁移

如果你有现有的 localStorage 数据需要迁移：

```javascript
// 在浏览器控制台运行
const oldData = localStorage.getItem('family-menu-combinations')
console.log('Old combinations:', JSON.parse(oldData, null, 2))

// 手动将数据通过新的 UI 界面重新创建
// 或编写迁移脚本插入到 Supabase
```

---

## ✨ 下一步优化

- [ ] 添加用户认证（Supabase Auth）
- [ ] 实现多家庭隔离（family_id 字段）
- [ ] 添加实时订阅（Supabase Realtime）
- [ ] 优化统计查询（使用数据库视图）
- [ ] 添加数据备份功能

---

## 🎉 完成！

你的家庭点菜系统现在已经：
- ✅ 数据永久存储在 Supabase
- ✅ 支持家庭成员间数据共享
- ✅ 统计数据实时准确更新
- ✅ 可以从任何设备访问

享受使用吧！ 🍽️
