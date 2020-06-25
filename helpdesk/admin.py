from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from helpdesk.models import Queue, Ticket, FollowUp, PreSetReply, KBCategory, TicketSpentTime, TicketCategory, \
    TicketType
from helpdesk.models import EscalationExclusion, EmailTemplate, KBItem
from helpdesk.models import TicketChange, Attachment, IgnoreEmail
from helpdesk.models import CustomField


@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'email_address', 'locale')
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ('default_owner',)


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(TicketType)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'mandatory_facturation')
    search_fields = ('name',)
    list_filter = ('mandatory_facturation',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'status', 'assigned_to', 'queue', 'submitter_email', 'category', 'type', 'billing', 'on_hold'
    )
    date_hierarchy = 'created'
    list_filter = ('queue', 'status', 'priority', 'category', 'type', 'billing', 'on_hold')
    search_fields = (
        'id', 'title', 'description', 'category__name', 'type__name', 'submitter_email',
        'assigned_to__username', 'assigned_to__first_name', 'assigned_to__last_name'
    )
    autocomplete_fields = (
        'assigned_to', 'customer_contact', 'customer', 'site', 'customer_product', 'category', 'type'
    )
    list_select_related = ('queue', 'assigned_to', 'category', 'type')

    def hidden_submitter_email(self, ticket):
        if ticket.submitter_email:
            username, domain = ticket.submitter_email.split("@")
            username = username[:2] + "*" * (len(username) - 2)
            domain = domain[:1] + "*" * (len(domain) - 2) + domain[-1:]
            return "%s@%s" % (username, domain)
        else:
            return ticket.submitter_email
    hidden_submitter_email.short_description = _('Submitter E-Mail')


class TicketChangeInline(admin.StackedInline):
    model = TicketChange


class AttachmentInline(admin.StackedInline):
    model = Attachment


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    inlines = [TicketChangeInline, AttachmentInline]
    list_display = ('ticket_get_ticket_for_url', 'title', 'date', 'ticket', 'user', 'new_status')
    list_filter = ('new_status', 'public')
    autocomplete_fields = ('user', 'ticket')
    date_hierarchy = 'date'
    search_fields = ('ticket__id', 'title', 'comment')
    list_select_related = ('ticket__queue', 'user')

    def ticket_get_ticket_for_url(self, obj):
        return obj.ticket.ticket_for_url
    ticket_get_ticket_for_url.short_description = _('Slug')


@admin.register(KBCategory)
class KBCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(KBItem)
class KBItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'last_updated', 'votes')
    date_hierarchy = 'last_updated'
    list_display_links = ('title',)
    list_filter = ('category',)
    search_fields = ('title', 'question', 'answer')


@admin.register(CustomField)
class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'data_type')
    list_filter = ('data_type',)


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_name', 'heading', 'locale')
    list_filter = ('locale', )


@admin.register(IgnoreEmail)
class IgnoreEmailAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'queue_list', 'email_address', 'keep_in_mailbox')
    date_hierarchy = 'date'
    list_filter = ('keep_in_mailbox',)


@admin.register(TicketSpentTime)
class TicketSpentTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'employee', 'start_date', 'duration', 'end_date', 'status', 'comment')
    list_filter = ('status',)
    search_fields = (
        'employee__user__username', 'employee__user__first_name', 'employee__user_last_name', 'comment',
        'ticket__id'
    )
    date_hierarchy = 'start_date'
    autocomplete_fields = ('ticket', 'employee')
    list_select_related = ('ticket', 'employee__user')


admin.site.register(PreSetReply)
admin.site.register(EscalationExclusion)
