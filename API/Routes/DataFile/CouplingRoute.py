from flask import Blueprint, jsonify, request
from Classes.Case.DataFileClass import DataFile
from Classes.Case.OGCoreClass import OGCore
from Classes.Coupling.ExchangeClass import Exchange

coupling_api = Blueprint('CouplingRoute', __name__)

@coupling_api.route("/api/runCoupling", methods=['GET', 'POST'])
def run_coupling():
    """
    Sequentially runs CLEWS -> ETL -> OG-Core
    """
    try:
        if request.method == 'GET':
            return jsonify({'message': 'Coupling API is active. Use POST to run.'}), 200
            
        casename = request.json['casename']
        caserunname = request.json['caserunname']
        solver = request.json.get('solver', 'CBC')
        
        # 1. Run CLEWS
        clews = DataFile(casename)
        clews_res = clews.run(solver, caserunname)
        if clews_res.get('status_code') != 'success':
            return jsonify({'message': 'CLEWS run failed', 'details': clews_res}), 500
            
        # 2. ETL (CLEWS -> OG-Core)
        exchange = Exchange(casename)
        og_shocks = exchange.clews_to_ogcore(caserunname)
        
        # 3. Run OG-Core
        og = OGCore(casename)
        og_res = og.run_og(f"{caserunname}_coupled", og_spec=og_shocks)
        
        return jsonify({
            "message": "Coupled run completed successfully",
            "clews": clews_res,
            "ogcore": og_res,
            "status_code": "success"
        }), 200
        
    except Exception as e:
        return jsonify({'message': str(e), 'status_code': 'error'}), 500

@coupling_api.route("/runConvergence", methods=['POST'])
def run_convergence():
    """
    Iteratively runs models until results converge
    """
    # This will be fully implemented in Phase 3
    return jsonify({'message': 'Convergence module planned for Phase 3', 'status_code': 'planned'}), 202
