import asyncio
import json
import os

from ap_monitor import APMonitor
from logger.compositelogger import CompositeLogger
from logger.discordlogger import DiscordLogger
from logger.printlogger import PrintLogger
from tplink_switch import TpLinkSwitch


def load_ap_monitors(config, logger):
    switches = {}
    for switch_name in config['switches']:
        switch_config = config['switches'][switch_name]

        switch = TpLinkSwitch(
            name=switch_name,
            host=switch_config['host'],
            username=switch_config['username'],
            password=switch_config['password'],
        )

        switches[switch_name] = switch

    ap_monitors = {}
    for ap_name in config['ap_monitors']:
        ap_config = config['ap_monitors'][ap_name]

        mon = APMonitor(
            host=ap_config['ap_host'],
            name=ap_name,
            switch=switches[ap_config['switch']],
            switch_port=ap_config['switch_port'],
            logger=logger,
        )

        ap_monitors[ap_name] = mon

    return ap_monitors


async def main():
    print(f'ap-monitor version {os.getenv("IMAGE_VERSION")}')

    heartbeat_interval = float(os.getenv('HEARTBEAT_INTERVAL', 10))

    discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if discord_webhook_url == '':
        discord_webhook_url = None

    logger = CompositeLogger([PrintLogger()])
    if discord_webhook_url is not None:
        logger.add_logger(DiscordLogger(discord_webhook_url))

    if os.getenv('APMON_CONFIG'):
        print('APMON_CONFIG is present, loading configuration from environment variable.')
        config_str = os.getenv('APMON_CONFIG')
    else:
        print('APMON_CONFIG is absent, loading configuration from config.json (if present).')
        with open('config.json', 'r') as file:
            config_str = file.read()

    ap_monitors = load_ap_monitors(json.loads(config_str), logger)

    print(f'Heartbeat interval: {heartbeat_interval}')
    print(f'Discord webhook url: {None if discord_webhook_url is None else discord_webhook_url[:50] + "..."}')
    print(f'AP monitors: {[ap.name for ap in ap_monitors.values()]}')

    while True:
        await asyncio.sleep(heartbeat_interval)

        for ap_monitor in ap_monitors.values():
            await ap_monitor.perform_check()


if __name__ == '__main__':
    asyncio.run(main())
