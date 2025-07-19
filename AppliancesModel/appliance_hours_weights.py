class ApplianceHoursWeights:
    def __init__(self):
        pass

    def determine_hours_weights(self,hour_dictionary,period=365):
        hours_weights = {}
        for appliance_type, hours in hour_dictionary.items():
            hours_weights[appliance_type] = {}
            for hour,count in hours.items():
                hours_weights[appliance_type][hour] = round(count / period, 2)
        return hours_weights
