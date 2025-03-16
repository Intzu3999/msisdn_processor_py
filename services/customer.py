import os
from dotenv import load_dotenv

load_dotenv()

# const { getToken } = require('../tokenManager'); 
MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")






const getCustomerApi = async (msisdn) => {
  const result = { msisdn };

  let token;
  try {
    token = await getToken(); // Use the cached token
  } catch (error) {
    console.error("❌ Failed to fetch token:", error.message);
    return result; // Return the result object with the error state
  }

  // GET Customer v3
  try {
    const getCustomerParams = new URLSearchParams({ msisdn });
    const getCustomerURL = `${BASE_URL}/moli-customer/v3/customer?${getCustomerParams.toString()}`;    
    
    const apiResponse = await axios.get(getCustomerURL, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    // console.log('🛠️ getCustomer Payload:', apiResponse?.data);
    const idNo = apiResponse?.data?.[0]?.personalInfo?.[0]?.identification?.[0]?.idNo || 'N/A';
    const idType = apiResponse?.data?.[0]?.personalInfo?.[0]?.identification?.[0]?.type?.code || 'NA';
    const countryCode = apiResponse?.data?.[0]?.contact?.address?.[0]?.country?.code || 'NA' ;
    console.log(`✅ getCustomerApi: ${apiResponse.status} id:${idType} ${idNo} countryCode:${countryCode}`);

    result.getCustomerApiData = {
      httpStatus: `✅ ${apiResponse.status}`,
      idNo: (idNo || "Null"),
      idType: (idType || "Null"),
      countryCode: (countryCode || "Null"),
    };

  } catch (error) {
    const statusCode = error.response?.status || "Unknown Status";
    const errorMessage = error.response?.data?.message || error.message || "Unknown Error";
    console.error(`❌ getCustomerApi: Status - ${statusCode}, Error - ${errorMessage}`);
    result.getCustomerApiData = `❌ ${statusCode}`;
  }

  return result;
};

const postCustomerApi = async (msisdn, telco, id) => {
  const result = { msisdn , telco, id };
  let token;
    try {
      token = await getAccessToken(); 
    } catch (error) {
      console.error("❌ Failed to fetch token:", error.message);
      return result; 
    }

  // POST customer - TESTING
  try {
    const subscriberParams = new URLSearchParams({ msisdn, telco });
    const subscriberURL = `${BASE_URL}/moli-subscriber/v1/subscriber?${subscriberParams.toString()}`;    
    
    const subscriberResponse = await axios.get(subscriberURL, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    // console.log('🛠️ getSubscriber Payload:', subscriberResponse?.data);
    const subscriberTelco = subscriberResponse.data.telco;
    const payType = subscriberResponse.data.type;  

    console.log(`✅ postCustomerApi: ${subscriberResponse.status} ${subscriberTelco} ${payType}`);

    result.postCustomerApiData = {
      httpStatus: `✅ ${subscriberResponse.status}`,
      telco: subscriberTelco || "Null",
      payType: payType || "Null",   
    };

  } catch (error) {
    const statusCode = error.response?.status || "Unknown Status";
    const errorMessage = error.response?.data?.message || error.message || "Unknown Error";
    console.error(`❌ postCustomerApi: Status - ${statusCode}, Error - ${errorMessage}`);
    result.postCustomerApiData = `❌ ${statusCode}`;
  }

  return result;
};

module.exports = { getCustomerApi, postCustomerApi };