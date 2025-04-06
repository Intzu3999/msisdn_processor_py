import os
import aiohttp
import urllib.parse
from services.handle_api_error import handle_api_error
from asyncio import Semaphore

MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

service_rate_limiter = Semaphore(1)

async def postpaid_validation_api(token, msisdn):
    async with service_rate_limiter:
        service = "postpaid_validation_api"
        service_data = f"{service}_data"
        result = {"msisdn": msisdn}

        base_url = f"{MOLI_BASE_URL}/postpaid/validation"

        params = {"type": "ALL"}

        body = {
            # "idNumber": "890313085728",
            # "idType": "NRIC",
            # "birthDate": "1982-08-08",
            # "telco": "DIGI"
            "msisdn": msisdn
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "PythonScript/1.0",
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(base_url, params=params, json=body, headers=headers, ssl=False) as response:
                    response.raise_for_status()
                    payload = await response.json()

                    data = payload[0] if isinstance(payload, list) and payload else {}
                    print("🛠️ postpaid_validation_api Raw Payload:", data)

                    extracted_data = flatten_data(data)

                    print(
                        f"✅ postpaid_validation_api: Status {response.status} | MSISDN {msisdn}\n"
                        f"   Overall: {extracted_data['overall_result']}\n"
                        f"   1. {extracted_data['rule_1']}: {extracted_data['rule_1_result']}\n"
                        f"   2. {extracted_data['rule_2']}: {extracted_data['rule_2_result']}\n"
                        f"   3. {extracted_data['rule_3']}: {extracted_data['rule_3_result']}\n"
                        f"   4. {extracted_data['rule_4']}: {extracted_data['rule_4_result']}\n"
                        f"   5. {extracted_data['rule_5']}: {extracted_data['rule_5_result']}"
                    )
                    
                    result[service_data] = {
                        "customerStatus": f"✅ {response.status}",
                        **extracted_data,
                    }

        except aiohttp.ClientResponseError as error:
            return await handle_api_error(error, msisdn, service)

        except Exception as error:
            return await handle_api_error(error, msisdn, service)
        
        return result
    
def flatten_data(data):
    flattened = {
        'overall_result': data.get('result', 'N/A'),
        'validation_type': data.get('type', 'N/A'),
        # Postpaid Validation Rule Fields
        'rule_1': 'N/A', 'rule_1_result': 'N/A',
        'rule_2': 'N/A', 'rule_2_result': 'N/A',
        'rule_3': 'N/A', 'rule_3_result': 'N/A',
        'rule_4': 'N/A', 'rule_4_result': 'N/A',
        'rule_5': 'N/A', 'rule_5_result': 'N/A'
    }
    
    # Populate available rules
    for i, rule in enumerate(data.get('rules', [])[:5], 1):
        flattened[f'rule_{i}'] = rule.get('rule', 'N/A')
        flattened[f'rule_{i}_result'] = rule.get('result', 'N/A')
    
    return flattened