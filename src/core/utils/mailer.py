import os
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPException
from ssl import create_default_context

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.settings import settings

# Configure Jinja2
template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
env = Environment(
    loader=FileSystemLoader(template_dir), autoescape=select_autoescape(["html", "xml"])
)


def render_template(template_name: str, **kwargs) -> str:
    template = env.get_template(template_name)
    return template.render(**kwargs)


def send_email(to_email: str, subject: str, template_name: str, **kwargs):
    body = render_template(template_name, **kwargs)

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = settings.MAIL_USERNAME
    msg["To"] = to_email

    context = create_default_context()

    try:
        with SMTP(settings.MAIL_HOST, settings.MAIL_PORT) as server:
            server.starttls(context=context)
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            server.sendmail(settings.MAIL_USERNAME, to_email, msg.as_string())
            server.quit()
        print(f"Email sent to {to_email}")
    except SMTPException as e:
        print(f"Error sending email: {e}")
        raise Exception("Error sending email")
