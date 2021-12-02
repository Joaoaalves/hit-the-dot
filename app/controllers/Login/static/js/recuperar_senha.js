beforeSubmit = function(){
    if(document.getElementById('email').value){
        alert("Se a conta existir, um email de recuperação será enviado!");
        return true;
    }
    return false;
}