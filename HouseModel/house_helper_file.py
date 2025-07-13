
class HouseHelperFile:
    def __init__(self):
        pass

    def show_starting_time_and_ending_time(self,house):
        timestamps=list(house.consumption.keys())
        if not timestamps:
            print('No consumption data available.')
            return None, None   
        return timestamps[0],timestamps[-1]