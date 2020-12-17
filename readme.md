# wallpaperscraft-downloader
This is a wallpaper downloader for [https://wallpaperscraft.com/](https://wallpaperscraft.com/).
## run1.py
apply multi-thread to download each page's pictures and crawl only one page each time.
## run2.py
apply multi-thread to crawl many pages and downlaod each page's pictures in one thread.
## pack
```bash
pyinstaller -F -i favicon.ico run1.py
or
pyinstaller -F -i favicon.ico run2.py
```
## tips
you can download packed `exe` file  at the `dist` folder.