from tplink_api.tplink_api import TpLinkApi
from utils import is_host_reachable


class TpLinkSwitch:
    def __init__(self, name, host, username, password):
        self.name = name
        self.host = host

        self.api = TpLinkApi(
            host=host,
            port=80,
            use_ssl=False,
            user=username,
            password=password,
            verify_ssl=False,
        )

    async def set_port_enabled(self, port_number: int, enabled: bool) -> None:
        port_states = await self.api.get_port_states()
        port_state = next(filter(lambda p: p.number == port_number, port_states))

        await self.api.set_port_state(
            number=port_number,
            enabled=enabled,
            speed_config=port_state.speed_config,
            flow_control_config=port_state.flow_control_config,
        )

    async def is_reachable(self) -> bool:
        return await is_host_reachable(self.host)
