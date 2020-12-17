import os, json, time, requests
from bs4 import BeautifulSoup
import concurrent.futures as cf


class WallpaperDownloader(object):
    def __init__(self):
        self.site = 'https://wallpaperscraft.com'
        self.server = 'https://images.wallpaperscraft.com/image/'
        self.proxies = None
        self.proxy()

    def proxy(self):
        print('='*30)
        print('是否开启网络代理：')
        print('1> 是 (如果你有VPN推荐选择是)')
        print('0> 否 (默认)')
        p = input('请输入你的选择：(默认不开启) ')
        if p:
            ip = input('请输入代理主机号：(默认：127.0.0.1) ')
            pt = input('请输入代理端口号：(默认：41091) ')
            ip = ip if ip else '127.0.0.1'
            pt = pt if pt else '41091'
            self.proxies = {
                "http": f"http://{ip}:{pt}",
                "https": f"http://{ip}:{pt}"
            }
        else:
            pass

    def translate(self, query):
        url = 'http://fanyi.youdao.com/translate'
        data = {
            "i": query,  # 待翻译的字符串
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": "16081210430989",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_CLICKBUTTION"
        }
        res = requests.post(url, data=data).json()
        return res['translateResult'][0][0]['tgt']

    def get_tags(self):
        print('='*30)
        print('正在获取壁纸标签：')
        print('='*30)
        if not os.path.exists('tags.txt'):
            resp = requests.get(self.site, proxies=self.proxies)
            soup = BeautifulSoup(resp.content, 'lxml')
            tags = soup.select('div.filters>ul>li>a')
            tags_list = []
            for tag in tags:
                tag_url = self.site+tag['href']
                tag_name = self.translate(tag.contents[0].strip())
                tag_name = tag_name.replace(' ', '')
                tag_count = tag.contents[1].string
                tag_item = [tag_url, tag_name, tag_count]
                with open('tags.txt', 'a', encoding='utf-8') as f:
                    f.write(' '.join(tag_item)+'\n')
                tags_list.append(tag_item)
            self.tags = tags_list
        else:
            with open('tags.txt', encoding='utf-8') as f:
                self.tags = [line.strip().split() for line in f.readlines()]

    def get_input(self):
        print('所有标签信息如下：')
        print('='*30)
        for index, tag in enumerate(self.tags):
            print(f'{index+1:0>2}> {tag[1]} 总计{tag[2]}张')
        print('='*30)
        inp = input('请选择下载的标签：')
        print('='*30)
        choose_tag = int(inp) if inp else 5
        self.root = self.tags[choose_tag-1][1]
        os.makedirs(self.root, exist_ok=True)
        self.tag_url = self.tags[choose_tag-1][0]

    def down(self, name, link):
        if os.path.exists(name):
            pass
        else:
            r = requests.get(link, proxies=self.proxies)
            with open(name, 'wb') as f:
                f.write(r.content)

    def show(self, page_num, num, _sum,  runtime):
        barLen = 20  # 进度条的长度
        perFin = num/_sum
        numFin = round(barLen*perFin)
        numNon = barLen-numFin
        leftTime = (1-perFin)*(runtime/perFin)
        print(
            f"第{page_num}页",
            f"{num:0>{len(str(_sum))}}/{_sum}",
            f"|{'█'*numFin}{' '*numNon}|",
            f"PROCESS: {perFin*100:.0f}%",
            f"RUN: {runtime:.0f}S",
            f"ETA: {leftTime:.0f}S",
            end='\r'
        )
        if num == _sum:
            print()

    def crawl_page(self, page_num):
        page_url = f'{self.tag_url}/page{page_num}'
        resp = requests.get(page_url, proxies=self.proxies)
        soup = BeautifulSoup(resp.content, 'lxml')
        imgs = soup.select('ul.wallpapers__list>li>a')
        _sum = len(imgs)
        tp = cf.ThreadPoolExecutor(15)
        futures = []
        count = 0
        t1 = time.time()
        for item in imgs:
            url = self.site+item['href']
            resp = requests.get(url, proxies=self.proxies)
            soup = BeautifulSoup(resp.content, 'lxml')
            href = soup.select_one('span.wallpaper-table__cell>a')['href']
            link = self.server+href.replace('/download/', '').replace('/', '_')+'.jpg'
            _dir = f'{self.root}/{page_num:0>{len(str(self.total_page))}}'
            os.makedirs(_dir, exist_ok=True)
            name = f'{_dir}/{link.split("/")[-1]}'
            future = tp.submit(self.down, name, link)
            futures.append(future)
        for future in cf.as_completed(futures):
            count += 1
            t2 = time.time()
            runtime = t2-t1
            self.show(page_num, count, _sum, runtime)
        tp.shutdown()

    def main(self):
        resp = requests.get(self.tag_url, proxies=self.proxies)
        soup = BeautifulSoup(resp.content, 'lxml')
        last = soup.select('div.pager>ul.pager__list>li>a')[-1]['href']
        self.total_page = int(last.split('/')[-1].replace('page', ''))
        print(f'该标签共有{self.total_page}页图片。')
        print('='*30)
        start_page = int(input('指定起始下载页数：'))
        end_page = int(input('指定终止下载页数：'))
        print('='*30)
        sum_page = end_page-start_page+1
        for index in range(start_page, end_page+1):
            self.crawl_page(index)
        print('='*30)
        os.system('pause')


if __name__ == "__main__":
    wd = WallpaperDownloader()
    wd.get_tags()
    wd.get_input()
    wd.main()
