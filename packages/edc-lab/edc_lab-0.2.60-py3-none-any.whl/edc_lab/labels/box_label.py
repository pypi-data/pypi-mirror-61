from django.apps import apps as django_apps

from .base_label import BaseLabel


class BoxLabel(BaseLabel):

    model = "edc_lab.box"
    template_name = "box"

    @property
    def label_context(self):
        edc_protocol_app_config = django_apps.get_app_config("edc_protocol")
        return {
            "barcode_value": self.model_obj.box_identifier,
            "box_identifier": self.model_obj.human_readable_identifier,
            "box_name": self.model_obj.name,
            "protocol": edc_protocol_app_config.protocol,
            "site": str(self.model_obj.site.id),
            "box_datetime": self.model_obj.box_datetime.strftime("%Y-%m-%d %H:%M"),
            "category": self.model_obj.get_category_display().upper(),
            "specimen_types": self.model_obj.specimen_types,
            "site_name": str(self.model_obj.site.siteprofile.title),
        }
