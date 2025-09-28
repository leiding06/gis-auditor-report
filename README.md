# GIS Auditor Report

**GIS Auditor Report** is a QGIS plugin for auditing and validating vector layers.  
It allows users to define and run a series of essential validation checks across vector layers and standalone attribute tables within a QGIS project.
It helps users identify data quality issues by checking **shared keys**, **spatial relationships**, and **duplicate values**, with results available in clear, exportable reports.

---
## ✨ Key Features

Unlike rigid, project-specific QA tools, this plugin offers flexibility through user-defined checks:

1.  **Shared Key Match:** Validate that attribute values match between a **Source Layer** (and its selected field) and a **Target Layer/Table** (and its selected field).
2.  **Spatial Relationship Check:** Test for geometric integrity (e.g., Are all features in Layer A **`within`** features in Layer B? **`intersects`**, **`touches`**, etc.).
3.  **Duplicate/Uniqueness Check:** Identify non-unique values for a selected field across a layer, helping to enforce data integrity.
4.  **Vector-to-Table Check:** Perform attribute checks against non-spatial tables (like CSV files or database views).
5.  **Actionable HTML Report:** All errors and mismatches are compiled into a clearly formatted, downloadable HTML report for easy sharing and tracking.

---

## 🚀 Getting Started

### Installation

1.  Open QGIS.
2.  Navigate to **Plugins** -> **Manage and Install Plugins...**
3.  Search for **`GIS CrossCheck Toolbox`**.
4.  Click **Install**.

### Usage

1.  Start the plugin.
2.  The main dialog will display modular sections for **Key Checks**, **Spatial Checks**, and **Uniqueness Checks**.
3.  Select your input layers, define the fields/spatial operators, and click **'Run Checks'**.
4.  An HTML report will be generated in your default download folder.

---

## 💻 For Developers & Contributors

We welcome contributions! Your current code, which includes advanced logic for archaeological cross-checks, demonstrates a high level of Python and PyQGIS expertise.

If you are interested in contributing, please check out the following areas:

* **Code Cleanup/Refactoring:** Improving the modularity of the core check functions.
* **New Checks:** Adding new check types (e.g., Value Range Checks, Topology Rules).
* **UI/UX Improvement:** Enhancing the customisation dialog for a better user experience.

### How to Contribute

1.  Fork this repository.
2.  Clone your fork: `git clone [your-fork-url]`
3.  Create a new branch for your feature or bug fix.
4.  Submit a **Pull Request (PR)** detailing your changes.

---

## 📜 License

This project is licensed under the GNU General Public License v2.0 or later (**GPL-2.0-or-later**).
