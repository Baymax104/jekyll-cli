# Power Jekyll

`Power Jekyll`是一个用于管理Jekyll博客的PowerShell模块，它通过`blog`命令提供了一组命令，可以方便地进行博客的本地开发、创建、发布等操作

## 功能

通过`blog`命令提供了以下功能：

- `serve`: 在本地通过Jekyll启动博客服务器
- `list`: 列出所有的博文和草稿
- `open`: 在编辑器中打开指定的博文或草稿
- `draft`: 创建一个位于`_drafts`目录下的新草稿
- `post`: 创建一个位于`_posts`目录下的新博文
- `publish`: 发布一个草稿，将其移动到`_posts`目录下
- `unpublish`: 撤销一篇已发布的博文，将其移动回`_drafts`目录

其他功能

- 自动补全子命令
- 自动补全`_posts`目录和`_drafts`目录下的文件名

## 安装

在使用之前，你需要额外安装`argcomplete`包和`ruamel.yaml`包，可以在你的Python环境中使用下面的命令安装

```powershell
pip install argcomplete
pip install ruamel.yaml
```

安装完成后，你可以在PowerShell中通过`Import-Module`命令导入模块，类似下面的命令

```powershell
Import-Module -Name "本程序目录的绝对路径"
```

或将程序目录移动到PowerShell的模块安装目录中，安装目录路径可通过`PSModulePath`环境变量查看

移动后，PowerShell会自动加载模块，或通过`Import-Module`命令导入

```powershell
Import-Module PowerJekyll
```

## 关于config.yml

`config.yml`中可以配置博客的格式头`yaml fomatter`，在使用`post`、`draft`命令时，会使用配置的格式头初始化文档

```yaml
# yaml formatter
formatter:
  draft:
    layout: post
    title:
    categories: []
    tags: []

  post:
    layout: post
    title:
    categories: []
    tags: []
    date:  
```

## 使用示例

下面是一些使用示例：

```powershell
# 启动本地服务器
blog serve
blog s

# 本地博客显示草稿
blog s -d

# 列出所有的博文和草稿
blog list
blog l

# 创建一个新的草稿
blog draft my-draft
blog d my-draft

# 打开指定的博文或草稿
blog open 2024-05-23-my-post
blog o 2024-05-23-my-post

# 发布一个草稿
blog publish my-draft
blog pub my-draft

# 撤销发布一篇已发布的博文
blog unpublish 2024-05-23-my-post
blog unpub 2024-05-23-my-post
```
