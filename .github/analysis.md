```angular2html

├── ISSUE_TEMPLATE                 # Directory containing templates for issues.
│   ├── bug-report.md              # Template for reporting bugs. Guides users to provide necessary information to identify and fix bugs.
│   ├── config.yml                 # Configuration file for issue template settings. Determines how templates are shown to users.
│   └── feature-request.md         # Template for requesting new features. Helps users to describe the feature and its benefits clearly.
├── SECURITY.md                    # Security policy. Provides information on reporting security vulnerabilities in the project.
├── dependabot.yml                 # Dependabot configuration file. Automates dependency updates, ensuring the project uses the latest secure versions.
├── pull_request_template.md       # Template for pull requests. Helps contributors to provide a consistent and comprehensive description of their changes.
└── workflows                      # Directory containing GitHub Actions workflows.
    ├── lock.yaml                  # Workflow to lock closed issues and pull requests after a period of inactivity, preventing spam and off-topic discussions.
    ├── publish.yaml               # Workflow for publishing the project, such as pushing to package registries or deploying to hosting services.
    └── tests.yaml                 # Workflow for running tests. Ensures that contributions do not break existing functionality.


```

```angular2html
Flask 官方 GitHub `.github` 目录结构:

├── ISSUE_TEMPLATE                 # 包含问题模板的目录。
│   ├── bug-report.md              # 报告错误的模板。指导用户提供识别和修复错误所需的信息。
│   ├── config.yml                 # 问题模板设置的配置文件。决定如何向用户展示模板。
│   └── feature-request.md         # 新功能请求的模板。帮助用户清晰描述所需功能及其益处。
├── SECURITY.md                    # 安全政策文件。提供有关在项目中报告安全漏洞的信息。
├── dependabot.yml                 # Dependabot 配置文件。自动更新依赖项，确保项目使用最新安全版本。
├── pull_request_template.md       # 拉取请求的模板。帮助贡献者提供一致和全面的更改描述。
└── workflows                      # 包含 GitHub Actions 工作流的目录。
    ├── lock.yaml                  # 工作流文件，用于在一段时间无活动后锁定关闭的问题和拉取请求，防止垃圾邮件和偏题讨论。
    ├── publish.yaml               # 工作流文件，用于发布项目，如推送到包注册中心或部署到托管服务。
    └── tests.yaml                 # 工作流文件，用于运行测试。确保贡献不会破坏现有功能。

```
