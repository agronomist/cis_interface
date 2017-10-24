import uuid
from cis_interface.drivers.ConnectionDriver import ConnectionDriver


class ServerResponseDriver(ConnectionDriver):
    r"""Class for handling server side RPC type communication.

    Args:
        model_response_name (str): The name of the channel used by the server
            model to send responses to requests.
        model_response_address (str): The address of the channel used by the
            server model to send responses to requests.
        response_address (str): The address of the channel used to send
            responses to the client response driver.
        comm (str, optional): The comm class that should be used to
            communicate with the server resposne driver. Defaults to
            _default_comm.
        **kwargs: Additional keyword arguments are passed to parent class.

    Attributes:
        comm (str): The comm class that should be used to communicate
            with the server driver. Defaults to _default_comm.

    """

    def __init__(self, model_response_name, model_response_address,
                 response_address, comm=None, **kwargs):
        response_name = 'ServerResponse.%s' % str(uuid.uuid4())
        # Input communicator from client model
        icomm_kws = kwargs.get('icomm_kws', {})
        icomm_kws['comm'] = None
        icomm_kws['name'] = model_response_name
        icomm_kws['address'] = model_response_address
        kwargs['icomm_kws'] = icomm_kws
        # Output communicator to client response driver
        ocomm_kws = kwargs.get('ocomm_kws', {})
        ocomm_kws['comm'] = comm
        ocomm_kws['name'] = response_name
        ocomm_kws['address'] = response_address
        kwargs['ocomm_kws'] = ocomm_kws
        super(ServerResponseDriver, self).__init__(response_name, **kwargs)
        assert(not hasattr(self, 'comm'))
        self.comm = comm
        self._unused = True
        # print 80*'='
        # print self.__class__
        # print self.env
        # print self.icomm.name, self.icomm.address
        # print self.ocomm.name, self.ocomm.address
        
    @property
    def is_valid(self):
        r"""bool: Returns True if the connection is unused and the parent class
        is valid."""
        with self.lock:
            return (super(ConnectionDriver, self).is_valid and self._unused)

    @property
    def model_response_name(self):
        r"""str: The name of the channel used by the server model to send
        responses."""
        return self.icomm.name

    @property
    def model_response_address(self):
        r"""str: The address of the channel used by the server model to send
        responses."""
        return self.icomm.address
    
    @property
    def response_name(self):
        r"""str: The name of the channel used to send responses to the client
        response driver."""
        return self.ocomm.name
    
    @property
    def response_address(self):
        r"""str: The address of the channel used to send responses to the client
        response driver."""
        return self.ocomm.address

    def send_message(self, *args, **kwargs):
        r"""Set comm to used and then send the message.

        Args:
            *args: Arguments are passed to parent class send_message.
            *kwargs: Keyword arguments are passed to parent class send_message.

        Returns:
            bool: Success or failure of send.

        """
        self._unused = False
        super(ServerResponseDriver, self).send_message(*args, **kwargs)
