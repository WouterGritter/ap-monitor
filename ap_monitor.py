from typing import Optional

from logger.logger import Logger
from tplink_switch import TpLinkSwitch
from utils import is_host_reachable


class APMonitor:
    def __init__(self, host: str, name: str, switch: TpLinkSwitch, switch_port: int, logger: Logger):
        self.host = host
        self.name = name
        self.switch = switch
        self.switch_port = switch_port
        self.logger = logger

        self.switch_port_disabled = False

    async def perform_check(self):
        if not await self.switch.is_reachable():
            return

        reachable = await self.is_reachable()
        if reachable:
            if self.switch_port_disabled:
                self._log(f'AP is reachable again after disabling switch port. '
                      f'Assuming anomaly has been fixed and the port has been enabled manually.')
                self.switch_port_disabled = False
        else:
            if not self.switch_port_disabled:
                self._log(f'AP is not reachable. Assuming someone has tampered with the AP connection. '
                          f'Disabling switch port #{self.switch_port} on switch {self.switch.name}. '
                          f'When the issue has been resolved, please enable the port manually in the switch '
                          f'to allow the AP to function again.')

                try:
                    await self.switch.set_port_enabled(self.switch_port, False)
                    self.switch_port_disabled = True
                except Exception as e:
                    self._log(f'An exception occurred when attempting to disable the port. Retrying on next check. {e}')

    async def attempt_recovery(self):
        if not await self.switch.is_reachable():
            return

        self._log('Attempting recovery.')

        await self.switch.set_port_enabled(self.switch_port, True)

        reachable = await self.is_reachable(30)
        if reachable:
            self._log('Recovery successful, AP is reachable again.')
            self.switch_port_disabled = False
        else:
            self._log('Recovery unsuccessful. AP is not reachable after enabling port.')
            await self.switch.set_port_enabled(self.switch_port, False)
            self.switch_port_disabled = True

    def _log(self, text: str):
        self.logger.log(f'[{self.name}@{self.host}] {text}')

    async def is_reachable(self, retries: Optional[int] = None):
        if retries is None:
            return await is_host_reachable(self.host)
        else:
            return await is_host_reachable(self.host, retries=retries)
