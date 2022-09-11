"""Hub app views."""

import folium
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from folium.features import LatLngPopup
from folium.plugins import Fullscreen, LocateControl
from jinja2 import Template

from .forms import AddMarkerForm
from .models import Marker


def home(request):
    """Home page with map."""

    start_location = (50.45, 30.52)  # Ukraine
    current_map = folium.Map(location=start_location, zoom_start=6)

    # Fullscreen map button
    Fullscreen(
        position="topleft", title=_("Полный экран"), title_cancel=_("Выход")
    ).add_to(current_map)
    # A button to define user's location
    LocateControl(
        auto_start=False, position="topleft", strings={"title": _("Где я")}
    ).add_to(current_map)

    # Rewrite the default popup text to use custom popup with only coordinates
    # and auto latitude, longitude fields filling upon mouse click on a map
    lat_lng_popup = LatLngPopup()
    lat_lng_popup._template = Template(
        """
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.popup();
                function latLngPop(e) {
                    {{this.get_name()}}
                        .setLatLng(e.latlng)
                        .setContent(e.latlng.lat.toFixed(4) + ", " + e.latlng.lng.toFixed(4))
                        .openOn({{this._parent.get_name()}});
                        parent.document.getElementById("latitude").value = e.latlng.lat.toFixed(4);
                        parent.document.getElementById("longitude").value = e.latlng.lng.toFixed(4);
                    }
                {{this._parent.get_name()}}.on('click', latLngPop);
            {% endmacro %}
            """
    )
    lat_lng_popup.add_to(current_map)

    # deliver_layer = folium.FeatureGroup(name="Вручают").add_to(current_map)

    html = """
        <div style="text-align:center;">
            <img style="max-width: 64px; border-radius: 50%;" 
                src="https://epicbootstrap.com/freebies/snippets/team-cards/assets/img/2.jpg">
            <h3 style="font-weight:bold; margin:10px 0px 0px 0px;">
                Ben Johnson
            </h3>
            <p style="font-size:15px; margin-top:10px; margin-bottom:10px;">
                Aenean tortor est, vulputate quis leo Aenean tortor est, vulputate quis leo in, vehicula rhoncus lacus. 
                Praesent aliquam in tellus eu gravida. Aliquam varius finibus est, et interdum justo suscipit id
            </p>
            <div>
                <a href="#" target="_top" style="margin:0 10px; display:inline-block;">Facebook</a>
            </div>
        </div>
    """
    iframe = folium.IFrame(html=html, width=260, height=260)

    # Layer control button
    folium.LayerControl(position="topleft").add_to(current_map)

    markers = Marker.objects.all().select_related()
    for marker in markers:
        folium.Marker(
            location=(marker.latitude, marker.longitude),
            popup=folium.Popup(iframe, max_width=280, max_height=320),
            icon=folium.Icon(
                color=marker.category.color.name,
                icon=marker.category.icon.name,
                prefix="fa",
            ),
            # tooltip=tooltip,
        ).add_to(current_map)

    if request.method == "POST":
        form = AddMarkerForm(request.POST)
        if form.is_valid():
            # form.save(commit=False)
            # form.ip = get_client_ip(request)
            form.save()
            messages.success(request, _("Маркер успешно опубликован!"), "success")
            return redirect(to="home")
        else:
            messages.error(request, _(f"Ошибка. Проверьте координаты."), "danger")
    else:
        form = AddMarkerForm()

    m = current_map._repr_html_()
    context = {"current_map": m, "form": form}
    return render(request, template_name="hub/index.html", context=context)


def about(request):
    """About project page."""
    return render(request, template_name="hub/about.html")


@login_required(redirect_field_name="login")
def user_markers(request):
    """User markers list page."""
    markers = Marker.objects.filter(owner_id=request.user.id).select_related()
    if request.method == "POST":
        get_object_or_404(
            Marker, owner=request.user, pk=request.POST.get("delete")
        ).delete()
        messages.success(request, _("Метка удалена!"), "success")
        return redirect("markers")
    context = {
        "markers": markers,
    }
    return render(request, "hub/markers.html", context)


# def get_client_ip(request):
#     """Get client IP address."""
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip
