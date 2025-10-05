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


        print(f"[DEBUG] SpatialCheck initialized")
        print(f"[DEBUG] Parent ID: {config.get('parent_id')}")
        print(f"[DEBUG] Child ID: {config.get('child_id')}")
        print(f"[DEBUG] Child unique field: {self.child_unique_field}")
        print(f"[DEBUG] Parent layer found: {self.parent_layer is not None}")
        print(f"[DEBUG] Child layer found: {self.child_layer is not None}")
        if self.parent_layer:
            print(f"[DEBUG] Parent layer name: {self.parent_layer.name()}")
        if self.child_layer:
            print(f"[DEBUG] Child layer name: {self.child_layer.name()}")
            print(f"[DEBUG] Child layer fields: {self.child_layer.fields().names()}")
        
        
        self.results = {
            'check_type': 'spatial',
            'parent_layer_name': self.parent_layer.name() if self.parent_layer else 'Invalid Layer',
            'child_layer_name': self.child_layer.name() if self.child_layer else 'Invalid Layer',
            'errors': []
        }

    def run(self) -> dict:
        if not self.parent_layer or not self.child_layer:
            print("[ERROR] Invalid parent or child layer")
            return self.results
            
        print(f"Running spatial check on layers: {self.parent_layer.name()} and {self.child_layer.name()}")
        
        # Build a spatial index for the parent layer for efficient lookup
        parent_index = QgsSpatialIndex(self.parent_layer.getFeatures())
        
        errors_found = 0
        total_children = 0

        # 1. Iterate through all child features
        for child_feature in self.child_layer.getFeatures():
            child_geom = child_feature.geometry()
            child_id_value = child_feature[self.child_unique_field]
            
            # Get child ID - use feature ID if field not specified or invalid
            if self.child_unique_field and self.child_unique_field in self.child_layer.fields().names():
                child_id_value = child_feature[self.child_unique_field]
            else:
                child_id_value = child_feature.id()

            
            
            candidate_parent_ids = parent_index.intersects(child_geom.boundingBox())
            
            # Check if child is within ANY parent feature
            is_within_any_parent = False
            
            for parent_id in candidate_parent_ids:
                parent_feature = self.parent_layer.getFeature(parent_id)
                parent_geom = parent_feature.geometry()
                
                # Child is valid if it's within OR contained by the parent
                # We don't care which parent, just that there is one
                if child_geom.within(parent_geom) or parent_geom.contains(child_geom):
                    is_within_any_parent = True
                    break  # Found a valid parent, no need to check others
            
            # If child is NOT within any parent, it's an error
            if not is_within_any_parent:
                errors_found += 1
                self.results['errors'].append({
                    'child_id': child_id_value
                })
        
        print(f"[DEBUG] Spatial check complete: checked {total_children} children, {errors_found} are outside all parents")
        
        return self.results