// Comportamentos globais do TrackVault.
// Fica em arquivo próprio (sem JavaScript inline no HTML) para permitir uma
// Content-Security-Policy restritiva: script-src 'self' (achado DAST-02).

// <button data-confirmar="Mensagem?"> pede confirmação antes de enviar o formulário.
document.addEventListener('click', function (evento) {
    var alvo = evento.target.closest('[data-confirmar]');
    if (alvo && !window.confirm(alvo.getAttribute('data-confirmar'))) {
        evento.preventDefault();
    }
});
