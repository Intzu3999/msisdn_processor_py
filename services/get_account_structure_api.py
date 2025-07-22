import os
import aiohttp
from services.handle_api_error import handle_api_error
from asyncio import Semaphore

MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

service_rate_limiter = Semaphore(1)

async def get_account_structure_api(token, msisdn):
    async with service_rate_limiter:
        service = "account_structure_api"
        service_data = f"{service}_data"
        result = {"msisdn": msisdn}

        base_url = f"{MOLI_BASE_URL}/moli-account/v1/accounts/{msisdn}/structure"
        params = {
            "level": "customer"
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "PythonScript/1.0",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, params=params, headers=headers) as response:

                     # Validate response format first
                    payload = await response.json()
                    if not isinstance(payload, dict):
                        raise ValueError(f"Unexpected response format: {type(payload)}")
                    
                    # print(f"DEBUG - Raw payload: {payload}")  # Inspect actual structure
                    
                    # Ensure structure exists
                    if "structure" not in payload:
                        payload["structure"] = []
                    
                    extracted_data = extract_account_structure(payload, msisdn)

                    print(extracted_data)
                    
                    result[service_data] = {
                        "customerStatus": f"✅ {response.status}",
                        "msisdn": msisdn,
                        "extracted": extracted_data,
                    }

        except aiohttp.ClientResponseError as error:
            return await handle_api_error(error, msisdn, service)
        except Exception as error:
            return await handle_api_error(error, msisdn, service)

        return result


def extract_account_structure(payload, original_msisdn):
    extracted_data = []
    
    for account in payload.get("structure", []):
        telco = account.get("telco", "N/A")
        principal = account.get("principal", {})
        principal_msisdn = principal.get("msisdn", "")
        principal_account_number = principal.get("accountNumber", "N/A")
        customer_name = principal.get("customerName", "N/A")
        pay_type = principal.get("payType", "N/A")
        subscriber_status = principal.get("subscriberStatus", "N/A")
        supplementary_lines = account.get("supplementary", [])

        # If there are no supplementary lines, we still want the principal row
        if not supplementary_lines:
            extracted_data.append({
                "telco": telco,
                "account_type": "principal",
                "linked_principal_msisdn": principal_msisdn,
                "account_number": principal_account_number,
                "msisdn": principal_msisdn,
                "customer_name": customer_name,
                "pay_type": pay_type,
                "status": subscriber_status,
                "total_supplementary": 0,
                "is_original_msisdn": str(principal_msisdn) == str(original_msisdn),
            })
        else:
            # Add supplementary lines as flattened rows
            for supp in supplementary_lines:
                extracted_data.append({
                    "telco": telco,
                    "account_type": "supplementary",
                    "linked_principal_msisdn": principal_msisdn,
                    "account_number": supp.get("accountNumber", "N/A"),
                    "msisdn": supp.get("msisdn", "N/A"),
                    "customer_name": supp.get("customerName", "N/A"),
                    "pay_type": supp.get("payType", "N/A"),
                    "status": supp.get("subscriberStatus", "N/A"),
                    "total_supplementary": len(supplementary_lines),
                    "is_original_msisdn": str(supp.get("msisdn", "")) == str(original_msisdn),
                })

    return extracted_data



# def flatten_data(data, original_msisdn):
#     flattened = {
#         'telco': data.get('telco', 'N/A'),
#         'level': data.get('level', 'N/A'),
#         'total_accounts': len(data.get('structure', [])),
#         'accounts': []
#     }

#     for idx, account in enumerate(data.get('structure', []), 1):
#         principal = account.get('principal', {})
#         supplementary = account.get('supplementary', [])

#         principal_data = {
#             'account_type': 'principal',
#             'account_index': idx,
#             'account_number': principal.get('accountNumber', 'N/A'),
#             'msisdn': principal.get('msisdn', 'N/A'),
#             'customer_name': principal.get('customerName', 'N/A'),
#             'pay_type': principal.get('payType', 'N/A'),
#             'status': principal.get('subscriberStatus', 'N/A'),
#             'is_original_msisdn': str(principal.get('msisdn', '')) == str(original_msisdn)
#         }

#         flattened['accounts'].append(principal_data)

#         for sup_idx, sup in enumerate(supplementary, 1):
#             sup_data = {
#                 'account_type': 'supplementary',
#                 'account_index': f"{idx}.{sup_idx}",
#                 'account_number': sup.get('accountNumber', 'N/A'),
#                 'msisdn': sup.get('msisdn', 'N/A'),
#                 'customer_name': sup.get('customerName', 'N/A'),
#                 'pay_type': sup.get('payType', 'N/A'),
#                 'status': sup.get('subscriberStatus', 'N/A'),
#                 'is_original_msisdn': str(sup.get('msisdn', '')) == str(original_msisdn)
#             }
#             flattened['accounts'].append(sup_data)

#     return flattened