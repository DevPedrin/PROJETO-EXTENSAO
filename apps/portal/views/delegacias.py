from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages

from django.contrib.auth.decorators import (
    login_required,
    user_passes_test
)

from ..models import Delegacia
from ..forms import DelegaciaForm
from ..permissions import eh_admin


@login_required
@user_passes_test(eh_admin)
def painel_delegacias(request):

    if request.method == 'POST':

        pk = request.POST.get('pk')
        acao = request.POST.get('acao')

        if acao == 'excluir' and pk:

            Delegacia.objects.filter(
                pk=pk
            ).delete()

            messages.success(
                request,
                'Delegacia removida com sucesso.'
            )

            return redirect(
                'portal:painel_delegacias'
            )

        if acao == 'toggle_ativo' and pk:

            delegacia = get_object_or_404(
                Delegacia,
                pk=pk
            )

            delegacia.ativo = (
                not delegacia.ativo
            )

            delegacia.save()

            messages.success(
                request,
                f'Delegacia {"ativada" if delegacia.ativo else "desativada"}.'
            )

            return redirect(
                'portal:painel_delegacias'
            )

        pk_editar = request.POST.get(
            'pk_editar'
        )

        if pk_editar:

            instancia = get_object_or_404(
                Delegacia,
                pk=pk_editar
            )

            form = DelegaciaForm(
                request.POST,
                instance=instancia
            )

            if form.is_valid():

                form.save()

                messages.success(
                    request,
                    'Delegacia atualizada com sucesso.'
                )

                return redirect(
                    'portal:painel_delegacias'
                )

        else:

            form = DelegaciaForm(
                request.POST
            )

            if form.is_valid():

                form.save()

                messages.success(
                    request,
                    'Delegacia cadastrada com sucesso.'
                )

                return redirect(
                    'portal:painel_delegacias'
                )

    else:

        form = DelegaciaForm()

    delegacias = (
        Delegacia.objects.all()
    )

    return render(
        request,
        'portal/painel_delegacias.html',
        {
            'form': form,
            'delegacias': delegacias,
        }
    )