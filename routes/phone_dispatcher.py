from flask import request, Blueprint, jsonify, current_app

from config import neo4j_driver
from repository.Phone_tracker_repository import PhoneTrackerRepository

phone_blueprint = Blueprint('phone_blueprint', __name__)



@phone_blueprint.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
   data =  request.json

   try:
      repo = PhoneTrackerRepository(neo4j_driver)
      repo.create_phone_tracker(data)


      return jsonify({'success': True}), 201

   except Exception as e:
      print(e)
      return jsonify({'error': str(e)}), 500


@phone_blueprint.route("/api/by_bluetooth", methods=['GET'])
def get_interaction_by_bluetooth():
   try:
       repo = PhoneTrackerRepository(neo4j_driver)
       result = repo.get_num_phon_by_bluetooth()

       return jsonify({'result': result}), 200

   except Exception as e:
      print(e)
      return jsonify({'error': str(e)}), 500


@phone_blueprint.route("/api/by_signal_strength_dbm", methods=['GET'])
def by_signal_strength_dbm():

    try:

        repo = PhoneTrackerRepository(neo4j_driver)
        result = repo.get_phon_by_signal_strength_dbm()

        return jsonify({'result': result}), 200


    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500



@phone_blueprint.route("/api/phone_connected/<string:id>", methods=['GET'])
def phone_connected(id):
    try:
        repo = PhoneTrackerRepository(neo4j_driver)
        result = repo.get_num_phon_is_connected(id)

        return jsonify({'result': result}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500




