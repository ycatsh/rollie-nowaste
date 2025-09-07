  document.getElementById('show-password').addEventListener('change', function () {
    const passwordField = document.getElementById('password');
    const confirm_passwordField = document.getElementById('confirm_password');
    passwordField.type = this.checked ? 'text' : 'password';
    confirm_passwordField.type = this.checked ? 'text' : 'password';
});
