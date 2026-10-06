(async () => {
  const videos = [...document.querySelectorAll('video[data-reference-video]')];
  if (!videos.length) return;
  try {
    const response = await fetch('source-media.json', {cache: 'no-store'});
    if (!response.ok) return;
    const source = await response.json();
    const age = Date.now() - Date.parse(source.updated_at);
    if (!source.url?.startsWith('https://') || !Number.isFinite(age) || age > 23 * 3600 * 1000) return;
    if ([...document.querySelectorAll('audio,video')].some(media => !media.paused)) return;
    for (const video of videos) {
      const fallback = video.getAttribute('src');
      const initialTime = video.currentTime || 0;
      let restored = false;
      video.addEventListener('error', () => {
        if (restored) return;
        restored = true;
        const time = video.currentTime || 0;
        video.src = fallback;
        document.querySelectorAll('[data-source-quality]').forEach(el => {
          el.textContent = '原片预览，保留原音轨；无录屏。';
        });
        video.addEventListener('loadedmetadata', () => {
          if (!video.currentTime) video.currentTime = time;
        }, {once: true});
        video.load();
      });
      video.src = source.url;
      video.addEventListener('loadedmetadata', () => {
        if (!video.currentTime) video.currentTime = initialTime;
      }, {once: true});
      video.load();
    }
    document.querySelectorAll('[data-source-quality]').forEach(el => {
      el.textContent = '1080p 原片，保留原始音视频；无录屏。';
    });
  } catch {
    // The bundled preview keeps the comparison usable during a refresh outage.
  }
})();
