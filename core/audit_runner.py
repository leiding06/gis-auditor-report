# gis_auditor_report/core/audit_runner.py

from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtWidgets import QProgressBar
from .check.duplicate_check import DuplicateCheck # Corrected import path
from .check.spatial_check import SpatialCheck
from .check.exclusion_check import ExclusionCheck
from .report_generator import ReportGenerator # type: ignore



class AuditRunner(QObject):
    """
    Main controller for the audit process. 
    Receives all check configurations, manages the progress bar, 
    dispatches checks, and generates the final report.
    """
    
    # Define a signal to notify the main dialog when all checks are finished
    finished = pyqtSignal()
    report_generated = pyqtSignal(str) 

    def __init__(self, all_configs: list, progress_bar: QProgressBar, report_path: str,report_config: dict, parent=None):
        super().__init__(parent)
        self.all_configs = all_configs
        self.progress_bar = progress_bar
        self.report_path = report_path
        self.total_checks = len(all_configs)
        self.current_check_count = 0
        self.report_config = report_config 
        
   
        self.results = {
            'duplicate': [],
            'spatial': [],
            'exclusion': []
        }

        
    def run_checks(self):
        """Initiates the execution of all configured checks sequentially."""
        
        if not self.all_configs:
            self.finished.emit()
            return

        self.progress_bar.setMaximum(self.total_checks)
        self.progress_bar.setValue(0)
        
        for config in self.all_configs:
            self.current_check_count += 1
            self._execute_single_check(config)
            
            # Update the progress bar to show task completion
            self.progress_bar.setValue(self.current_check_count)
            
        # All checks completed
        self._generate_report()
        self.report_generated.emit(self.report_path) 

    def _execute_single_check(self, config: dict):
        """Dispatches a single check configuration to the appropriate check class."""
        
        check_type = config.get('check_type') # Changed from 'type' to 'check_type' to match dialog
        
        if check_type == 'duplicate':
            checker = DuplicateCheck(config)
            check_result = checker.run()
            # Append the result dictionary to the correct list
            self.results['duplicate'].append(check_result)
            
        elif check_type == 'spatial':
            checker = SpatialCheck(config)
            check_result = checker.run()
            self.results['spatial'].append(check_result)


        elif check_type == 'exclusion':
            checker = ExclusionCheck(config)
            check_result = checker.run()
            self.results['exclusion'].append(check_result)

    def _generate_report(self):
        """
        Calls the ReportGenerator to compile the collected results into the final HTML report.
        """
        print("All checks completed. Generating report...")
        
        # Instantiate the ReportGenerator with the path, results, and config
        generator = ReportGenerator(self.report_path, self.results, self.report_config)
        
        # Call the method to build and save the report file
        try:
            generator.generate_report()
        except Exception as e:
            # Handle potential file writing errors
            print(f"Error generating report: {e}")
            pass