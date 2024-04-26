import aioping


async def is_host_reachable(host: str, timeout: float = 1.0, retries: int = 3):
    for i in range(retries):
        try:
            await aioping.ping(host, timeout)
            return True
        except:
            print(f'[ping] {host} is unreachable (try {i + 1} of {retries})')
            continue

    return False
