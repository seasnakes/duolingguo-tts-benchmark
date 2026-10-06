# 多玲国 TTS 试听对比

网页源文件在 site/。较大媒体保存为小块；GitHub Actions 自动还原、核验 SHA-256 并部署 GitHub Pages。

公开入口：https://seasnakes.github.io/duolingguo-tts-benchmark/

音频保留原始文件。原片为 720p 在线预览，本地原始 1080p 视频保留。

完整 1080p 原片存放于飞书。网页优先使用飞书原片，每 6 小时刷新临时媒体链接；连接失败时使用已打包的 720p 预览。密钥仅保存在 GitHub 部署环境 Secrets。
