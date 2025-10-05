# GIS Auditor Report

A powerful and user-friendly QA/QC plugin for validating vector data in QGIS. Configure duplicate, spatial, and exclusion-zone checks via a simple interface. Generate HTML reports, which can also be exported to PDF using your browser's print feature.

---

## Key Features

Unlike rigid, project-specific QA tools, this plugin offers flexibility through user-defined checks:

Flexible Check Selection: Freely add or remove validation checks—you only run what you need, for each project.

Section 1: Duplicate Value Check: Detect non-unique attribute values in any layer.

Section 2: Spatial Relationship Check: Ensure child features (e.g., points) follow rules relative to parent features (e.g., polygons).

Section 3: Exclusion Zone Check: Detect target features violating restricted areas.

Automated Report Details: Every HTML report includes the generation timestamp and operator name, making results traceable and auditable.

Instant HTML Report: Generate and share a clean report immediately after running your checks. PDF format available in browser - Print to PDF.

---
![HTML Report Snapshot](https://github.com/leiding06/gis-auditor-report/blob/main/public/sample_output/git_auditor_report_layout.png)

![Report Layout](https://github.com/leiding06/gis-auditor-report/blob/main/public/sample_output/gis_auditor_report_html_snapshot.png)
## Getting Started

### Installation

1.  Open QGIS.
2.  Navigate to **Plugins** -> **Manage and Install Plugins...**
3.  Search for **`GIS Auditor Report`**.
4.  Click **Install**.

### Usage

1.  Start the plugin.
2.  The main dialog will display modular sections for **Key Checks**, **Spatial Checks**, and **Uniqueness Checks**.
3.  Select your input layers, define the fields/spatial operators, and click **'Run Checks'**.
4.  An HTML report will be generated in your default download folder.

---

## For Developers & Contributors

Welcome contributions!

If you are interested in contributing, please check out the following areas:

- **Code Cleanup/Refactoring:** Improving the modularity of the core check functions.
- **New Checks:** Adding new check types (e.g., Value Range Checks, Topology Rules).
- **UI/UX Improvement:** Enhancing the customisation dialog for a better user experience.

### How to Contribute

1.  Fork this repository.
2.  Clone your fork
3.  Create a new branch for your feature or bug fix.
4.  Submit a **Pull Request (PR)** detailing your changes.

---

## License

This project is licensed under the GNU General Public License v2.0 or later (**GPL-2.0-or-later**).
