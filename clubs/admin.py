from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
from django.template import Context

from . import models
from . import email
import teach.admin as teach_admin

# http://djangotricks.blogspot.com/2013/12/how-to-export-data-as-excel.html
def export_csv(modeladmin, request, queryset):
    import csv
    from django.http import HttpResponse
    from django.conf import settings
    from django.utils.encoding import smart_str
    from django.core.urlresolvers import reverse

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=clubs.csv'
    writer = csv.writer(response, csv.excel)
    # BOM (optional...Excel needs it to open UTF-8 file properly)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"Name"),
        smart_str(u"Location"),
        smart_str(u"Email"),
        smart_str(u"Description"),
        smart_str(u"Admin URL")
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.name),
            smart_str(obj.location),
            smart_str(obj.owner.email),
            smart_str(obj.description),
            '%s%s' % (settings.ORIGIN,
                      reverse('admin:clubs_club_change', args=[obj.pk]))
        ])
    return response

export_csv.short_description = u"Export CSV"

def owner_email(obj):
    return obj.owner.email

class ClubAdmin(admin.ModelAdmin):
    actions = [export_csv]
    list_display = ('name', 'location', 'created', 'modified', 'owner',
                    owner_email, 'status', 'denial', 'is_active',)
    list_filter = ('status', 'denial', 'is_active',)
    readonly_fields = (owner_email,)

    def save_model(self, request, obj, form, change):
        # Even though the context is empty (normally it contains a dict with
        # placeholder replacements to occur in the template), Django 1.7 needs
        # a context parameter passed in mandatorily.
        context = Context()
        super(ClubAdmin, self).save_model(request, obj, form, change)
        approve_mail, decline_mail = email.approve_club, email.decline_club

        if obj.status == models.Club.APPROVED:
            send_mail(
                subject=approve_mail.plaintext.subject.render(context),
                message=approve_mail.plaintext.body.render(context),
                html_message=approve_mail.html.body.render(context),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=settings.TEACH_STAFF_EMAILS,
                # We don't want send failure to prevent a success response.
                fail_silently=True,
            )
        # We only care about the "unqualified" case for denied clubs
        elif obj.status == models.Club.DENIED and obj.denial == models.Club.UNQUALIFIED:
            send_mail(
                subject=decline_mail.plaintext.subject.render(context),
                message=decline_mail.plaintext.body.render(context),
                html_message=decline_mail.html.body.render(context),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=settings.TEACH_STAFF_EMAILS,
                # We don't want send failure to prevent a success response.
                fail_silently=True,
            )

teach_admin.site.register(models.Club, ClubAdmin)
