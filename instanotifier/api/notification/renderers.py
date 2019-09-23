from rest_framework.renderers import (
    BrowsableAPIRenderer,
    JSONRenderer,
    TemplateHTMLRenderer,
)


class TemplateHTMLRendererBase(TemplateHTMLRenderer):
    """ Base class that converts the context into a dict """

    def _convert_context_into_dict(self, context):
        if not "results" in context and not isinstance(context, dict):
            context = dict(results=context)
        return context

    def get_template_context(self, data, renderer_context):
        # NOTE: the data input argument should be a dictionary, according
        # to parent get_template_context()
        # The pagination of view translates the queryset into a dict.

        context = super(TemplateHTMLRendererBase, self).get_template_context(
            data, renderer_context
        )

        context = self._convert_context_into_dict(context)
        return context


class ListViewTemplateRenderer(TemplateHTMLRendererBase, BrowsableAPIRenderer):
    """ Renders the list of RssNotifications into an html. Supports searching. """

    template_name = "api/notification/rssnotification_api_list.html"

    def get_template_context(self, data, renderer_context):
        view = renderer_context["view"]
        request = renderer_context["request"]
        response = renderer_context["response"]

        context = super(ListViewTemplateRenderer, self).get_template_context(
            data, renderer_context
        )

        if getattr(view, "paginator", None) and view.paginator.display_page_controls:
            paginator = view.paginator
        else:
            paginator = None

        context["paginator"] = paginator
        context["filter_form"] = self.get_filter_form(data, view, request)
        context["filter_date_used"] = (
            view.filter_date_used if hasattr(view, "filter_date_used") else ""
        )
        context["rating_checkbox"] = view.rating_manager.checkbox
        context["rating_checkbox_is_checked"] = (
            "checked" if view.rating_manager.checkbox.is_checked else ""
        )

        return context
