from pathlib import Path
import os
import json
import traceback
from Classes.Base import Config
from Classes.Case.OsemosysClass import Osemosys
from ogcore import parameters, runner

class OGCore(Osemosys):
    def __init__(self, case):
        super().__init__(case)
        self.og_res_path = Path(Config.DATA_STORAGE, self.case, 'res', 'ogcore')
        self.og_res_path.mkdir(parents=True, exist_ok=True)

    def run_og(self, sc_name, og_spec=None):
        try:
            # Initialize specifications with default values
            # In a real scenario, we would load these from OG_Parameters.json
            p = parameters.Specifications()
            
            # Apply MUIO scenario specific updates if any
            if og_spec:
                p.update_specifications(og_spec)

            # Output path for this specific run
            run_output_path = self.og_res_path / sc_name
            run_output_path.mkdir(parents=True, exist_ok=True)

            # Run the model (using a simple local runner for now)
            # For large models, this should be moved to a background thread
            runner.runner(p, time_path=True, client=None, output_base=str(run_output_path))
            
            response = {
                "message": f"OG-Core run '{sc_name}' completed successfully!",
                "status_code": "success",
                "path": str(run_output_path)
            }
            return response
        except Exception as e:
            print(traceback.format_exc())
            return {
                "message": str(e),
                "status_code": "error"
            }

    def get_og_results(self, sc_name):
        try:
            results_path = self.og_res_path / sc_name / 'SS' / 'SS_vars.pkl'
            # In Phase 1, we just return the path or basic metadata
            # Phase 2 will involve parsing these into JSON for the frontend
            if results_path.exists():
                return {
                    "status_code": "success",
                    "results_path": str(results_path)
                }
            else:
                return {
                    "message": "Results not found",
                    "status_code": "error"
                }
        except Exception as e:
            return {
                "message": str(e),
                "status_code": "error"
            }
