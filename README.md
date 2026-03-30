# 🍳 家庭点菜系统

一个温馨可爱的家庭点菜 Web 应用，采用像素艺术风格设计，让家庭点菜变得简单有趣！

![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)
![Vue](https://img.shields.io/badge/Vue-3.4-4FC08D?logo=vue.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi)
![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ 特性

- 🎨 **温馨像素风格** - 采用可爱的像素艺术设计和温暖的配色方案
- 📱 **移动优先** - 完美适配移动端，流畅的操作体验
- 🍽️ **菜品管理** - 轻松添加、编辑、删除菜品
- 📝 **每日菜单** - 快速创建当日菜单，记录家庭美食
- 🎨 **搭配清单** - 保存常用菜品搭配，一键复用
- 📅 **历史记录** - 回顾过去的点菜记录，避免重复
- ⚡ **丝滑体验** - 60fps 流畅动画，响应迅速
- 🎯 **简单易用** - 直观的界面，全家老少皆宜

## 🛠️ 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全
- **Vite** - 快速构建工具
- **Pinia** - 状态管理
- **Vue Router** - 路由管理
- **Axios** - HTTP 客户端

### 后端
- **Python 3.11+** - 编程语言
- **FastAPI** - 高性能 Web 框架
- **Supabase** - PostgreSQL 数据库（可选用内存存储演示）

### 部署
- **Vercel** - 前端和后端部署
- **GitHub** - 代码托管和 CI/CD

## 🚀 快速开始

### 前置要求

- Node.js 18+ (推荐 20+)
- Python 3.11+
- npm 或 yarn

### 安装步骤

1. **克隆仓库**

```bash
git clone <your-repo-url>
cd menu-web
```

2. **安装前端依赖**

```bash
cd frontend
npm install
```

3. **安装后端依赖**

```bash
cd ../backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. **配置环境变量**

```bash
# 前端 (.env)
cp frontend/.env.example frontend/.env

# 后端 (.env)
cp backend/.env.example backend/.env
```

5. **启动开发服务器**

**终端 1 - 后端**:
```bash
cd backend
source venv/bin/activate
python main.py
```

**终端 2 - 前端**:
```bash
cd frontend
npm run dev
```

6. **访问应用**

- 前端: http://localhost:5173
- 后端 API: http://localhost:8002
- API 文档: http://localhost:8002/docs

## 📖 使用指南

### 1. 添加菜品

- 点击底部导航的"菜品"
- 点击"添加菜品"按钮
- 输入菜品名称和描述
- 点击"添加"保存

### 2. 创建今日菜单

- 在首页点击"创建今日菜单"
- 从菜品列表中选择想要的菜品
- 点击"保存菜单"

### 3. 创建搭配清单

- 点击底部导航的"搭配"
- 点击"创建搭配"
- 选择常用菜品组合
- 保存后可一键应用到今日菜单

### 4. 查看历史记录

- 点击底部导航的"历史"
- 浏览过去的菜单记录
- 使用日期筛选器查找特定日期

## 🎨 设计系统

### 配色方案

- **主色**: 琥珀色 (#F59E0B)
- **强调色**: 珊瑚色 (#F87171)
- **背景色**: 奶油色 (#FEF3C7)
- **文字色**: 深灰色 (#1F2937)

### 像素风格特点

- 2-3px 像素边框
- 圆润的边角设计
- 硬阴影效果
- 流畅的过渡动画

## 🧪 测试

### 前端测试

```bash
cd frontend
npm run test:unit      # 单元测试
npm run test:e2e       # E2E 测试
```

### 后端测试

```bash
cd backend
source venv/bin/activate
pytest
```

## 📦 部署

### Vercel 部署

1. 连接 GitHub 仓库到 Vercel
2. 配置环境变量
3. 自动部署到生产环境

```bash
# 或使用 Vercel CLI
npm i -g vercel
vercel --prod
```

## 📁 项目结构

```
menu-web/
├── frontend/          # Vue 3 前端应用
│   ├── src/
│   │   ├── components/   # Vue 组件
│   │   ├── pages/        # 页面组件
│   │   ├── services/     # API 服务
│   │   ├── stores/       # Pinia 状态管理
│   │   └── assets/       # 静态资源
│   └── package.json
│
├── backend/           # FastAPI 后端应用
│   ├── src/
│   │   ├── api/          # API 端点
│   │   ├── models/       # 数据模型
│   │   ├── services/     # 业务逻辑
│   │   └── config.py     # 配置
│   ├── main.py           # 应用入口
│   └── requirements.txt
│
└── specs/             # 项目规格文档
    └── 001-family-menu-system/
        ├── spec.md        # 功能规格
        ├── plan.md        # 实施计划
        └── tasks.md       # 任务列表
```

## 🤝 贡献指南

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md) 了解详情。

## 📄 许可证

MIT License © 2026

## 🙏 致谢

- 感谢所有贡献者
- 感谢开源社区的支持
- 特别感谢家人的美食灵感 💝

---

**用 ❤️ 和 🍳 制作**
