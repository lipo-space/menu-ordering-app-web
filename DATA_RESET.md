# 数据清空指南

## 清空所有数据的方法

### 1. 后端数据（菜品和菜单）

#### 方法 A: 使用 API 端点（推荐）
```bash
# 清空所有后端数据
curl -X DELETE http://localhost:8000/api/v1/admin/clear-all
```

#### 方法 B: 重启后端服务
后端使用内存存储，重启服务会自动清空所有数据：
```bash
# 停止后端服务 (Ctrl+C)
# 然后重新启动
cd backend
python main.py
```

### 2. 前端数据（搭配）

#### 方法 A: 使用浏览器控制台（推荐）
1. 打开浏览器开发者工具 (F12 或 Cmd+Option+I)
2. 进入 Console（控制台）标签
3. 运行以下命令：
```javascript
localStorage.removeItem('family-menu-combinations')
location.reload()
```

#### 方法 B: 使用 Application 面板
1. 打开浏览器开发者工具 (F12 或 Cmd+Option+I)
2. 进入 Application（应用）标签
3. 在左侧菜单找到 "Local Storage"
4. 点击你的网站域名
5. 找到 `family-menu-combinations` 这一行
6. 右键删除或点击删除按钮
7. 刷新页面

### 3. 一键清空脚本

在项目根目录运行：
```bash
# 清空后端数据
curl -X DELETE http://localhost:8000/api/v1/admin/clear-all

# 清空前端数据（需要在浏览器控制台运行）
# localStorage.removeItem('family-menu-combinations'); location.reload();
```

## 数据存储位置

- **后端**: 内存存储（temp_dishes_db, temp_menus_db）
- **前端**: localStorage（family-menu-combinations）

## 注意事项

⚠️ **数据不可恢复**: 清空操作会永久删除所有数据，请确保在测试环境中使用。

⚠️ **后端数据**: 由于使用内存存储，后端重启后会自动清空所有数据。

⚠️ **前端数据**: 搭配数据存储在浏览器的 localStorage 中，需要手动清空。

## 初始状态

- 后端已设置为不初始化示例数据（INIT_WITH_SAMPLE_DATA = False）
- 首次启动时，系统将从空数据库开始
- 你需要手动添加菜品、创建搭配和菜单
