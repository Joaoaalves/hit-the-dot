self.addEventListener('push', function(event) {
        console.log('[Service Worker] Push Received.');
        console.log(`[Service Worker] Push had this data: "${event.data.text()}"`);
        body = event.data.text()
        const title = 'Hit the Dot';
        const options = {
          body: body,
          icon: 'https://htd.dbsweb.com.br/static/images/logo.png',
          badge: 'https://htd.dbsweb.com.br/static/images/logo.png'
        };
        
        event.waitUntil(self.registration.showNotification(title, options));
});