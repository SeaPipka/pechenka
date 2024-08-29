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
	try:
		with open(txt, "r", encoding="utf-8", errors="ignore") as f:	
			for line in f.readlines():
				cline = line.strip().split()
				if len(cline) == 7:
					if "github" in cline[0]: # Если нашли нужный сайт.
						if cline[5] == "user_session": # Поиск нужной куки
							print(cline, txt)
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
		print(f"In Progress: [{total}/{i}]", end="\r")
		read_cookie(txt)

	print(f'Работа окончена!\nВремя затраченное на работу {round(time() - start, 2)}s')


	# txt = r'C:\Users\ADMIN\Downloads\Telegram Desktop\fatetraffic\AE[D7B474802AE000AF42976DCC4DCCB402] [2024-08-28T20_36_12.0267380+03_00]\Cookies\Google_[Chrome]_Default Network.txt'

	# with open(txt, "r" ) as f:	
	# 	for line in f.readlines():
	# 		cline = line.strip().split()
	# 		if len(cline) == 7:
	# 			if "wallets" in cline[0]:
	# 				print(cline)
