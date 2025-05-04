import FlowNetwork as fn
import concurrent.futures
import time
import random
import threading

stop_processing = threading.Event()

def concurrent_loop(network,thread,stop_event):
    while not stop_event.is_set():
        #print(f"Thread {thread}: Starting task...")
        result = network.dfs('0',[],[])
        if result:
            network.update_flow(result)
        else: stop_event.set()

def run_with_thread_pool(network, num_threads):
    true_stop = True
    while true_stop:
        stop_processing.clear()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            {executor.submit(concurrent_loop,network, i, stop_processing): i for i in range(num_threads)}
        if not network.dfs('0',[],[]):  true_stop = False




if __name__ == "__main__":
    network = fn.FlowNetwork.create_from_file("testn.txt")#max flow is 416
    run_with_thread_pool(network,4)
    print(network.get_max_flow())
    print(network.find_min_cut_edges('0'))
