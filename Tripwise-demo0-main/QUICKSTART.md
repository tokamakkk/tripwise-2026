# TralP 快速启动指南

⚡ 5 分钟快速启动 TralP 旅行规划系统

## 📋 前置要求

- ✅ Python 3.9 或更高版本
- ✅ Firebase 账号（免费）
- ✅ Ollama（用于本地 LLM）或 OpenAI API key
- ✅ Serper API key（用于搜索功能）

## 🚀 5 步快速启动

### 步骤 1：克隆并安装

```bash
# 克隆项目
cd /path/to/your/projects
git clone <repository-url>
cd TralP

# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 步骤 2：配置 Firebase

1. **创建 Firebase 项目**
   - 访问：https://console.firebase.google.com/
   - 点击"添加项目"
   - 按照向导完成项目创建

2. **启用 Authentication**
   - 在 Firebase 控制台选择你的项目
   - 左侧菜单 → Authentication → 开始使用
   - 选择"电子邮件/密码"并启用

3. **启用 Realtime Database**
   - 左侧菜单 → Realtime Database → 创建数据库
   - 选择"测试模式"（开发环境）
   - 记录数据库 URL（例如：https://your-project.firebaseio.com）

4. **获取 Firebase 配置**
   - 项目设置 → 常规 → 你的应用
   - 选择 Web 应用（</>）
   - 复制配置信息

5. **下载 Service Account**
   - 项目设置 → 服务账号
   - 点击"生成新的私钥"
   - 保存 JSON 文件为 `firebase-admin-sdk.json`
   - 将文件放在项目根目录

### 步骤 3：配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
nano .env  # 或使用你喜欢的编辑器
```

填入必要的配置：

```env
# Flask 配置
SECRET_KEY=your-super-secret-key-change-this
DEBUG=True

# Firebase 配置（从步骤 2 获取）
FIREBASE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789012
FIREBASE_APP_ID=1:123456789012:web:abcdef123456

# Firebase Admin SDK
FIREBASE_ADMIN_CREDENTIALS_PATH=./firebase-admin-sdk.json

# LLM 配置（Ollama 本地）
LLM_MODEL=ollama/llama3.2:1b
LLM_BASE_URL=http://127.0.0.1:11434
LLM_PROVIDER=ollama

# Serper API（必需，用于搜索）
SERPER_API_KEY=your-serper-api-key

# 第三方 API（可选）
AMAP_API_KEY=your-amap-key
CTRIP_API_KEY=your-ctrip-key
CTRIP_API_SECRET=your-ctrip-secret
```

**获取 Serper API Key：**
1. 访问：https://serper.dev/
2. 注册账号（免费提供 2500 次查询）
3. 复制 API key

### 步骤 4：启动 Ollama（如果使用本地 LLM）

```bash
# 安装 Ollama（如果还没安装）
# macOS/Linux: curl -fsSL https://ollama.com/install.sh | sh
# Windows: 下载安装程序 https://ollama.com/download

# 启动 Ollama 服务
ollama serve

# 在新终端中拉取模型
ollama pull llama3.2:1b

# 验证模型可用
ollama list
```

### 步骤 5：启动应用

```bash
# 在项目目录中
python run.py
```

看到以下输出表示启动成功：

```
🚀 Starting TralP AI Travel Planner on http://0.0.0.0:5000
📝 Debug mode: True
🌍 Environment: development
 * Running on http://0.0.0.0:5000
```

## ✅ 验证安装

### 1. 健康检查

```bash
curl http://localhost:5000/health
```

应返回：
```json
{"status": "healthy", "message": "TralP API is running"}
```

### 2. 注册测试用户

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123456",
    "display_name": "测试用户"
  }'
```

### 3. 在 Firebase 控制台验证

1. 打开 Firebase 控制台
2. 进入 Authentication → Users
3. 应该能看到刚注册的用户
4. 进入 Realtime Database → Data
5. 应该能看到 `users` 节点下的用户数据

## 🎯 第一个旅行计划

### 1. 使用 Python 脚本测试

创建 `test_api.py`：

```python
import requests
import json
import time

BASE_URL = "http://localhost:5000"

# 1. 注册用户
print("📝 注册用户...")
response = requests.post(f"{BASE_URL}/api/auth/register", json={
    "email": "traveler@example.com",
    "password": "password123",
    "display_name": "旅行者"
})
print(f"注册结果: {response.status_code}")

# 2. 使用 Firebase SDK 获取 token（这里简化，实际需要在客户端完成）
# 为了测试，我们先跳过真实的登录，直接使用注册返回的信息

print("\n💡 提示：在实际应用中，需要使用 Firebase SDK 在客户端登录获取 token")
print("这里为了演示，假设你已经获得了 Firebase ID token")

# 注意：需要真实的 Firebase token 才能继续
# 你可以在浏览器中使用 Firebase SDK 登录并获取 token
```

### 2. 使用 Postman 或 curl 测试

#### Step 1: 注册用户

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "password": "yourpassword",
    "display_name": "Your Name"
  }'
```

#### Step 2: 使用 Firebase SDK 登录（在浏览器或客户端应用中）

```javascript
// 示例 JavaScript 代码
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";

const auth = getAuth();
signInWithEmailAndPassword(auth, "your@email.com", "yourpassword")
  .then((userCredential) => {
    userCredential.user.getIdToken().then((token) => {
      console.log("Token:", token);
      // 使用这个 token 调用 API
    });
  });
```

#### Step 3: 创建旅行计划

```bash
curl -X POST http://localhost:5000/api/travel/plan \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN_HERE" \
  -d '{
    "from_location": "北京",
    "destination": "成都",
    "num_people": 2,
    "duration": 5,
    "budget": 5000
  }'
```

#### Step 4: 查询计划状态

```bash
# 使用返回的 plan_id
curl http://localhost:5000/api/travel/plans/PLAN_ID/status \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN_HERE"
```

#### Step 5: 获取完整计划

```bash
curl http://localhost:5000/api/travel/plans/PLAN_ID \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN_HERE"
```

## 🔧 常见问题

### Firebase 初始化失败

**错误**：`Error initializing Firebase`

**解决**：
1. 确认 `firebase-admin-sdk.json` 文件存在
2. 检查文件路径是否正确
3. 验证 JSON 文件格式是否有效

### Ollama 连接失败

**错误**：`Connection refused on port 11434`

**解决**：
1. 确认 Ollama 服务正在运行：`ollama serve`
2. 检查端口是否被占用：`lsof -i :11434`
3. 验证模型已下载：`ollama list`

### Serper API 错误

**错误**：`Serper API key not configured`

**解决**：
1. 确认 `.env` 中配置了 `SERPER_API_KEY`
2. 检查 API key 是否有效
3. 访问 https://serper.dev/ 查看使用配额

### 端口已被占用

**错误**：`Address already in use`

**解决**：
```bash
# 查找占用端口的进程
lsof -i :5000

# 或更改端口
FLASK_PORT=8000 python run.py
```

## 📚 下一步

- 📖 阅读 [完整文档](README.md)
- 🏗️ 了解 [项目结构](STRUCTURE.md)
- 🧪 运行 [测试](tests/README.md)
- 🔌 探索 [API 文档](app/routes/README.md)
- 🤖 学习 [AI Agents](app/agents/README.md)

## 💡 提示

1. **开发模式**：在 `.env` 中设置 `DEBUG=True` 以获取详细错误信息
2. **日志**：查看终端输出了解 AI agents 的工作过程
3. **Firebase 规则**：生产环境务必配置适当的安全规则
4. **API 配额**：注意第三方 API 的使用限制

## 🎉 完成！

现在你已经成功启动了 TralP！开始探索 AI 驱动的旅行规划功能吧！

需要帮助？查看 [README.md](README.md) 获取更多信息。

