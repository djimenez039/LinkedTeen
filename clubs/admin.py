from django.contrib import admin
from .models import Club, ClubAnnouncement, ClubMembership, ClubPost


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
	search_fields = ('name',)


@admin.register(ClubMembership)
class ClubMembershipAdmin(admin.ModelAdmin):
	list_display = ('club', 'student', 'role', 'joined_at')
	list_filter = ('role', 'club')
	search_fields = ('club__name', 'student__username', 'student__email')


admin.site.register(ClubAnnouncement)
admin.site.register(ClubPost)
