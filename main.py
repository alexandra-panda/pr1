import os
import re
import socket
import threading

import requests
import urllib3

# htons host to network short
# ntohs network to host short

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
    mysocket.connect(("me.utm.md", 80))
    mysocket.sendall(b"GET / HTTP/1.1\r\nHost: me.utm.md\r\n\r\n")

    print(str(mysocket.recv(52), 'utf-8'))


def get_url_images_in_text(source):
    # Finds image's urls
    urls = []
    results = re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg|gif)', source)

    for x in results:
        if 'http://' not in x:
            x = 'http://me.utm.md' + x
        urls.append(x)
    urls = list(set(urls))
    print('Links of images detected: ' + str(len(urls)))
    return urls


def get_images_from_url(url):
    resp = requests.get(url)
    urls = get_url_images_in_text(resp.text)
    print('\nUrls of images:\n', urls)
    return urls




def download_images(path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
        mysocket.connect(("me.utm.md", 80))
        mysocket.sendall("GET {0} HTTP/1.1\r\nHost: me.utm.md\r\nConnection: close\r\n\r\n".format(path).encode("latin1"))


        images = b''

        while True:

            data = mysocket.recv(1024)
            if not data:
                images = images.split(b"\r\n\r\n")
                if "200" not in images[0].decode("latin1"):
                    print(path)
                image_path = os.path.join(os.getcwd(), "MeImages", path.rpartition("/")[-1])
                with open(image_path, "wb") as fcont:
                    fcont.write(images[-1])
                break

            images += data
img_list = get_images_from_url('http://me.utm.md/')


thread_list = []

for i in img_list:
    t = threading.Thread(target=download_images, args=(i,))
    thread_list.append(t)
    t.start()


for i in thread_list:
    i.join()
print("Download Done")
