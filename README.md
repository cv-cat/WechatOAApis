<div align="center">
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
    </a>
    <a href="https://fastapi.tiangolo.com/">
        <img src="https://img.shields.io/badge/FastAPI-0.115%2B-009688" alt="FastAPI">
    </a>
</div>

# 💬 WeChat Platform

**✨ 专业的微信公众号数据采集解决方案，支持公众号文章全量抓取与内容解析**

## ⚠️ 前置条件

运行此代码需要有微信公众号的账户：https://mp.weixin.qq.com/

**⚠️ 严禁用于爬取用户隐私、违规商业用途！本项目仅供学习与技术研究使用，后果自负。**

## 🌟 功能特性

- ✅ **公众号数据采集**
  - 支持通过公众号名称搜索获取 `fakeid`
  - 支持获取公众号全量文章列表，自动翻页
  - 支持解析文章详情（标题、正文、图片、作者、发布时间、地区）

## 🛠️ 快速开始

### ⛳ 运行环境

- Python 3.10+

### 🎯 本地安装

```bash
pip install -r requirements.txt
```

### 🚀 运行项目

```bash
python App.py
```

服务启动后访问 http://localhost:5004/docs 查看交互式 API 文档。

### 🎨 Token 与 Cookie 配置

在登录微信公众号 PC 端后，按 `F12` 抓包，任何接口的 `param` 都会有 `token`，以及请求头里有 `cookie`。

1. 打开 [mp.weixin.qq.com](https://mp.weixin.qq.com/) 并登录账号
2. 按 `F12` 打开开发者工具，点击「网络」
3. 找任意一个接口请求，在 URL 参数中复制 `token` 字段值，在请求头中复制 `Cookie` 字段值

## 📡 接口说明

### POST `/get_fakeid`

通过公众号名称搜索获取公众号的唯一标识 `fakeid`。

**请求参数**

| 字段          | 类型  | 必填 | 说明             |
|-------------|-----|----|----------------|
| query       | str | 是  | 公众号名称          |
| token       | str | 是  | 登录后抓包获取的 token |
| cookies_str | str | 是  | 登录后抓包获取的 cookie |

**请求示例**

```bash
curl -X POST http://localhost:5004/get_fakeid \
  -H "Content-Type: application/json" \
  -d '{
    "query": "公众号名称",
    "token": "xxxxxxxx",
    "cookies_str": "RK=xxx; slave_sid=xxx; ..."
  }'
```

**响应示例**

```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "list": [
      {
        "fakeid": "MzU1MDk0ODI0Mw==",
        "nickname": "公众号昵称",
        "alias": "gh_xxxxxxxx",
        "round_head_img": "https://..."
      }
    ]
  }
}
```

---

### POST `/get_shop_works`

获取指定公众号的全量文章列表（自动翻页）。

**请求参数**

| 字段          | 类型  | 必填 | 说明                     |
|-------------|-----|----|------------------------|
| fakeid      | str | 是  | 公众号唯一标识（由 /get_fakeid 获取）|
| token       | str | 是  | 登录后抓包获取的 token         |
| cookies_str | str | 是  | 登录后抓包获取的 cookie        |
| sleep_time  | int | 是  | 每次请求间隔秒数（建议 ≥ 10，防频控）  |

**请求示例**

```bash
curl -X POST http://localhost:5004/get_shop_works \
  -H "Content-Type: application/json" \
  -d '{
    "fakeid": "MzU1MDk0ODI0Mw==",
    "token": "xxxxxxxx",
    "cookies_str": "RK=xxx; slave_sid=xxx; ...",
    "sleep_time": 10
  }'
```

**响应示例**

```json
{
  "code": 200,
  "message": "成功",
  "data": [
    {
      "publish_time": 1700000000,
      "publish_info": "{\"appmsgex\":[{\"title\":\"文章标题\",\"link\":\"https://mp.weixin.qq.com/s?...\"}]}"
    }
  ]
}
```

---

### POST `/get_work_detail`

解析微信公众号文章详情，提取标题、正文、图片、作者、发布时间等信息。

**请求参数**

| 字段  | 类型  | 必填 | 说明         |
|-----|-----|----|------------|
| url | str | 是  | 文章的完整 URL |

**请求示例**

```bash
curl -X POST http://localhost:5004/get_work_detail \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://mp.weixin.qq.com/s?__biz=xxx&mid=xxx&idx=1&sn=xxx"
  }'
```

**响应示例**

```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "source_platform": "wx",
    "url": "https://mp.weixin.qq.com/s?...",
    "title": "文章标题",
    "content": "文章正文内容...",
    "images": ["https://mmbiz.qpic.cn/..."],
    "author": {
      "user": "作者昵称",
      "profile": "公众号名称",
      "city": "广东"
    },
    "time": "1700000000"
  }
}
```

## 🐳 Docker 部署

```bash
docker build -t wechat-platform .
docker run -d -p 5004:5004 wechat-platform
```

## 🍥 日志

| 日期       | 说明                                         |
|----------|--------------------------------------------|
| 26/04/11 | 项目初始化，完成公众号 fakeid 搜索、文章全量采集、文章详情解析 API 封装 |

## 🤝 欢迎贡献 PR

本项目欢迎任何形式的贡献！如果你有新功能想法、Bug 修复或文档改进，欢迎提交 PR。

- Fork 本仓库并在新分支上开发
- 保持代码风格与现有代码一致
- PR 描述中请简要说明改动内容和目的

## 🧸 额外说明
1. 感谢 star⭐ 和 follow📰！不时更新
2. 作者的联系方式在主页里，有问题可以随时联系我
3. 可以关注下作者的其他项目，欢迎 PR 和 issue
4. 感谢赞助！如果此项目对您有帮助，请作者喝一杯奶茶~~ （开心一整天😊😊）
5. thank you~~~
