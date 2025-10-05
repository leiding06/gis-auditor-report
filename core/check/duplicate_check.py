# gis_auditor_report/core/check/duplicate_check.py

from qgis.core import QgsProject, QgsProcessingFeedback, QgsVectorLayer

class DuplicateCheck:
    """
    Performs a check for duplicate attribute values in a specified layer and field.
    """

    def __init__(self, config: dict):
        """
        Initializes the check with a specific configuration.
        
        Args:
            config (dict): A dictionary containing the check parameters.
                           e.g., {'check_type': 'duplicate', 'layer_id': '...', 'field_name': '...'}
        """
        self.config = config
        self.layer = QgsProject.instance().mapLayer(config.get('layer_id'))
        self.field_name = config.get('field_name')

        print(f"[DEBUG] DuplicateCheck initialized")
        print(f"[DEBUG] Layer ID: {config.get('layer_id')}")
        print(f"[DEBUG] Field name: {self.field_name}")
        print(f"[DEBUG] Layer found: {self.layer is not None}")
        if self.layer:
            print(f"[DEBUG] Layer name: {self.layer.name()}")
            print(f"[DEBUG] Available fields: {self.layer.fields().names()}")
        

        self.results = {
            'check_type': 'duplicate',
            'layer_name': self.layer.name() if self.layer else 'Invalid Layer',
            'field_name':self.field_name,
            'errors': [] # To store the found duplicate values
        }
        
    def run(self) -> dict: # Define return type as dict.
        """
        Executes the duplicate check and returns a dictionary of results.
        """
        if not self.layer:
            print("[ERROR] Layer is None")
            return self.results
            
        if self.field_name not in self.layer.fields().names():
            print(f"[ERROR] Field '{self.field_name}' not found in layer")
            print(f"[ERROR] Available fields: {self.layer.fields().names()}")
            return self.results
            
        # Placeholder for the actual logic
        print(f"Running duplicate check on layer '{self.layer.name()}' for field '{self.field_name}'")
        
        
        # 1. Create a dictionary to count occurrences of each value.
        value_counts = {}
        # 2. Iterate through all features in the layer.
        for feature in self.layer.getFeatures():
        # 3. For each feature, get the value of self.field_name.
            value = feature[self.field_name]
        # 4. Count how many times each value appears.
            if value is None or value == '':
                value_str = 'NULL'
            else:
                value_str = str(value)

            value_counts[value_str] = value_counts.get(value_str, 0) + 1

        # 5. Identify values with a count > 1.
        duplicated_values = {k: v for k, v in value_counts.items() if v > 1}
        # 6. Store the results in self.results['errors'].
        for value, count in duplicated_values.items():
            self.results['errors'].append({
                'value': value, 
                'count': count
            })
        

        return self.results