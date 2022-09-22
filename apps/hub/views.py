"""Hub app views."""
import branca
import folium
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.formats import date_format
from django.utils.translation import gettext as _
from folium.features import LatLngPopup
from folium.plugins import Fullscreen, LocateControl
from jinja2 import Template

from apps.accounts.models import User

from .forms import AddMarkerForm, UpdateMarkerForm
from .models import Marker


def home(request):
    """Home page with map."""

    start_location = (50.45, 30.52)  # Ukraine
    current_map = folium.Map(location=start_location, zoom_start=6)
    map_container = branca.element.Figure(height="100%")
    map_container.add_child(current_map)

    # Fullscreen map button
    Fullscreen(
        position="topleft", title=_("Fullscreen"), title_cancel=_("Exit")
    ).add_to(current_map)
    # A button to define user's location
    LocateControl(
        auto_start=False, position="topleft", strings={"title": _("My location")}
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
                        .setContent(e.latlng.lat.toFixed(4) + ", " + e.latlng.lng.toFixed(4) + 
                        "<br><div style='text-align: center; font-size: 2em;'>" +
                        "<a data-bs-toggle='modal' data-bs-target='#addMarker' role='button'>" + 
                        "<i class='fa fa-map-marker' aria-hidden='true'></i></a></div>")
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
    # Layer control button
    folium.LayerControl(position="topleft").add_to(current_map)

    # get or set cache for markers queryset
    markers = cache.get_or_set(
        "markers_frontend",
        Marker.objects.prefetch_related(
            Prefetch("owner", queryset=User.objects.all())
        ).select_related(),
        300,
    )

    for marker in markers:
        folium.Marker(
            location=(marker.latitude, marker.longitude),
            popup=folium.Popup(html=popup_html(marker), max_width=280, max_height=320),
            icon=folium.Icon(
                color=marker.category.color,
                icon=marker.category.icon.name,
                prefix="fa",
            ),
            tooltip=marker.category.name,
        ).add_to(current_map)

    # add new Marker
    if request.method == "POST":
        form = AddMarkerForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.ip = get_client_ip(request)
            form.owner = request.user if isinstance(request.user, User) else None
            form.save()
            messages.success(
                request, _("Marker added successfully!"), extra_tags="success"
            )
            return redirect(to="home")
        else:
            messages.error(request, _("Error. Check coordinates."), extra_tags="danger")
    else:
        form = AddMarkerForm()

    context = {"current_map": map_container.render(), "form": form}
    return render(request, template_name="hub/index.html", context=context)


def about(request):
    """About project page."""
    return render(request, template_name="hub/about.html")


@login_required
def user_markers(request):
    """User markers list page with Delete functionality on POST."""
    markers = Marker.objects.filter(owner_id=request.user.id).select_related()
    if request.method == "POST":
        get_object_or_404(
            Marker, owner=request.user, pk=request.POST.get("delete")
        ).delete()
        messages.success(
            request, _("The marker has been deleted!"), extra_tags="success"
        )
        return redirect("markers")

    paginator = Paginator(markers, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "markers": markers,
        "page_obj": page_obj,
    }
    return render(request, "hub/markers.html", context)


@login_required
def edit_marker(request, marker_id):
    """Edit marker data page."""
    marker = get_object_or_404(Marker, pk=marker_id)
    if request.method == "POST":
        form = UpdateMarkerForm(data=request.POST, instance=marker)
        if form.is_valid():
            form.save()
            messages.success(
                request, _("The marker has been updated!"), extra_tags="success"
            )
            return redirect(to="markers")
        else:
            messages.error(request, _("Please, correct errors."), extra_tags="danger")
    else:
        if marker.owner == request.user:
            form = UpdateMarkerForm(instance=marker)
        else:
            messages.error(request, _("Access forbidden!"), extra_tags="danger")
            raise ValueError(_("Access forbidden!"))
    context = {"form": form, "marker_id": marker_id}
    return render(request, "hub/edit-marker.html", context)


def popup_html(marker):
    """Return HTML template for Marker popup window on a map."""
    comment = marker.comment
    # format UTC timestamp from DB to local user's short datetime format with appropriate timezone
    created_at = date_format(
        marker.created_at.astimezone(), format="SHORT_DATETIME_FORMAT", use_l10n=True
    )
    owner = marker.owner

    html = f"""
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>
        <div style="text-align:center;">
          <a target="_top" href="{"profile-public/" + str(owner.pk) if owner else "#"}/">
            <img style="max-width: 56px; border-radius: 50%;" alt="user_image"
                src="media/{owner.avatar if owner else "avatar/default_avatar.jpg"}">
          </a>
            <h4 style="font-weight:bold; margin:10px 0px 0px 0px;">
                {owner.get_full_name() if owner else ""}
            </h4>
            <p style="font-size:15px; margin-top:10px; margin-bottom:10px;">
                {comment}
            </p>
            <div class="row">
                <div><strong>{created_at}</strong></div>
            </div>
        </div>
        </body>
    </html>
    """
    return html


def get_client_ip(request):
    """Get client IP address."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
