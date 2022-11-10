from typing import Union, List, Optional

from idoitapi.Request import Request
from idoitapi.CMDBCategory import CMDBCategory
from idoitapi.APIException import JSONRPC
from idoitapi.utils import ip2long, long2ip


class Subnet(Request):
    """
    Special methods for subnets
    """

    def __init__(self, *args, **kwargs) -> None:
        super(self.__class__, self).__init__(*args, **kwargs)

        self.taken: List[str] = []
        """List of used IP addresses"""

        self.current: Optional[int] = None
        """Current IP address as long integer"""

        self.first: Optional[int] = None
        """First IP address in subnet as long integer"""

        self.last: Optional[int] = None
        """Last IP address in subnet as long integer"""

    def load(self, object_id: int) -> None:
        """
        Fetches some information about subnet object

        :param int object_id: Object identifier
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        category = CMDBCategory(self._api)
        net_info = category.read(object_id, 'C__CATS__NET')

        if len(net_info) != 1 or not isinstance(net_info[0], dict):
            raise JSONRPC(message='Nothing found for object identifier {}'.format(object_id))

        if net_info[0]['type']['const'] != 'C__CATS_NET_TYPE__IPV4':
            raise JSONRPC(message='Works only for IPv4')

        self.first = ip2long(net_info[0]['range_from'])
        self.last = ip2long(net_info[0]['range_to'])
        taken_ip_addresses = category.read(object_id, 'C__CATS__NET_IP_ADDRESSES')

        self.taken.extend([taken_ip_address['title'] for taken_ip_address in taken_ip_addresses])

        self.current = self.first

    def has_next(self) -> bool:
        """
        Is there a free IP address?

        :return: Is there a free IP address?
        :rtype: bool
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        if self.current is None:
            raise JSONRPC(message='You need to call method "load()" first.')

        for ip_long in range(self.current, self.last+1):
            if not self.is_used(ip_long):
                return True
        else:
            return False

    def next(self) -> Union[str, None]:
        """
        Fetches next free IP address

        :return: IPv4 address, or ``None`` if no free UP address
        :rtype: Union[str, None]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        if self.current is None:
            raise JSONRPC(message='You need to call method "load()" first.')

        for ip_long in range(self.current, self.last+1):
            self.current = ip_long

            if not self.is_used(ip_long):
                return long2ip(ip_long)
        else:
            return None

    def is_free(self, ip_address: str) -> bool:
        """
        Is IP address currently unused in subnet?

        :param str ip_address: IPv4 address
        :return: Is IP address currently unused in subnet?
        :rtype: bool
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        if self.current is None:
            raise JSONRPC(message='You need to call method "load()" first.')

        ip_long = ip2long(ip_address)

        return not self.is_used(ip_long)

    def is_used(self, long_ip: int) -> bool:
        """
        Is IP address already taken in subnet?

        :param int long_ip: IPv4 address converted to integer
        :return: Is IP address already taken in subnet?
        :rtype: bool
        """
        for taken in self.taken:
            taken_ip_long = ip2long(taken)

            if taken_ip_long == long_ip:
                return True
        else:
            return False
