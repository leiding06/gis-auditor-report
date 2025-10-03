# gis_auditor_report/core/audit_runner.py

from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtWidgets import QProgressBar

# from .checks.duplicate_check import DuplicateCheck # To be imported later

class AuditRunner(QObject):
    """
    Main controller for the audit process. 
    Receives all check configurations, manages the progress bar, 
    dispatches checks, and generates the final report.
    """
    
    # Define a signal to notify the main dialog when all checks are finished
    finished = pyqtSignal()

    def __init__(self, all_configs: list, progress_bar: QProgressBar, parent=None):
        """Constructor. Initializes the runner with audit configurations and the progress bar."""
        super().__init__(parent)
        self.all_configs = all_configs
        self.progress_bar = progress_bar
        self.total_checks = len(all_configs)
        self.current_check_count = 0
        self.results = [] # Stores report data from each completed check
        
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
        self.finished.emit() # Emit the finished signal

    def _execute_single_check(self, config: dict):
        """Dispatches a single check configuration to the appropriate check class."""
        
        check_type = config.get('type')
        
        # TODO: Instantiate and call the check classes created in core/checks/
        
        if check_type == 'duplicate':
            # Example:
            # checker = DuplicateCheck(config)
            # check_result = checker.run()
            # self.results.append(check_result)
            print(f"Executing Duplicate Check for config: {config}")

        elif check_type == 'spatial':
            print(f"Executing Spatial Check for config: {config}")

        elif check_type == 'exclusion':
            print(f"Executing Exclusion Zone Check for config: {config}")

    def _generate_report(self):
        """Compiles the collected results into the final HTML report."""
        print("All checks completed. Generating report...")
        # Actual report generation logic goes here
        pass