document.addEventListener('DOMContentLoaded', function() {
    async function validateForm(event) {
        const usernameInput = document.getElementById('id_username');
        const emailInput = document.getElementById('id_email');
        const password1Input = document.getElementById('id_password1');
        const password2Input = document.getElementById('id_password2');

        clearErrorMessages();

        let valid = true;

        const username = usernameInput.value.trim();
        if (!username) {
            showError(usernameInput, 'El nombre de usuario es requerido.');
            valid = false;
        } else if (!isValidUsername(username)) {
            showError(usernameInput, 'El nombre de usuario solo puede contener letras, dígitos y los caracteres @/./+/-/_.');
            valid = false;
        }

        const email = emailInput.value.trim();
        if (!email) {
            showError(emailInput, 'El correo electrónico es requerido.');
            valid = false;
        } else if (!isValidEmail(email)) {
            showError(emailInput, 'Por favor ingrese un correo electrónico válido.');
            valid = false;
        }

        const password1 = password1Input.value;
        const password2 = password2Input.value;
        if (!password1) {
            showError(password1Input, 'La contraseña es requerida.');
            valid = false;
        } else if (password1.length < 8) {
            showError(password1Input, 'La contraseña debe tener al menos 8 caracteres.');
            valid = false;
        } else if (/^\d+$/.test(password1)) {
            showError(password1Input, 'La contraseña no puede ser solo números.');
            valid = false;
        }

        if (password1 !== password2) {
            showError(password2Input, 'Las contraseñas no coinciden.');
            valid = false;
        }

        if (!valid) {
            event.preventDefault();
        }

        return valid;
    }

    function showError(inputElement, message) {
        const errorElement = document.createElement('div');
        errorElement.classList.add('error-message');
        errorElement.style.color = 'red';
        errorElement.textContent = message;
        inputElement.parentNode.appendChild(errorElement);
    }

    function clearErrorMessages() {
        const errorMessages = document.querySelectorAll('.error-message');
        errorMessages.forEach(el => el.remove());
    }

    function isValidUsername(username) {
        const usernamePattern = /^[a-zA-Z0-9@.+_-]+$/;
        return usernamePattern.test(username);
    }

    function isValidEmail(email) {
        const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
        return emailPattern.test(email);
    }

    const form = document.querySelector('.register-form');
    form.addEventListener('submit', validateForm);
});
