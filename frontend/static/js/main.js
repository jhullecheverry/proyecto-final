/**
 * Funciones utilitarias para el frontend
 */

function showMessage(text, type = 'success') {
    const messageDiv = document.getElementById('message');
    if (!messageDiv) return;

    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';

    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

function formatCurrency(value) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP'
    }).format(value);
}

function handleError(error) {
    console.error('Error:', error);
    showMessage('Ha ocurrido un error. Por favor, inténtelo de nuevo.', 'error');
}