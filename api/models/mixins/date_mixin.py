from django.db import models


class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    is_deleted = models.BooleanField(db_index=True, default=False)

    class Meta:
        abstract = True

    def additional_deleted_actions(self):
        pass

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(DateMixin, self).save(force_insert, force_update, using, update_fields)
        if self.is_deleted:
            self.additional_deleted_actions()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()
