# Nodejs 笔记

## nvm

nvm 是 node 版本管理工具，可以安装多个版本的 node，切换不同版本的 node。

安装命令

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
```

常用命令

```bash
nvm install --lts        # 安装最新 LTS 版本
nvm install 20           # 安装指定大版本
nvm use 20               # 切换到指定版本
nvm ls                   # 列出已安装的版本
nvm alias default 20     # 设置默认版本
```

## npm

npm 是 Node.js 的默认包管理工具，随 Node.js 一起安装。

常用命令

```bash
npm init -y                     # 快速初始化项目
npm install <package>           # 安装依赖到 dependencies
npm install -D <package>        # 安装依赖到 devDependencies
npm install -g <package>        # 全局安装
npm uninstall <package>         # 卸载依赖
npm update                      # 更新所有依赖
npm list --depth=0              # 查看已安装的顶层依赖
npm outdated                    # 检查过期依赖
npm cache clean --force         # 清除缓存
```

## npx

npx 是 npm 5.2+ 自带的命令执行工具，用于执行 npm 包中的命令，无需全局安装。

核心用途：

1. **执行未安装的包** — 临时下载并执行，用完即删，不污染全局环境
2. **执行项目本地安装的包** — 无需写 `./node_modules/.bin/` 前缀
3. **指定版本执行** — 可以临时使用特定版本的工具

```bash
npx create-react-app my-app          # 创建 React 项目（无需全局安装 create-react-app）
npx create-next-app@latest my-app    # 创建 Next.js 项目
npx ts-node script.ts                # 临时用 ts-node 执行 TypeScript 文件
npx eslint .                         # 执行项目本地的 eslint
npx -p node@18 node -v               # 临时使用指定 Node 版本执行命令
npx -y <package>                     # 跳过确认提示直接执行
```

npx 与 npm 的区别：`npm install -g` 会将包永久安装到全局，而 `npx` 临时下载执行后自动清理，适合低频使用的 CLI 工具。

## pnpm

pnpm 是高性能的 npm 替代品，通过硬链接共享依赖，节省磁盘空间，安装速度更快。

安装

```bash
npm install -g pnpm
```

常用命令

```bash
pnpm install                    # 安装所有依赖
pnpm add <package>              # 安装依赖
pnpm add -D <package>           # 安装开发依赖
pnpm remove <package>           # 卸载依赖
pnpm dlx <package>              # 类似 npx，临时执行包命令
```

## yarn

yarn 是 Facebook 推出的包管理工具，与 npm 功能类似。

安装

```bash
corepack enable                 # Node.js 16.10+ 内置 corepack，启用后可直接使用 yarn
```

常用命令

```bash
yarn init -y                    # 初始化项目
yarn add <package>              # 安装依赖
yarn add -D <package>           # 安装开发依赖
yarn remove <package>           # 卸载依赖
yarn dlx <package>              # 类似 npx，临时执行包命令
```

## 常用 Node.js 开发工具

| 工具        | 用途                         | 安装方式                  |
| ----------- | ---------------------------- | ------------------------- |
| nodemon     | 文件变动时自动重启 Node 服务 | `npm install -D nodemon`  |
| ts-node     | 直接运行 TypeScript 文件     | `npm install -D ts-node`  |
| tsx         | 更快的 TypeScript 执行工具   | `npm install -D tsx`      |
| eslint      | 代码检查                     | `npm init @eslint/config` |
| prettier    | 代码格式化                   | `npm install -D prettier` |
| http-server | 零配置静态文件服务器         | `npx http-server`         |
| json-server | 快速搭建 REST API mock 服务  | `npx json-server db.json` |
