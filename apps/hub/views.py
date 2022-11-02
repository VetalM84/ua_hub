"""Hub app views."""

import os
from typing import List

import branca
import folium
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import BadHeaderError, send_mail
from django.core.paginator import Paginator
from django.db.models import Count, Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.formats import date_format
from django.utils.html import strip_tags
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from folium.features import LatLngPopup
from folium.plugins import Fullscreen, LocateControl, MarkerCluster
from jinja2 import Template

from apps.accounts.models import User
from ua_hub import settings

from .forms import AddMarkerForm, ContactForm, UpdateMarkerForm
from .models import Category, Comment, Marker


def home(request):
    """Home page with map."""

    try:
        user = User.objects.only("start_coordinates").get(pk=request.user.pk)
        start_coordinates = user.start_coordinates.split(",")
        current_map = folium.Map(location=start_coordinates, zoom_start=6)
    except (ValueError, User.DoesNotExist):
        current_map = folium.Map(location=(48.51, 32.25), zoom_start=6)

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
                        "<i class='fa-solid fa-location-dot'></i></a></div>")
                        .openOn({{this._parent.get_name()}});
                        parent.document.getElementById("latitude").value = e.latlng.lat.toFixed(4);
                        parent.document.getElementById("longitude").value = e.latlng.lng.toFixed(4);
                    }
                {{this._parent.get_name()}}.on('click', latLngPop);
            {% endmacro %}
            """
    )
    lat_lng_popup.add_to(current_map)

    # get or set cache for markers queryset
    markers = cache.get_or_set(
        "markers_frontend",
        Marker.objects.prefetch_related(
            Prefetch(
                "comments",
                queryset=Comment.objects.annotate(cmns_cnt=Count("marker__comment")),
            )
        ).select_related("category", "owner", "category__icon"),
        timeout=3600,
    )

    # create a list of Layers from markers categories
    layers_list = []
    for item in Category.objects.all().only("name"):
        layers_list.append(MarkerCluster(name=item.name).add_to(current_map))

    # add marker to appropriate layer
    for layer in layers_list:
        for marker in markers:
            if marker.category.name == layer.layer_name:
                folium.Marker(
                    location=(marker.latitude, marker.longitude),
                    popup=folium.Popup(
                        html=popup_html(marker),
                        min_width=130,
                        max_width=280,
                        max_height=320,
                    ),
                    icon=folium.Icon(
                        color=marker.category.color,
                        icon=marker.category.icon.name,
                        prefix="fa",
                    ),
                    tooltip=marker.category.name,
                ).add_to(layer)

    folium.LayerControl(position="topleft").add_to(current_map)

    # add new Marker
    if request.method == "POST":
        form = AddMarkerForm(request.POST, request.FILES)
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
            messages.error(request, form.errors, extra_tags="danger")
    else:
        form = AddMarkerForm()

    context = {"current_map": map_container.render(), "form": form}
    return render(request, template_name="hub/index.html", context=context)


def get_marker(request, marker_id):
    """Get marker page."""
    marker = cache.get_or_set(
        f"marker_{marker_id}",
        get_object_or_404(
            Marker.objects.select_related("category", "owner").prefetch_related(
                "comments__owner", "comments"
            ),
            pk=marker_id,
        ),
        timeout=3600,
    )
    context = {
        "marker": marker,
    }
    return render(request, "hub/marker.html", context)


def about(request):
    """About project page."""
    return render(request, template_name="hub/about.html")


def privacy_policy(request):
    """Privacy Policy page."""
    return render(request, template_name="hub/gdrp.html")


def contact(request):
    """Contact us form page."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            send_email(
                subject="A message from UAHub",
                message=form.cleaned_data["message"],
                from_email=form.cleaned_data["from_email"],
                recipient_list=os.getenv("RECIPIENT_LIST").split(","),
            )
            messages.success(
                request, _("Email sent successfully!"), extra_tags="success"
            )
            return redirect("home")

    if request.user.is_anonymous:
        form = ContactForm()
    else:
        form = ContactForm(initial={"from_email": request.user.email})

    return render(request, template_name="hub/contact.html", context={"form": form})


@login_required
def user_markers(request):
    """User markers list page with Delete functionality on POST."""

    markers = cache.get_or_set(
        f"markers_user_{request.user.pk}_{get_language()}",
        Marker.objects.filter(owner_id=request.user.id)
        .order_by("-pk")
        .select_related(),
        3600,
    )
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
    comment = marker.comment[:160]
    # format UTC timestamp from DB to local user's short datetime format with appropriate timezone
    created_at = date_format(
        marker.created_at.astimezone(), format="SHORT_DATETIME_FORMAT", use_l10n=True
    )
    comments = marker.comments.count()
    comments_data = ""
    if comments:
        comments_data = f"""{comments}<i class="fa-solid fa-comments p-1"></i>"""

    likes = marker.likes_count
    likes_data = ""
    if likes:
        likes_data = f"""{likes}<i class="fa-solid fa-heart p-1"></i>"""

    image_data = ""
    if marker.image:
        image_data = f"""<i class="fa-regular fa-image p-1"></i>"""

    owner = marker.owner
    owner_data = ""
    if owner:
        owner_data = f"""
              <a target="_top" href="profile-public/{owner.pk}/">
                <img style="width: 50px; height: 50px; border-radius: 50%;" alt="user_image"
                    src="{owner.avatar_m.url if owner else "media/avatar/default_avatar.jpg"}">
              </a>
                <h5 style="font-weight:bold; margin:10px 0px 0px 0px;">
                    {owner.get_full_name() if owner else ""}
                </h5>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>
        <div class="text-center">
            <div class="d-flex">
                <div>{comments_data}</div>
                <div>{likes_data}</div>
                <div>{image_data}</div>
            </div>
            {owner_data}
            <p style="font-size:15px; margin:10px 0;">
                {comment}{"..." if len(comment) >= 160 else ""}
            </p>
            <div class="d-flex">
                <div class="flex-fill text-start fw-bold">{created_at}</div>
                <div class="flex-fill text-end">
                    <a href="marker/{marker.pk}/">
                        <i class="fa-solid fa-arrow-up-right-from-square"></i>
                    </a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html


def send_email(
    subject: str,
    from_email: str,
    recipient_list: List[str],
    message: str = None,
    html_message: str = None,
):
    """Method to send email."""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
        )
    except BadHeaderError:
        return HttpResponse(_("Invalid header found."))


def get_client_ip(request):
    """Get client IP address."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def like(request):
    """Add like to marker."""
    if request.POST.get("action") == "post":
        marker_id = int(request.POST.get("marker_id"))
        marker = get_object_or_404(Marker, id=marker_id)
        if marker.like.filter(id=request.user.pk).exists():
            marker.like.remove(request.user)
            marker.likes_count -= 1
            result = marker.likes_count
            marker.save()
        else:
            marker.like.add(request.user)
            marker.likes_count += 1
            result = marker.likes_count
            marker.save()
        return JsonResponse(
            {
                "result": result,
            }
        )


def add_comment(request):
    """Add comment to Marker."""
    if request.POST.get("action") == "post":
        marker_id = int(request.POST.get("marker_id"))
        marker = get_object_or_404(Marker, id=marker_id)
        comment_text = request.POST.get("comment_text")
        if request.user.is_authenticated:
            if len(comment_text) >= 10:
                comment = Comment.objects.create(
                    owner=request.user, marker=marker, comment_text=comment_text
                )
                result = marker.comments.all().count()
                comment.save()
                message = _("Comment has added. Reload page.")

                # send email to marker's owner
                if marker.owner:
                    context = {
                        "marker": marker,
                        "comment_text": comment_text,
                    }
                    html_message = render_to_string(
                        template_name="hub/mail/new_comment.html", context=context
                    )
                    send_email(
                        subject="A new comment added to your mark on UAHub",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[marker.owner.email],
                        message=strip_tags(html_message),
                        html_message=html_message,
                    )
            else:
                result = ""
                message = _("Error! Enter at least 10 symbols.")
        else:
            result = ""
            message = _("Sign in to leave a comment")
        return JsonResponse({"result": result, "message": message})


def delete_comment(request):
    """Delete comment from Marker."""
    if request.POST.get("action") == "post":
        comment_id = int(request.POST.get("comment_id"))
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user.is_authenticated and comment.owner == request.user:
            comment.delete()
            message = _("You've deleted the mark. Reload page.")
        else:
            message = _("Error!")
    else:
        message = _("Sign in to delete a comment")
    return JsonResponse({"message": message})
