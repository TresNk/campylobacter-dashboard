import re
from collections import Counter

class LatexAnalyzer:
    """
    A class to analyze a LaTeX file and generate a report.
    This version is designed to return a list of structured findings.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.content = ""
        self.report = []

    def run_analysis(self):
        """Runs all analysis checks and returns the report."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.content = f.read()
        except FileNotFoundError:
            return [{'type': 'critical', 'title': f"File Not Found", 'details': f"The file '{self.filepath}' could not be found."}]
        except Exception as e:
            return [{'type': 'critical', 'title': "File Read Error", 'details': f"Could not read the file: {e}"}]

        self.report = []
        self._analyze_preamble()
        self._analyze_structure()
        self._analyze_formatting()
        self._analyze_model()
        return self.report

    def _add_finding(self, type, title, details=""):
        self.report.append({'type': type, 'title': title, 'details': details})

    def _analyze_preamble(self):
        packages = re.findall(r'\\usepackage(?:\[.*?\])?\{(.*?)\}', self.content)
        if 'hyperref' in packages:
            all_pkg_lines = re.findall(r'\\usepackage.*', self.content)
            if all_pkg_lines and 'hyperref' not in all_pkg_lines[-1]:
                 self._add_finding('recommendation', 'Package Order', 'The `hyperref` package should be loaded last for best compatibility.')

    def _analyze_structure(self):
        chapters = re.findall(r'\\chapter\*?\{(.*?)\}', self.content)
        self._add_finding('info', f"{len(chapters)} Chapters Found", ', '.join(chapters))

    def _analyze_formatting(self):
        forced_floats = len(re.findall(r'\\begin\{(?:figure|table)\}\[H\]', self.content))
        if forced_floats > 0:
            self._add_finding('warning', f"Found {forced_floats} '[H]' Float Specifier(s)", "Using `[H]` can cause poor page breaks. Consider using `[htbp]` instead.")
        
        typos = { "Diceased": "Deceased", "Hospitality": "Hospitalization" }
        for wrong, right in typos.items():
            if re.search(r'\b' + wrong + r'\b', self.content, re.IGNORECASE):
                self._add_finding('warning', f"Potential Typo: '{wrong}'", f"Did you mean '{right}'?")

    def _analyze_model(self):
        params = re.findall(r"(\\.+?)\s*&: (.*?)\s*\\\\", self.content)
        if params:
            param_list = "<ul>" + "".join([f"<li><code>{p[0].strip()}</code>: {p[1].strip()}</li>" for p in params]) + "</ul>"
            self._add_finding('info', f"{len(params)} Model Parameters Identified", param_list)

        r0_values = re.findall(r"R_0\s*=\s*([\d\.]+)", self.content)
        if len(set(r0_values)) > 1:
            self._add_finding('critical', 'Multiple R₀ Values Found', f"The document presents multiple distinct values for R₀, which could be confusing: {', '.join(sorted(list(set(r0_values))))}")