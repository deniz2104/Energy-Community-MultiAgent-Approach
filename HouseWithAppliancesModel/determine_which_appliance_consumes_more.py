import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.cluster import KMeans
from .house_with_appliances import HouseWithAppliancesConsumption

class DetermineWhichApplianceConsumesMore:
    def __init__(self) -> None:
        self.top_threshold = 20
        self.number_of_clusters = 2
        self.random_state = 42
        
    def _sigmoid(self, x: np.ndarray) -> np.ndarray: return 1 / (1 + np.exp(-x))

    def _determine_sigmoid_values(self, all_consumption_values: np.ndarray) -> np.ndarray:
        scaler = MinMaxScaler(feature_range=(-1, 1))
        all_consumption_values = scaler.fit_transform(all_consumption_values.reshape(-1, 1)).flatten()
        return self._sigmoid(all_consumption_values)

    def _label_house_appliances_with_Kmeans(self,sigmoid_values: np.ndarray) -> tuple[StandardScaler, KMeans, np.ndarray]:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(sigmoid_values.reshape(-1, 1))

        kmeans = KMeans(n_clusters=self.number_of_clusters, random_state=self.random_state, n_init=50)
        kmeans.fit(scaled_data)

        centroids = scaler.inverse_transform(kmeans.cluster_centers_)
        return scaler, kmeans, centroids

    def _gather_consumption_values_for_each_appliance(self, house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, np.ndarray]:
        consumption_values :dict[str, np.ndarray] = {}
        for appliance_name, consumption in house_with_appliances.appliance_consumption.items():
            values = np.array([value for _, value in consumption])
            consumption_values[appliance_name] = np.unique(np.trim_zeros(np.sort(values)))
        return consumption_values

    def eliminate_off_values_from_each_appliance(self, house_with_appliances: HouseWithAppliancesConsumption, off_consumption_values: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
        consumption_values = self._gather_consumption_values_for_each_appliance(house_with_appliances)
        for appliance_name, values in consumption_values.items():
            if appliance_name in off_consumption_values:
                off_values_per_appliance = off_consumption_values[appliance_name]
                mask = ~np.isin(values, off_values_per_appliance)
                consumption_values[appliance_name] = values[mask]
        return consumption_values

    def determine_sigmoid_values_for_each_appliance(self, consumption_values: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
        sigmoid_values :dict[str, np.ndarray] = {}
        for appliance_name, values in consumption_values.items():
            scaled_values = MinMaxScaler(feature_range=(-1, 1)).fit_transform(values.reshape(-1, 1)).flatten()
            sigmoid_values[appliance_name] = self._sigmoid(scaled_values)
        return sigmoid_values

    def gather_labels_and_counts(self, house_with_appliances: HouseWithAppliancesConsumption, off_values: dict[str, np.ndarray]) -> tuple[list[str], dict]:
        """
        Gather histogram bins and counts for sigmoid values distribution.
        
        The sigmoid values distribution is observed to be similar to a Gaussian curve.
        To identify dominant appliances, we remove labels up to 20% of the total,
        ensuring we focus on active values.
        
        Goal: Determine a threshold for each house using K-means, removing active values
        to better predict the threshold considering nearby values determined after sigmoid transformation.
        
        Args:
            house_with_appliances: House consumption data object
            off_values: Dictionary of off values per appliance
            
        Returns:
            tuple: (bin_labels, counts_per_appliance) for the sigmoid distribution histogram
        """
        all_consumption_values = self.eliminate_off_values_from_each_appliance(house_with_appliances, off_values)
        sigmoid_values = self.determine_sigmoid_values_for_each_appliance(all_consumption_values)
        
        bin_edges = np.arange(0.2, 0.9, 0.1)
        bin_labels = [f"{edge:.1f}-{edge+0.1:.1f}" for edge in bin_edges[:-1]]

        counts :dict[str, np.ndarray] = {}
        for appliance_name, values in sigmoid_values.items():
            counts[appliance_name], _ = np.histogram(values, bins=bin_edges)
        return bin_labels, counts

    def plot_sigmoid_distribution_bins(self, house_with_appliances: HouseWithAppliancesConsumption, off_values: dict[str, np.ndarray]) -> None:
        bin_labels, counts = self.gather_labels_and_counts(house_with_appliances, off_values)
        go.Figure(data=[go.Bar(x=bin_labels, y=counts)]).show()

    def _delete_big_value_labels_from_bins(self, house_with_appliances: HouseWithAppliancesConsumption, sigmoid_values: dict[str, np.ndarray], off_values) -> tuple[list[str], dict]:
        bin_labels, counts = self.gather_labels_and_counts(house_with_appliances, off_values)
        
        # Calculate total values across all bins
        total_values = sum(len(values) for values in sigmoid_values.values())
        
        # Find which bins to remove (top 20% of values)
        bins_to_remove:list[str] = []
        cumulative_percentage = 0
        
        for i in reversed(range(len(bin_labels))):
            bin_total = sum(counts[appliance][i] for appliance in counts)
            percentage = (bin_total / total_values) * 100
            
            if cumulative_percentage + percentage <= self.top_threshold:
                bins_to_remove.append(bin_labels[i])
                cumulative_percentage += percentage
            else:
                break

        filtered_labels = [label for label in bin_labels if label not in bins_to_remove]
        filtered_counts:dict[str,np.ndarray] = {}
        
        for appliance in counts:
            filtered_counts[appliance] = [
                counts[appliance][i] for i, label in enumerate(bin_labels) 
                if label not in bins_to_remove
            ]
        
        return filtered_labels, filtered_counts

    def _determine_top_margin_for_sigmoid(self, house_with_appliances: HouseWithAppliancesConsumption, sigmoid_values: dict[str, np.ndarray], off_values) -> dict[str, np.ndarray]:
        bin_labels, _ = self._delete_big_value_labels_from_bins(house_with_appliances, sigmoid_values, off_values)
        top_margin = float(bin_labels[-1].split("-")[1])

        filtered_sigmoid_values:dict[str, np.ndarray] = {}
        for appliance_name, values in sigmoid_values.items():
            filtered_values = np.array([value for value in values if value <= top_margin])
            filtered_sigmoid_values[appliance_name] = filtered_values

        return filtered_sigmoid_values
    
    def _filter_by_cluster(self, data: np.ndarray, kmeans: KMeans, scaler: StandardScaler, label: int) -> np.ndarray:
        return np.array([value for value in data if kmeans.predict(scaler.transform([[value]]))[0] == label])

    def _determine_pairs_of_active_and_inactive(self, sigmoid_values: np.ndarray) -> tuple[list[float], list[float]]:
        scaler, kmeans, centroids = self._label_house_appliances_with_Kmeans(sigmoid_values)
        
        off_label = np.argmin(centroids)
        on_label = np.argmax(centroids)

        off_pairs, on_pairs = [], []
        off_pairs.extend(self._filter_by_cluster(sigmoid_values, kmeans, scaler, off_label))
        on_pairs.extend(self._filter_by_cluster(sigmoid_values, kmeans, scaler, on_label))
        
        return off_pairs, on_pairs


    def determine_threshold(self, house_with_appliances: HouseWithAppliancesConsumption, off_values: dict[str, np.ndarray] = None) -> dict[str, float]:        
        all_consumption_values = self.eliminate_off_values_from_each_appliance(house_with_appliances, off_values)
        
        sigmoid_values_per_appliance = self.determine_sigmoid_values_for_each_appliance(all_consumption_values)
        
        filtered_sigmoid_values = self._determine_top_margin_for_sigmoid(house_with_appliances, sigmoid_values_per_appliance, off_values)
        
        thresholds_per_appliance:dict[str,float] = {}
        for appliance_name, appliance_sigmoid_values in filtered_sigmoid_values.items():
            off_pairs, _ = self._determine_pairs_of_active_and_inactive(appliance_sigmoid_values)
            off_values_from_off_pairs, _ = self._determine_pairs_of_active_and_inactive(np.array(off_pairs))
            thresholds_per_appliance[appliance_name] = off_values_from_off_pairs[-1]
        
        return thresholds_per_appliance