# AGENTS.md

RSS 博客聚合站：Flask 应用，部署在 Vercel，Python 3.14（由 `mise.toml` 指定）。

## 架构与数据流（关键）

- 唯一入口 `api/index.py`（Vercel serverless），`vercel.json` 通过 rewrite `/(.*)` 把所有请求路由到它；全部路由（首页/成员/日期/个人空间/RSS/404）都在这一个文件里。
- **博客数据不在本仓库**。运行时从 `RSSBLOG_SOURCE_BASE` 拉取：默认 `https://raw.githubusercontent.com/caibingcheng/rssblog-source/public/`，数据是 `stats.min.json` + 分页 CSV（`all/N.csv`、`member/N.csv`、`date/YYYYMM/N.csv`、`source/<hash>/N.csv`、`user/<uid>/{all,member,date}/...`）。
- `utils/init.py::RssblogSource` 缓存数据 3 小时（buffercache）；数据更新后需请求 `/immediate/` 清缓存刷新。
- `api/index.py` 在 **import 时** 模块级执行 `RssblogSource()` 初始化（读 `stats.min.json`），见 `api/index.py:20`；修改代码或环境变量后必须重启才生效。
- 本地调试：把 `RSSBLOG_SOURCE_BASE` 指向本地已下载的源数据目录即可，`utils/fetch.py` 对非 URL 直接读本地文件。
- `RSSBLOG_SOURCE_BASE` 也可覆盖为 gitee / jsdelivr CDN 等（`utils/init.py:8` 中保留了注释）。

## 命令

```bash
pip install -r requirements.txt
python api/index.py        # 本地运行
python3 .github/workflows/test_workflow_logic.py   # 工作流逻辑测试，纯脚本无 pytest
```

- 无 lint / typecheck 配置；仓库仅有一个测试脚本，跑法是直接执行该 `.py` 文件。

## 订阅管理工作流（gist）

- `.github/workflows/manage-gist.yml`：issue 评论包含 `ADD <section> <URL>` / `DELETE <section> <URL>` 时更新硬编码的 gist（个人空间订阅列表数据源），仅仓库 owner 可触发，需要 `GIST_TOKEN` secret。
- 工作流逻辑与真实行为通过 `contains()` 子串匹配触发，与测试脚本保持一致。
- 改动 workflow 时不要裸奔 secret；gist ID 是 `adf8f300dc50a61a965bdcc6ef0aecb3`。

## 站点约定

- README.md 会被 `api/index.py` 读取（`utils/markdown.py`）用于 about 页面；/about/ 路由当前被 `abort(404)` 禁用（`api/index.py:227`）。
- 皮肤资源在 `static/custom.css` / `custom.js` + `templates/*.html`；`.gitignore` 忽略 `__pycache__`、`local overrides`（`/api/utils*`）等，提交时留意。
