function whatsapp(phone_number){
    url = 'https://api.whatsapp.com/send?phone=' + phone_number;
    window.open(url, '_blank').focus();
}