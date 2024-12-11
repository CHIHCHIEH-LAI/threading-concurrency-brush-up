import threading
import queue
import time

NUM_AGENTS = 5  # Number of crawler agents

# Shared resources
to_visit_list = queue.Queue()  # URLs waiting to be visited
visited_record = set()  # URLs that have been visited

# Locks to protect shared resources
queue_lock = threading.Lock()
visited_lock = threading.Lock()


def get_links_from_page(url):
    """
    Simulated function to get links from a web page.
    In a real-world application, this function would fetch the page and extract the links.
    For the sake of demonstration, we just return a few dummy links.
    """
    return ["link1", "link2", "link3", "link4", "link5"]


def crawler_agent():
    while True:
        url = None

        # Try to get a URL from the queue
        with queue_lock:
            if not to_visit_list.empty():
                url = to_visit_list.get()

        if not url:
            break  # No more URLs to visit, exit the loop

        # Check if the URL has been visited
        with visited_lock:
            if url in visited_record:
                continue  # URL has been visited, skip it

            # Mark the URL as visited
            visited_record.add(url)

        # Simulate processing the page
        print(f"Processing: {url}")
        time.sleep(1)  # Pretend it takes 1 second to process a page

        # Get links from the page and add them to the queue
        links = get_links_from_page(url)
        with queue_lock:
            for link in links:
                if link not in visited_record:
                    to_visit_list.put(link)  # Add only new links


def main():
    # Seed the to_visit_list with an initial URL
    to_visit_list.put("http://example.com")

    # Create crawler agents
    agents = []
    for _ in range(NUM_AGENTS):
        agent = threading.Thread(target=crawler_agent)
        agent.start()
        agents.append(agent)

    # Wait for all crawler agents to finish
    for agent in agents:
        agent.join()

    print("Crawling finished.")


if __name__ == "__main__":
    main()
