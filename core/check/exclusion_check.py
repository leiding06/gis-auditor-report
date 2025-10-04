# gis_auditor_report/core/check/exclusion_check.py

from qgis.core import (
    QgsProject, 
    QgsSpatialIndex
)

class ExclusionCheck:
    """
    Checks if features in a target layer violate a predefined exclusion zone.
    It identifies target features that intersect or touch any feature in the exclusion layer.
    """

    def __init__(self, config: dict):
        """
        Initializes the check with a specific configuration.
        
        Args:
            config (dict): A dictionary containing the check parameters.
        """
        self.config = config
        self.target_layer = QgsProject.instance().mapLayer(config.get('target_id'))
        self.exclusion_layer = QgsProject.instance().mapLayer(config.get('exclusion_id'))
        self.target_unique_field = config.get('target_unique_field')
        
        self.results = {
            'check_type': 'exclusion',
            'target_layer_name': self.target_layer.name() if self.target_layer else 'Invalid Layer',
            'exclusion_layer_name': self.exclusion_layer.name() if self.exclusion_layer else 'Invalid Layer',
            'errors': []
        }

    def run(self) -> dict:
        """
        Executes the exclusion check and returns a dictionary of results.
        """
        if not self.target_layer or not self.exclusion_layer:
            self.results['errors'].append({
                'error_message': "Invalid target or exclusion layer in configuration."
            })
            return self.results
            
        print(f"Running exclusion zone check on layer: {self.target_layer.name()} against {self.exclusion_layer.name()}")
        
        # Build a spatial index for the exclusion layer for efficient lookups
        exclusion_index = QgsSpatialIndex(self.exclusion_layer.getFeatures())
        
        # 1. Iterate through all target features
        for target_feature in self.target_layer.getFeatures():
            target_geom = target_feature.geometry()
            target_id_value = target_feature[self.target_unique_field]
            
            # 2. Find all exclusion features that intersect the target's geometry
            intersecting_exclusion_ids = exclusion_index.intersects(target_geom.boundingBox())
            
            # 3. If any intersection is found, it is an error
            if intersecting_exclusion_ids:
                
                # Report the error
                self.results['errors'].append({
                    'target_layer_name': self.target_layer.name(),
                    'target_uid': target_id_value,
                    'exclusion_layer_name': self.exclusion_layer.name(),
                })
                
        return self.results