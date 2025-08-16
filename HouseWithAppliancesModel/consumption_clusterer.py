import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from .house_with_appliances import HouseWithAppliancesConsumption
from .consumption_data_processor import ConsumptionDataProcessor
from .sigmoid_analyzer import SigmoidAnalyzer

class ConsumptionClusterer:
    def __init__(self) -> None:
        self.number_of_clusters = 2
        self.random_state = 42
        self._data_processor = ConsumptionDataProcessor()
        self._sigmoid_analyzer = SigmoidAnalyzer()

    def _label_house_appliances_with_Kmeans(self, sigmoid_values: np.ndarray) -> tuple[StandardScaler, KMeans, np.ndarray]:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(sigmoid_values.reshape(-1, 1))

        kmeans = KMeans(n_clusters=self.number_of_clusters, random_state=self.random_state, n_init=50)
        kmeans.fit(scaled_data)

        centroids = scaler.inverse_transform(kmeans.cluster_centers_)
        return scaler, kmeans, centroids

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
        """Calculate consumption thresholds for each appliance using clustering analysis."""        
        all_consumption_values = self._data_processor.eliminate_off_values_from_each_appliance(house_with_appliances, off_values)
        
        sigmoid_values_per_appliance = self._data_processor.determine_sigmoid_values_for_each_appliance(all_consumption_values)

        filtered_sigmoid_values = self._sigmoid_analyzer.determine_top_margin_for_sigmoid(sigmoid_values_per_appliance)

        thresholds_per_appliance: dict[str, float] = {}
        for appliance_name, appliance_sigmoid_values in filtered_sigmoid_values.items():
            off_pairs, _ = self._determine_pairs_of_active_and_inactive(appliance_sigmoid_values)
            off_values_from_off_pairs, _ = self._determine_pairs_of_active_and_inactive(np.array(off_pairs))
            thresholds_per_appliance[appliance_name] = off_values_from_off_pairs[-1]
        
        return thresholds_per_appliance
