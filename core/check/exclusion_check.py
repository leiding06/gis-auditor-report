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

        print(f"[DEBUG] ExclusionCheck initialized")
        print(f"[DEBUG] Exclusion ID: {config.get('exclusion_id')}")
        print(f"[DEBUG] Target ID: {config.get('target_id')}")
        print(f"[DEBUG] Target unique field: {self.target_unique_field}")
        print(f"[DEBUG] Exclusion layer found: {self.exclusion_layer is not None}")
        print(f"[DEBUG] Target layer found: {self.target_layer is not None}")
        if self.exclusion_layer:
            print(f"[DEBUG] Exclusion layer name: {self.exclusion_layer.name()}")
        if self.target_layer:
            print(f"[DEBUG] Target layer name: {self.target_layer.name()}")
            print(f"[DEBUG] Target layer fields: {self.target_layer.fields().names()}")

        
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
            print("[ERROR] Invalid target or exclusion layer")
            return self.results
            
        print(f"Running exclusion zone check on layer: {self.target_layer.name()} against {self.exclusion_layer.name()}")
        
        # Build a spatial index for the exclusion layer for efficient lookups
        exclusion_index = QgsSpatialIndex(self.exclusion_layer.getFeatures())
        errors_found = 0
        
        for target_feature in self.target_layer.getFeatures():
            target_geom = target_feature.geometry()
            
            # Get target ID - use feature ID if field not specified or invalid
            if self.target_unique_field and self.target_unique_field in self.target_layer.fields().names():
                target_id_value = target_feature[self.target_unique_field]
            else:
                target_id_value = target_feature.id()
            
            # Find exclusion features that intersect the target's bounding box
            intersecting_exclusion_ids = exclusion_index.intersects(target_geom.boundingBox())
            
            # Check for actual geometric intersection (not just bounding box)
            has_intersection = False
            for exclusion_id in intersecting_exclusion_ids:
                exclusion_feature = self.exclusion_layer.getFeature(exclusion_id)
                exclusion_geom = exclusion_feature.geometry()
                
                if target_geom.intersects(exclusion_geom):
                    has_intersection = True
                    break
            
            # If intersection found, it's an error
            if has_intersection:
                errors_found += 1
                self.results['errors'].append({
                    'target_id': target_id_value  # FIXED: was 'target_uid'
                })
        
        print(f"[DEBUG] Exclusion check complete: {errors_found} errors found")
        
        return self.results