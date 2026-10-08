# 多玲国 TTS 试听对比

[试听主页](https://seasnakes.github.io/duolingguo-tts-benchmark/) · [逐句原片对照](https://seasnakes.github.io/duolingguo-tts-benchmark/aligned.html)

网页源文件在 `site/`。GitHub Actions 还原并核验媒体文件后部署到 Pages。

完整 1080p 原片存放于飞书，已通过完整下载的 SHA-256 核验。网页优先使用飞书原片，每 6 小时刷新媒体链接；连接失败时切换至已打包的 720p 预览。音频保留完整原始样本。

飞书应用凭据仅保存在 GitHub 部署环境 Secrets，网页不包含应用凭据。

原视频来源：[咪Mirror肉《多 玲 国》](https://www.bilibili.com/video/BV1Zmuk6kExf)。

## 发布就绪检查

上传后先轮询本次运行的 `github-pages` 文件包，核对上传步骤返回的 ID、未过期及非空，再执行 Pages 发布。最多查询 12 次、间隔 10 秒，每次请求最多 15 秒；步骤总超时 6 分钟。临时网络或 5xx 错误可重试，权限错误立即失败。该检查缓解上传完成后短暂查询不到文件包的情况，不掩盖持续故障。

本地回归检查：`python3 -m unittest discover -s scripts -p "test_*.py" -v`。
