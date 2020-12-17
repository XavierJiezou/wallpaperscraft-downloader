# wallpaperscraft-downloader
This is a wallpaper downloader for [https://wallpaperscraft.com/](https://wallpaperscraft.com/).
## demo
![demo](demo.gif)
## run1.py
Apply multi-thread to download each page's pictures and crawl only one page each time.
## run2.py
Apply multi-thread to crawl many pages and downlaod each page's pictures in one thread.
## pack
```bash
pyinstaller -F -i favicon.ico run1.py
or
pyinstaller -F -i favicon.ico run2.py
```
## tips
You can download packed `exe` file  at the `dist` folder.