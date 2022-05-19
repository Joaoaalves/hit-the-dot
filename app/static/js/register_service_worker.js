'use strict';

function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

function updateSubscriptionOnServer(subscription, apiEndpoint, csrf_token) {
  return fetch(apiEndpoint, {
    method: 'POST',
    headers: {
      'X-CSRFToken' : csrf_token,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      subscription_json: JSON.stringify(subscription)
    })
  });

}

function subscribeUser(swRegistration, applicationServerPublicKey, apiEndpoint, csrf_token) {
  const applicationServerKey = urlB64ToUint8Array(applicationServerPublicKey);
  swRegistration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: applicationServerKey
  })
  .then(function(subscription) {
 
    return updateSubscriptionOnServer(subscription, apiEndpoint, csrf_token);

  })
  .then(function(response) {
    if (!response.ok) {
      throw new Error('Bad status code from server.');
    }
    return response.json();
  })
  .then(function(responseData) {
    if (responseData.status!=="success") {
      throw new Error('Bad response from server.');
    }
  })
  .catch(function(err) {
  });
}

function registerServiceWorker(serviceWorkerUrl, applicationServerPublicKey, apiEndpoint, csrf_token){
  let swRegistration = null;
  if ('serviceWorker' in navigator && 'PushManager' in window) {
    navigator.serviceWorker.register(serviceWorkerUrl)
    .then(function(swReg) {
      subscribeUser(swReg, applicationServerPublicKey, apiEndpoint, csrf_token);

      swRegistration = swReg;
    })
    .catch(function(error) {
    });
  } else {
    console.warn('Push messaging is not supported');
  } 
  return swRegistration;
}
