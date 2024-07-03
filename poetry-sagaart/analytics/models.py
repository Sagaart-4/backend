import numpy as np


class Data:
    def __init__(
        self,
        category=np.NaN,
        year=np.NaN,
        height=np.NaN,
        width=np.NaN,
        work_material=np.NaN,
        pad_material=np.NaN,
        count_title=np.NaN,
        count_artist=np.NaN,
        country=np.NaN,
        sex=np.NaN,
        solo_shows=np.NaN,
        group_shows=np.NaN,
        age=np.NaN,
        is_alive=np.NaN,
    ):
        self.category = category
        self.year = year
        self.height = height
        self.width = width
        self.work_material = work_material
        self.pad_material = pad_material
        self.count_title = count_title
        self.count_artist = count_artist
        self.country = country
        self.sex = sex
        self.solo_shows = solo_shows
        self.group_shows = group_shows
        self.age = age
        self.is_alive = is_alive

    def art_data(self):
        return [
            self.category,
            self.year,
            self.height,
            self.width,
            self.work_material,
            self.pad_material,
            self.count_title,
            self.count_artist,
            self.country,
            self.sex,
            self.solo_shows,
            self.group_shows,
            self.age,
            self.is_alive,
        ]
