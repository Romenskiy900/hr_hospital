from odoo import models
from odoo.exceptions import ValidationError


class UniqueFieldMixin(models.AbstractModel):
    """Abstract mixin that enforces uniqueness of a given field value."""

    _name = 'unique.field.mixin'
    _description = 'Unique Field Mixin'

    def _check_unique_field_mixin(self, vals, field_name):
        """Validate that a field value is unique before create/write."""
        if field_name not in vals:
            return vals

        value = vals[field_name]

        domain = [(field_name, '=', value)]

        if self.ids:
            domain.append(('id', 'not in', self.ids))

        existing = self.search(domain, limit=1)

        if existing:
            raise ValidationError(
                f"Запис з таким значенням '{value}' вже існує!"
            )

        return vals