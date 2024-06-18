from flask import Flask, jsonify, request
import requests
from models import AirQuality
from database import get_session

app = Flask(__name__)

# Substitua pela sua chave de API válida do IQAir
AIRVISUAL_API_KEY = "d5a62d69-eb13-4cbc-8dc7-9e439c4b53ba"
AIRVISUAL_API_URL = "http://api.airvisual.com/v2/city"


@app.route('/qualidade_ar', methods=['GET'])
def get_air_quality():
    cidade = request.args.get('cidade')
    estado = request.args.get('estado')
    pais = request.args.get('pais', 'Brazil')  # Por padrão, assume os EUA
    if not cidade or not estado:
        return jsonify({'erro': 'Cidade e estado não fornecidos.'}), 400

    params = {
        'city': cidade,
        'state': estado,
        'country': pais,
        'key': AIRVISUAL_API_KEY
    }

    try:
        response = requests.get(AIRVISUAL_API_URL, params=params)
        response.raise_for_status()
        dados_ar = response.json()

        if 'data' not in dados_ar:
            return jsonify({'erro': 'Dados de qualidade do ar não disponíveis.'}), 500

        # Extrair os dados de interesse
        air_data = dados_ar['data']['current']['pollution']
        aqius = air_data['aqius']
        mainus = air_data['mainus']
        aqicn = air_data['aqicn']
        maincn = air_data['maincn']

        # Salvar no banco de dados
        session = get_session()
        nova_entrada = AirQuality(
            cidade=cidade,
            estado=estado,
            pais=pais,
            aqius=aqius,
            mainus=mainus,
            aqicn=aqicn,
            maincn=maincn
        )
        session.add(nova_entrada)
        session.commit()
        session.close()

        return jsonify({
            'cidade': dados_ar['data']['city'],
            'estado': dados_ar['data']['state'],
            'pais': dados_ar['data']['country'],
            'qualidade_ar': air_data
        })

    except requests.RequestException as e:
        return jsonify({'erro': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
