"""Hub app views."""

from django.shortcuts import render
from django.utils.translation import gettext as _

import folium
from folium import Popup
from folium.features import LatLngPopup
from folium.plugins import Fullscreen, LocateControl
from jinja2 import Template


def home(request):
    """Home page with map."""
    start_location = (50.45, 30.52)  # Ukraine
    current_map = folium.Map(location=start_location, zoom_start=6)

    # Fullscreen map button
    Fullscreen(position="topright", title=_("Полный экран"), title_cancel=_("Выход")).add_to(
        current_map
    )
    # A button to define user's location
    LocateControl(
        auto_start=False, position="topright", strings={"title": _(str("Где я"))}
    ).add_to(current_map)

    # Rewrite the default popup text to use custom popup with only coordinates
    popup = LatLngPopup()
    popup._template = Template(
        """
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.popup();
                function latLngPop(e) {
                    {{this.get_name()}}
                        .setLatLng(e.latlng)
                        .setContent(e.latlng.lat.toFixed(4) + ", " + e.latlng.lng.toFixed(4))
                        .openOn({{this._parent.get_name()}});
                        parent.document.getElementById("coordinates").value = 
                        e.latlng.lat.toFixed(4) + "," + e.latlng.lng.toFixed(4);
                    }
                {{this._parent.get_name()}}.on('click', latLngPop);
            {% endmacro %}
            """
    )
    popup.add_to(current_map)

    # deliver_layer = folium.FeatureGroup(name="Вручают").add_to(current_map)

    # Layer control button
    folium.LayerControl().add_to(current_map)

    maps = current_map._repr_html_()

    return render(request, template_name="index.html", context={"maps": maps})
