from flask import Blueprint, jsonify, request, session
from pathlib import Path
from Classes.Case.OGCoreClass import OGCore
from Classes.Base import Config

ogcore_api = Blueprint('OGCoreRoute', __name__)

@ogcore_api.route("/api/runOG", methods=['GET', 'POST'])
def run_og():
    try:
        if request.method == 'GET':
            return jsonify({'message': 'OG-Core API is active. Use POST to run.'}), 200
        
        casename = request.json.get('casename')
        sc_name = request.json.get('sc_name', 'default_og_run')
        og_spec = request.json.get('og_spec', {})

        if not casename:
            return jsonify({'message': 'No case selected.', 'status_code': 'error'}), 400

        og = OGCore(casename)
        response = og.run_og(sc_name, og_spec)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status_code': 'error'}), 500

@ogcore_api.route("/getOGResults", methods=['POST'])
def get_og_results():
    try:
        casename = request.json.get('casename')
        sc_name = request.json.get('sc_name')

        if not casename or not sc_name:
            return jsonify({'message': 'Missing parameters.', 'status_code': 'error'}), 400

        og = OGCore(casename)
        response = og.get_og_results(sc_name)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status_code': 'error'}), 500
