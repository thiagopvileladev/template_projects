from rest_framework import permissions


class DonoOuSomenteLeitura(permissions.BasePermission):
    """Qualquer um lê; só o autor altera ou exclui a própria avaliação."""

    message = 'Você só pode alterar ou excluir as suas próprias avaliações.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.usuario_id == request.user.id
