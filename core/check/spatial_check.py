# gis_auditor_report/core/check/spatial_check.py

from qgis.core import (
    QgsProject, 
    QgsSpatialIndex, 
)

class SpatialCheck:
    """
    Performs a hardcoded spatial relationship check between a parent and child layer.
    It checks if child features are within or contained by the parent features.
    """

    def __init__(self, config: dict):
        self.config = config
        self.parent_layer = QgsProject.instance().mapLayer(config.get('parent_id'))
        self.child_layer = QgsProject.instance().mapLayer(config.get('child_id'))
        self.child_unique_field = config.get('child_unique_field')
        
        self.results = {
            'check_type': 'spatial',
            'parent_layer_name': self.parent_layer.name() if self.parent_layer else 'Invalid Layer',
            'child_layer_name': self.child_layer.name() if self.child_layer else 'Invalid Layer',
            'errors': []
        }

    def run(self) -> dict:
        if not self.parent_layer or not self.child_layer:
            self.results['errors'].append({
                'error_message': "Invalid parent or child layer in configuration."
            })
            return self.results
            
        print(f"Running spatial check on layers: {self.parent_layer.name()} and {self.child_layer.name()}")
        
        # Build a spatial index for the parent layer for efficient lookups
        parent_index = QgsSpatialIndex(self.parent_layer.getFeatures())
        
        # 1. Iterate through all child features
        for child_feature in self.child_layer.getFeatures():
            child_geom = child_feature.geometry()
            child_id_value = child_feature[self.child_unique_field]
            
            # 2. Find all parent features that intersect the child's geometry
            parent_ids = parent_index.intersects(child_geom.boundingBox())
            
            # 3. Check if any of the intersecting parent features satisfy the relationship
            is_valid = False
            for parent_id in parent_ids:
                parent_feature = self.parent_layer.getFeature(parent_id)
                parent_geom = parent_feature.geometry()
                
                # Check both 'within' and 'contains' to maximize successful matches
                if child_geom.within(parent_geom) or parent_geom.contains(child_geom):
                    is_valid = True
                    break
            
            # 4. Report the error if no valid parent feature is found
            if not is_valid:
                self.results['errors'].append({
                    'parent_layer_name': self.parent_layer.name(),
                    'child_layer_name': self.child_layer.name(),
                    'child_uid': child_id_value,
                })
                
        return self.results