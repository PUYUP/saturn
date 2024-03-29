from django.utils.translation import ugettext_lazy as _

# STATUS
PENDING = 'pending'
REVIEWED = 'reviewed'
PUBLISHED = 'published'
RETURNED = 'returned'
REJECTED = 'rejected'
DRAFT = 'draft'
STATUS_CHOICES = (
    (PENDING, _("Tertunda")),
    (REVIEWED, _("Ditinjau")),
    (PUBLISHED, _("Terbit")),
    (RETURNED, _("Dikembalikan")),
    (REJECTED, _("Ditolak")),
    (DRAFT, _("Konsep")),
)


# ACCESS
PUBLIC = 'public'
PRIVATE = 'private'
ACCESS_CHOICES = (
    (PUBLIC, _("Terbuka")),
    (PRIVATE, _("Tertutup")),
)
