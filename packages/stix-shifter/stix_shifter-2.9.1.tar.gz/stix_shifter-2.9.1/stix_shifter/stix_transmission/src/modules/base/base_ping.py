from abc import ABCMeta, abstractmethod


class BasePing(object, metaclass=ABCMeta):
    @abstractmethod
    def ping(self):
        """
        Sends a basic request to the datasource to confirm we are connected and authenticated

        Args:
            search_id (str): The datasource query ID.

        Returns:
            dict: The return value.
                keys:
                    success (bool): True or False
                    error (str): error message (when success=False)
        """
        pass
