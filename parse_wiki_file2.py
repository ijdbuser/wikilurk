import re
import json
import threading
from queue import Queue
import time
from libzim import Archive, Entry, Item

MAX_THREADS = 10
ENTRY_COUNT = 10000

zim = Archive("wiki.zim")
print(zim.entry_count)

def extract_links(content):
    # Regex pattern to find wiki-style links [[Link|Description]]
    pattern = re.compile(r'<a href="(\w+?)" title=".+?">')
    links = pattern.findall(content)
    for i in range (0, len(links)):
        link:str = links[i]
        links[i] = link.replace('"', "'")
    return links

def worker(queue, articles):
    while True:
        entry_id = queue.get()
        if entry_id is None:  # Stop signal
            break
        try:
            entry: Entry = zim._get_entry_by_id(entry_id)
            item: Item = entry.get_item()
            if not item.path.startswith('A/') or not item.path or not item.title or item.title == "":
                continue
            content = bytes(item.content).decode()
            path = item.path.replace('"', "'")[2:]
            new_links = extract_links(content)
            if path in articles:
                articles[path]['links'] = list(set(articles[path]['links'] + new_links))
            else:
                articles[path] = {
                    'title': item.title.replace('"', "'"),
                    'links': list(set(new_links)),
                }
        except Exception as e:
            print(f"Error processing entry {entry_id}: {e}")
        finally:
            queue.task_done()


start_time = time.time()

queue = Queue()
articles = {}

threads = []
for i in range(MAX_THREADS):
    thread = threading.Thread(target=worker, args=(queue, articles))
    thread.start()
    threads.append(thread)

# Enqueue entries to process
for i in range(ENTRY_COUNT):
    queue.put(i)



# Wait for all tasks to be completed
queue.join()

# Stop workers
for i in range(MAX_THREADS):
    queue.put(None)  # Send stop signal to workers
for thread in threads:
    thread.join()

with open("data.json", "w") as data:
    json.dump(articles, data, indent=4)

end_time = time.time()

duration = end_time - start_time
print(f"Processing complete. Time taken: {duration:.2f} seconds.")
