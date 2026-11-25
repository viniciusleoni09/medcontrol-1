
// MEDCONTROL - JAVASCRIPT

// Mensagem de confirmação
function confirmarAcao(mensagem) {
    return confirm(mensagem);
}

// Mostrar mensagem na tela
function mostrarMensagem(mensagem) {
    alert(mensagem);
}

// Confirmar exclusão
function confirmarExclusao() {
    return confirm("Tem certeza que deseja excluir este registro?");
}

// Validação de formulário
function validarFormulario() {

    const campos = document.querySelectorAll(
        "input[required]"
    );

    for (let campo of campos) {

        if (campo.value.trim() === "") {
            alert("Preencha todos os campos obrigatórios!");
            campo.focus();
            return false;
        }

    }

    return true;
}
