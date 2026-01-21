# LordFoxFairy 的笔记博客

基于 Hugo 和 PaperMod 主题构建的个人笔记博客。

## 功能特性

- 自动同步 [NiKo-NoteBook](https://github.com/LordFoxFairy/NiKo-NoteBook) 仓库的笔记内容
- 每天北京时间凌晨 1:00 自动更新笔记
- 推送代码时自动触发部署
- 支持手动触发部署

## 目录结构

```
.
├── content/
│   ├── notebooks/          # NiKo-NoteBook 仓库内容（Git Submodule）
│   └── posts/              # 其他博客文章
├── themes/
│   └── PaperMod/           # PaperMod 主题（Git Submodule）
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions 自动部署配置
├── update-notebooks.sh     # 本地更新笔记脚本
└── hugo.toml              # Hugo 配置文件
```

## 使用方法

### 本地开发

1. 克隆仓库并初始化 submodules:
```bash
git clone --recursive https://github.com/LordFoxFairy/LordFoxFairy.github.io.git
cd LordFoxFairy.github.io
```

2. 启动 Hugo 本地服务器:
```bash
hugo server -D
```

3. 访问 http://localhost:1313 查看网站

### 更新笔记内容

#### 本地更新

运行更新脚本:
```bash
./update-notebooks.sh
```

该脚本会:
- **强制拉取** NiKo-NoteBook 仓库的最新内容
- **覆盖所有本地修改** (确保内容与远程仓库保持一致)
- 自动提交更新
- 提示你执行 `git push` 推送到远程

⚠️ **注意**: 此脚本会强制覆盖 `content/notebooks/` 目录下的所有本地修改，请勿在该目录下进行手动编辑。

#### 测试更新功能

运行测试脚本查看更新过程:
```bash
./test-update.sh
```

#### 自动更新

配置了三种自动更新机制:

1. **定时更新**: 每天北京时间凌晨 1:00 (UTC 17:00) 自动更新
2. **推送触发**: 向 main 分支推送代码时自动更新和部署
3. **手动触发**: 在 GitHub Actions 页面手动触发工作流

## 工作流程

1. 在 NiKo-NoteBook 仓库更新笔记
2. 等待定时任务自动同步，或运行 `./update-notebooks.sh` 手动同步
3. GitHub Actions 自动构建并部署到 GitHub Pages

## 配置说明

### Hugo 配置 (hugo.toml)

- 站点地址: https://LordFoxFairy.github.io/
- 主题: PaperMod
- 语言: 中文
- 启用了阅读时间和字数统计

### GitHub Actions 配置

- Hugo 版本: 0.112.0
- 自动更新 submodules
- 构建并部署到 gh-pages 分支

## 许可证

本项目仅用于个人笔记分享。
