from django import template

register = template.Library()


@register.inclusion_tag("_navbar.html", takes_context=True)
def navbar(context):
    """
    Renderiza o menu principal identificando automaticamente a aba ativa
    com base no nome da URL atual (request.resolver_match.url_name ou namespace).
    """
    request = context.get("request")

    current_url_name = ""
    current_namespace = ""

    if request and hasattr(request, "resolver_match") and request.resolver_match:
        current_url_name = request.resolver_match.url_name
        current_namespace = request.resolver_match.namespace

    nav_items = [
        {
            "id": "cadastros",
            "label": "cadastros",
            "url_name": "cadastros:listar",
            "is_active": current_namespace == "cadastros" or current_url_name == "listar",
        },
        {
            "id": "produtos",
            "label": "produtos",
            "url_name": "pagina_inicial",
            "is_active": current_namespace == "produtos",
        },
        {
            "id": "compras",
            "label": "compras",
            "url_name": "pagina_inicial",
            "is_active": current_namespace == "compras",
        },
        {
            "id": "vendas",
            "label": "vendas",
            "url_name": "pagina_inicial",
            "is_active": current_namespace == "vendas",
        },
        {
            "id": "financeiro",
            "label": "financeiro",
            "url_name": "pagina_inicial",
            "is_active": current_namespace == "financeiro",
        },
        {
            "id": "fiscal",
            "label": "fiscal",
            "url_name": "pagina_inicial",
            "is_active": current_namespace == "fiscal",
        },
    ]

    return {
        "nav_items": nav_items,
    }


@register.inclusion_tag("_th_sortable.html", takes_context=True)
def th_sortable(context, field, label, align="start"):
    """
    Renderiza um cabeçalho <th> ordenável.
    - field: Nome do campo no model (ex: 'descricao')
    - label: Texto exibido no cabeçalho
    - align: Alinhamento 'start' (esquerda), 'center' ou 'end' (direita)
    """
    request = context.get("request")
    current_order = request.GET.get("order_by", "") if request else ""

    is_current = current_order.lstrip("-") == field
    is_desc = current_order == f"-{field}"

    next_order = f"-{field}" if (is_current and not is_desc) else field

    return {
        "request": request,
        "field": field,
        "label": label,
        "align": align,
        "is_current": is_current,
        "is_desc": is_desc,
        "next_order": next_order,
    }
