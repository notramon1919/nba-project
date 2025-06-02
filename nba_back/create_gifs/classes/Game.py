import pandas as pd

from create_gifs.classes.Event import Event
from create_gifs.classes.Team import Team


class Game:
    """A class for keeping info about the games"""
    def __init__(self, path_to_json, event_index=None, path_to_gif_folder=None):
        # self.events = None
        self.path_to_gif_folder = path_to_gif_folder
        self.home_team = None
        self.guest_team = None
        self.event = None
        self.events = None
        self.path_to_json = path_to_json
        self.event_index = event_index

    def read_json(self):
        data_frame = pd.read_json(self.path_to_json)
        last_default_index = len(data_frame) - 1
        self.event_index = min(self.event_index, last_default_index)
        index = self.event_index

        event = data_frame['events'][index]
        self.event = Event(event)
        self.home_team = Team(event['home']['teamid'])
        self.guest_team = Team(event['visitor']['teamid'])

    def save(self):
        self.event.save(save_path=self.path_to_gif_folder)

    def get_events(self):
        data_frame = pd.read_json(self.path_to_json)
        self.events = data_frame["events"]
        return self.events