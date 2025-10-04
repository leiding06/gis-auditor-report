# gis_auditor_report/core/checks/duplicate_check.py

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
        self.results = {
            'check_type': 'duplicate',
            'layer_name': self.layer.name() if self.layer else 'Invalid Layer',
            'errors': [] # To store the found duplicate values
        }
        
    def run(self):
        """
        Executes the duplicate check and returns a dictionary of results.
        """
        if not self.layer or self.field_name not in self.layer.fields().names():
            self.results['errors'].append("Invalid layer or field in configuration.")
            return self.results
            
        # Placeholder for the actual logic
        print(f"Running duplicate check on layer '{self.layer.name()}' for field '{self.field_name}'")
        
        # --- Actual logic will go here ---
        # 1. Create a dictionary to count occurrences of each value.
        # 2. Iterate through all features in the layer.
        # 3. For each feature, get the value of self.field_name.
        # 4. Count how many times each value appears.
        # 5. Identify values with a count > 1.
        # 6. Store the results in self.results['errors'].
        
        # Example of a collected result:
        # self.results['errors'].append({'value': 'A101', 'count': 2})
        
        # --- End of actual logic ---

        return self.results