import copy
from src.exceptions.server_failure_exception import ServerFailureException
from src.driver.roku.roku_device_info import RokuDeviceInfo
from src.driver.roku.roku_media_player_info import RokuMediaPlayerInfo

class RokuInfo():
    session = None
    http_client = None

    def __init__(self, http_client, session):
        self.session = session
        self.http_client = http_client
    
    """
	Gets info about the Roku device under test such as version, power mode, etc.
	
	:returns: RokuDeviceInfo - Various information about the device under test.
	"""
    def get_device_info(self):
        session = copy.deepcopy(self.session)
        session['action'] = 'device_info'
        device_info_json = self.__handler(self.http_client.post_to_server('info', session))
        return RokuDeviceInfo(device_info_json)
    
    """
	Gets info about the Roku media player under test including buffering information, the player state, player errors, etc.
	
	:returns: RokuMediaPlayerInfo - Various information about the device media player under test.
	"""
    def get_media_player_info(self):
        session = copy.deepcopy(self.session)
        session['action'] = 'media_player_info'
        media_info_json = self.__handler(self.http_client.post_to_server('info', session))
        return RokuMediaPlayerInfo(media_info_json)

    """
	Gets the Roku debugger logs from session start to now.
	
	:returns: String - The Roku debugger logs.
	"""
    def get_debug_logs(self):
        session = copy.deepcopy(self.session)
        session['action'] = 'get_debug_logs'
        log_json = self.__handler(self.http_client.post_to_server('info', session))
        return log_json['log_content']

    def __handler(self, element_json):
        if element_json['results'] != 'success':
            raise ServerFailureException(element_json['results'])
        return element_json
