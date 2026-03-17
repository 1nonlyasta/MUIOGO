from pathlib import Path
import pandas as pd
import json
from Classes.Base import Config

class Exchange:
    def __init__(self, case):
        self.case = case
        self.case_path = Path(Config.DATA_STORAGE, case)
        
    def clews_to_ogcore(self, caserunname):
        """
        Extracts results from CLEWS (OSEMOSYS) and transforms them into 
        shocks for OG-Core.
        """
        try:
            # Path to CLEWS CSV results
            clews_res_path = self.case_path / 'res' / caserunname / 'csv'
            
            # 1. Extract: Load energy cost data
            cost_file = clews_res_path / 'TotalDiscountedCost.csv'
            if cost_file.exists():
                df = pd.read_csv(cost_file)
                # Aggregate total cost per year
                annual_cost = df.groupby('y')['v'].sum()
                
                # 2. Transform: High costs -> Lower productivity growth (g_y)
                # Simple linear mapping for demonstration: 
                # g_y_new = g_y_default * (1 - (cost / cost_threshold))
                cost_threshold = 1e12 # Example threshold
                tfp_shocks = (1 - (annual_cost / cost_threshold)).to_dict()
                
                # Filter for OG-Core relevant years (e.g., first 5 years)
                # OG-Core often requires a list or array
                start_year = int(min(annual_cost.index))
                g_y_shocks = [float(tfp_shocks.get(y, 1.0)) for y in range(start_year, start_year + 10)]
                
                return {
                    "g_y": g_y_shocks,
                    "message": "Dynamic shocks generated from CLEWS results"
                }
            else:
                return {
                    "g_y": [1.0] * 10, # Baseline
                    "message": "CLEWS cost results not found, using baseline"
                }
        except Exception as e:
            return {"error": str(e)}

    def ogcore_to_clews(self, og_results_json):
        """
        Transforms OG-Core results (GDP, Population) into CLEWS demand.
        """
        try:
            # Example: GDP growth -> Increased energy demand
            # Placeholder logic
            gdp_growth = og_results_json.get('gdp_growth', 1.0)
            
            clews_updates = {
                "SpecifiedAnnualDemand": gdp_growth * 1.05 # Simple multiplier
            }
            
            return clews_updates
        except Exception as e:
            return {"error": str(e)}
