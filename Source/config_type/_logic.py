class base_type:
    '''
    This is a base class meant to encapsulate some configuration metadata.
    It could be accessed by classes in the `game_config` module.
    '''

    def __init__(self, data_dict: dict, base_dir: str) -> None:
        self.base_dir = base_dir
        self.data_dict = data_dict
