import logging
import socket

from flask import Blueprint
from flask.views import MethodView

import ckan.lib.navl.dictization_functions as dictization_functions
import ckan.logic as logic
import ckan.lib.mailer as mailer
from ckan.plugins import toolkit as tk

from ckanext.nmwd_theme.helpers import validate_contact_form


nmwd = Blueprint("nmwd", __name__)
logger = logging.getLogger(__name__)


base_render = tk.render


def map():
    return base_render("map.html")


def team():
    return base_render("team.html")


def news():
    return base_render("news.html")


def faq():
    return base_render("faq.html")


class ContactFormView(MethodView):
    def get(self, data=None, errors=None, error_summary=None):
        form_vars = {
            u'data': data or {},
            u'errors': errors or {},
            u'error_summary': error_summary or {}
        }
        return base_render("contact.html", extra_vars=form_vars)

    def post(self):
        data_dict = logic.clean_dict(
            dictization_functions.unflatten(
                logic.tuplize_dict(logic.parse_params(tk.request.form))
            )
        )
 
        data, errors, error_summary = validate_contact_form(data_dict)
        if errors:
            return self.get(data, errors, error_summary)

        sender = data.get("email", "").strip()
        recipients = tk.config.get('email_to', '')
        subject = "Message from newmexicowaterdata.org contact form"

        f_name = data.get("firstname", "").strip()
        l_name = data.get("lastname", "").strip()
        body = data.get("message", "").strip()

        body_parts = [
            f'{body}\n',
            'Sent by:',
            f'Name: {f_name + " " + l_name}',
            f'Email: {sender}',
        ]

        mail_dict = {
            'recipient_email': recipients,
            'recipient_name': tk.config.get('ckan.site_title'),
            'subject': subject,
            'body': '\n'.join(body_parts),
            'headers': {'reply-to': sender},
        }

        # note the pop here so that we don't get parameter clashes when we call
        # mail_recipient below
        email = mail_dict.pop('recipient_email')
        name = mail_dict.pop('recipient_name')

        try:
            mailer.mail_recipient(name, email, **mail_dict)
        except (mailer.MailerException, socket.error) as e:
            tk.h.flash_error(e.args[0])
            return self.get(data_dict)

        return base_render("success.html")


def reports():
    return base_render("reports.html")


def photos():
    return base_render("photos.html")


def events():
    return base_render("events.html")


nmwd.add_url_rule("/map", view_func=map)
nmwd.add_url_rule("/team", view_func=team)
nmwd.add_url_rule("/news", view_func=news)
nmwd.add_url_rule("/faq", view_func=faq)
nmwd.add_url_rule(
    "/contact",
    view_func=ContactFormView.as_view(str("contact")),
    methods=("GET", "POST"),
)
nmwd.add_url_rule("/reports", view_func=reports)
nmwd.add_url_rule("/photos", view_func=photos)
nmwd.add_url_rule("/events", view_func=events)


def get_blueprints():
    return [nmwd]
