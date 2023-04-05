import os.path
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor as pool
import os
import threading
import requests
import requests.adapters
import subprocess
import re

FILE_ROOT = "/Users/chenzhuo/Desktop/CHENZHUO/windows/Billing/aaaa"
PATH_FILE_ROOT = "/Users/chenzhuo/Desktop/Standford/21days_DL/spyder/drama"
SERVER_URL = "https://cdn2.jiuse.cloud/hls/"


headers ={
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    # "Connection": "close",

}
VERIFY = True

def concat_files(video_index, output_video_name, file_list):
    input_path = os.path.join(FILE_ROOT, video_index)
    ts_file = input_path + ".txt"
    # output_video_name = os.path.join(FILE_ROOT, video_index + ".mp4")
    with open(ts_file, "w+") as f:
        for d in file_list:
            f.write("file " + input_path + "/" + d + "\n")

    ffmpeg = os.path.join(FILE_ROOT, "ffmpeg")
    cmd = f"{ffmpeg} -f concat -safe 0 -i {ts_file} -c copy {output_video_name}"
    print(cmd)
    subprocess.call(cmd, shell=True)
    # os.system(cmd)
    return


def download_slice(zip_index):
    total_index, TS_filename = zip_index
    curr_thread = threading.currentThread().name.split("-")[-1]
    time_start = time.time()
    response = requests.get(os.path.join(video_URL, TS_filename), headers=headers, verify=VERIFY)
    time.sleep(2)
    data = response.content
    status = response.status_code
    time_end = time.time()
    t_name = int(TS_filename.split(".")[0][5:]) + 1
    print(f"{t_name}/{total_index}", "status", status, "used", f"{time_end - time_start:.2f}s", "on", curr_thread)

    if status == 200:
        with open(os.path.join(FILE_ROOT, video_index, TS_filename), mode='wb+') as f:
            f.write(data)
        time.sleep(1)

    elif status == 503:
        print(TS_filename, "re-download")
        download_slice(zip_index)
    else:
        raise f"{status} error"


def url_to_index(url):
    response = requests.get(url, verify=VERIFY)
    time.sleep(2)
    response = response.content.decode('utf-8')
    soup = BeautifulSoup(response, 'html.parser')

    label_index = soup.findAll('video')
    data_src = label_index[0]["data-src"]

    video_index = None
    if "index.m3u8" in data_src:
        video_index = data_src.split("/")[4]
    else:
        raise "index error"

    label_title = soup.findAll('h4')[0].contents[0]

    return video_index, data_src, label_title


def get_all_file_index(url):
    response = requests.get(data_src, verify=VERIFY)
    time.sleep(2)
    response = response.content.decode('utf-8').split("\n")
    ts_index_list = [i for i in response if i.endswith(".ts")]
    return ts_index_list


def get_url_from_file():
    file = os.path.join(PATH_FILE_ROOT, "path_file.txt")
    f = open(file, "r")
    temp = f.readlines()
    f.close()

    temp = [temp[i].strip() for i in range(len(temp))]
    if temp:
        print("download waiting list:")
    for i, t in enumerate(temp):
        print(i + 1, t)
    if temp:
        return temp.pop(0)
    print("download finished. exit.")
    exit(0)


def pop_url_from_file(addin=None):
    file = os.path.join(PATH_FILE_ROOT, "path_file.txt")
    f = open(file, "r")
    temp = f.readlines()
    temp = [temp[i].strip() for i in range(len(temp))]
    if addin:
        temp += addin
        print("page parsed url added")
    if temp:
        temp.pop(0)
    f = open(file, "w+")
    f.seek(0)
    f.write("\n".join(temp))
    f.close()


def handle_first_url_from_file(url):
    return url.split("/")[3] != "video"


def parse_page(url):
    response = requests.get(url, verify=VERIFY)
    time.sleep(2)
    response = response.content.decode('utf-8')
    soup = BeautifulSoup(response, 'html.parser')

    all_a = soup.findAll('a')
    next_page = soup.find_all("a", {"class": "page-link"})
    print(next_page)
    url_list = set()
    for a in all_a:
        href = a.get('href')
        temp = ["/video/view/"]
        for t in temp:
            if href and href.startswith(t):
                url_list.add("https://j20t.9s117.xyz" + href)
    if next_page:
        href = next_page[-1].get("href")
        url_list.add("https://j20t.9s117.xyz" + href)
    return list(url_list)


if __name__ == "__main__":

    while True:
        # not sure if works
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False

        url = get_url_from_file()
        time.sleep(2)

        page = handle_first_url_from_file(url)
        if page:
            url_list = parse_page(url)
            # for i, u in enumerate(url_list):
            #     print(i, u)
            # break
            pop_url_from_file(url_list)
            time.sleep(2)
            continue
        time_start_total = time.time()
        video_index, data_src, label_title = url_to_index(url)
        print("video_index", video_index, "\ndata_src", data_src, "\nlabel_title", label_title)
        # break

        video_URL = SERVER_URL + video_index
        print("video_URL", video_URL)
        download_videos_path = os.path.join(FILE_ROOT, video_index)
        print("download_videos_path", download_videos_path, end=" ")

        output_video_name = os.path.join(FILE_ROOT, video_index + "_" + label_title + ".mp4")
        out_video_slice_folder = os.path.join(FILE_ROOT, video_index)
        if not os.path.isfile(output_video_name) and not os.path.exists(out_video_slice_folder):
            os.makedirs(download_videos_path)
            print("created")
        else:
            print("already exists")
            pop_url_from_file()
            continue
        file_list = get_all_file_index(data_src)
        file_list_len = len(file_list)
        if file_list_len < 20:
            continue
        total_len = [file_list_len for _ in range(file_list_len)]

        print(f"totally there are {file_list_len} ts files")
        pl = pool(max_workers=8)
        pl.map(download_slice, list(zip(total_len, file_list)))
        pl.shutdown()

        concat_files(video_index, output_video_name, file_list)
        pop_url_from_file()
        os.system("rm -rf " + download_videos_path)
        os.system("rm -f " + FILE_ROOT + "/" + video_index + ".txt")
        time_end_total = time.time()
        print(video_index, f"download done, total cost {time_end_total - time_start_total}")


