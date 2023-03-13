from typing import List, Dict, Optional

from idoitapi.Console.Console import Console


class Import(Console):
    """
    Requests for API namespace 'console.import'
    """

    def import_from_csv_file(self, options: Optional[Dict] = None) -> List[str]:
        """
        Import data from CSV file located on i-doit host

        :param dict options: Options
        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.import.csv',
            options
        )

    def list_csv_import_profiles(self) -> List[str]:
        """
        List available CSV import profiles

        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.import.csvprofiles'
        )

    def import_from_inventory(self, options: Optional[Dict] = None) -> List[str]:
        """
        Import data from h-inventory output file located on i-doit host

        :param dict options: Options
        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.import.hinventory',
            options
        )

    def import_from_jdisc_discovery(self, options: Optional[Dict] = None) -> List[str]:
        """
        Import data from JDisc Discovery instance

        :param dict options: Options
        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.import.jdisc',
            options
        )

    def trigger_jdisc_discovery(self, options: Optional[Dict] = None) -> List[str]:
        """
        Trigger discovery job on JDisc Discovery instance

        :param dict options: Options
        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.import.jdiscdiscovery',
            options
        )

    def import_from_ocs_inventory_ng(self, options: Optional[Dict] = None) -> List[str]:
        """
        Import data from OCS Inventory NG instance

        :param dict options: Options
        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.import.ocs',
            options
        )

    def import_from_syslog(self, options: Optional[Dict] = None) -> List[str]:
        """
        Import data from syslog

        :param dict options: Options
        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.import.syslog',
            options
        )

    def import_from_xml_file(self, options: Optional[Dict] = None) -> List[str]:
        """
        Import data from XML file located on i-doit host

        :param dict options: Options
        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.import.xml',
            options
        )
