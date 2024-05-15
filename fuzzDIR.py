import requests
import threading
import queue
import time

# Configuration
wordlist_path = '/usr/share/wordlists/dirbuster/directory-list-1.0.txt'
target_url = 'http://54.206.178.157:8085'
output_file = 'fuzz_results.txt'
num_threads = 10  # Number of threads to use
delay = 0.1  # Delay between requests in seconds
verbose = True  # Verbose mode for detailed logging
headers = {'User-Agent': 'Mozilla/5.0'}

# Queue to hold wordlist items
q = queue.Queue()

def load_wordlist(path):
    with open(path, 'r') as file:
        for line in file:
            word = line.strip()
            if word:
                q.put(word)

def fuzz_directory():
    while not q.empty():
        directory = q.get()
        url = f"{target_url}/{directory}"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(f"[+] Found: {url}")
                with open(output_file, 'a') as f:
                    f.write(f"{url}\n")
            elif verbose:
                print(f"[-] {response.status_code} for {url}")
            time.sleep(delay)
        except requests.RequestException as e:
            print(f"[-] Error: {e}")
        q.task_done()

def main():
    load_wordlist(wordlist_path)
    print(f"[+] Loaded {q.qsize()} directories from wordlist.")

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=fuzz_directory)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("[+] Fuzzing completed.")

if __name__ == "__main__":
    main()
