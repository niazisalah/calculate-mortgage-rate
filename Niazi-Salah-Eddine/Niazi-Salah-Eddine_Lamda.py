import json
import requests

def lambda_handler(event, context):
    
    # Lecture des attributs dette et nb_mois
    d = float(event["dette"])
    n = float(event["nb_mois"])
    
    # Lecture du taux_interet si non null, sinon requete vers API de la banque
    if event["taux_interet"] is not None:
        i = float(event["taux_interet"])*0.01
    else:
        api_url = 'https://api.api-ninjas.com/v1/interestrate?name=Canadian BOC'
    
        api_response = requests.get(api_url, headers={'X-Api-Key': '49FrttvE62WItHpaC/npkg==dDJnRTENfM0l4wdW'})
    
        if api_response.status_code == requests.codes.ok:
            json_response = api_response.json()
            rate = json_response['central_bank_rates'][0]['rate_pct']
            i = (rate+1)*0.01
        else:
            print("Error:", api_response.status_code, api_response.text)
    
    # Calcul du paiement mensuel
    m_haut = d * (i / 12 * pow((1 + i / 12), n))
    m_bas = pow((1 + i / 12), n) - 1
    m = m_haut / m_bas
    
    return round(m,2)