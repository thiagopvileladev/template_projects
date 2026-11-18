// Botão "Imprimir / Salvar PDF": abre a impressão do navegador, que permite
// salvar como PDF. Fica em arquivo separado (sem JavaScript inline no HTML).
document.querySelectorAll('[data-imprimir]').forEach(function (botao) {
    botao.addEventListener('click', function () {
        window.print();
    });
});
