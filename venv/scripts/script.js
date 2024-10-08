document.addEventListener('DOMContentLoaded', () => {
    if (recompensasObtidas.length > 0) {
        // Exibir a primeira recompensa desbloqueada
        document.getElementById('recompensa-obtida').textContent = recompensasObtidas[0];
        document.getElementById('popup-recompensa').classList.remove('hidden');
    }
});

function fecharPopup() {
    document.getElementById('popup-recompensa').classList.add('hidden');
}
