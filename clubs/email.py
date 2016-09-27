from django.template.loader import get_template


class EmailTemplateContents:
    pass


class EmailTemplate:
    def __init__(
        self,
        plaintext_subject='',
        plaintext_body='',
        html_body=None,
    ):
        self.plaintext = EmailTemplateContents()
        self.plaintext.subject = plaintext_subject
        self.plaintext.body = plaintext_body
        self.html = EmailTemplateContents()
        self.html.body = html_body


create_club = EmailTemplate(
    plaintext_subject=get_template('clubs/email/create_club_user/subject.txt'),
    plaintext_body=get_template('clubs/email/create_club_user/body.txt'),
)

create_club_staff = EmailTemplate(
    plaintext_subject=get_template('clubs/email/create_club_staff/subject.txt'),
    plaintext_body=get_template('clubs/email/create_club_staff/body.txt'),
)

approve_club = EmailTemplate(
    plaintext_subject=get_template('clubs/email/approve_club/subject.txt'),
    plaintext_body=get_template('clubs/email/approve_club/body.txt'),
    html_body=get_template('clubs/email/approve_club/body.html'),
)

decline_club = EmailTemplate(
    plaintext_subject=get_template('clubs/email/decline_club/subject.txt'),
    plaintext_body=get_template('clubs/email/decline_club/body.txt'),
    html_body=get_template('clubs/email/decline_club/body.html'),
)
