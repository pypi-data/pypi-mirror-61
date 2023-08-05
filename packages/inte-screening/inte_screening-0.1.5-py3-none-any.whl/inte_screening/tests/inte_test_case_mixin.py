from dateutil.relativedelta import relativedelta
from django.contrib.sites.models import Site
from edc_appointment.constants import IN_PROGRESS_APPT
from edc_appointment.models import Appointment
from edc_auth.group_permissions_updater import GroupPermissionsUpdater
from edc_constants.constants import YES, NOT_APPLICABLE, RANDOM_SAMPLING, MALE, NO
from edc_facility.import_holidays import import_holidays
from edc_facility.models import Holiday
from edc_list_data.site_list_data import site_list_data
from edc_randomization.randomization_list_importer import RandomizationListImporter
from edc_sites import add_or_update_django_sites
from edc_sites.tests.site_test_case_mixin import SiteTestCaseMixin
from edc_utils.date import get_utcnow
from edc_visit_tracking.constants import SCHEDULED
from inte_auth.codenames_by_group import get_codenames_by_group
from inte_sites.sites import fqdn, inte_sites
from inte_subject.models import SubjectVisit
from inte_visit_schedule.constants import DAY1
from model_bakery import baker

from ..models import SubjectScreening
from ..forms import SubjectScreeningForm
from ..constants import NCD_CLINIC


class InteTestCaseMixin(SiteTestCaseMixin):
    fqdn = fqdn

    default_sites = inte_sites

    site_names = [s[1] for s in default_sites]

    import_randomization_list = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        import_holidays(test=True)
        add_or_update_django_sites(sites=inte_sites, fqdn=fqdn)
        site_list_data.autodiscover()
        GroupPermissionsUpdater(
            codenames_by_group=get_codenames_by_group(), verbose=True
        )
        if cls.import_randomization_list:
            RandomizationListImporter(verbose=False, name="default")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        Holiday.objects.all().delete()

    def get_subject_screening(self, report_datetime=None, eligibility_datetime=None):
        data = {
            "screening_consent": YES,
            "selection_method": RANDOM_SAMPLING,
            "report_datetime": report_datetime or get_utcnow(),
            "initials": "EW",
            "gender": MALE,
            "age_in_years": 25,
            "hospital_identifier": "13343322",
            "clinic_type": NCD_CLINIC,
            "qualifying_condition": YES,
            "lives_nearby": YES,
            "requires_acute_care": NO,
            "unsuitable_for_study": NO,
            "unsuitable_agreed": NOT_APPLICABLE,
        }

        form = SubjectScreeningForm(data=data, instance=None)
        form.save()

        subject_screening = SubjectScreening.objects.get(
            screening_identifier=form.instance.screening_identifier
        )

        self.assertTrue(subject_screening.eligible)

        if eligibility_datetime:
            subject_screening.eligibility_datetime = eligibility_datetime
            subject_screening.save()

        return subject_screening

    def get_subject_consent(self, subject_screening, site_name=None):
        site_name = site_name or "kinoni"
        return baker.make_recipe(
            "inte_consent.subjectconsent",
            user_created="erikvw",
            user_modified="erikvw",
            screening_identifier=subject_screening.screening_identifier,
            initials=subject_screening.initials,
            dob=get_utcnow().date()
            - relativedelta(years=subject_screening.age_in_years),
            site=Site.objects.get(name=site_name),
        )

    def get_subject_visit(self, visit_code=None):
        visit_code = visit_code or DAY1
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        subject_identifier = subject_consent.subject_identifier

        appointment = Appointment.objects.get(
            subject_identifier=subject_identifier, visit_code=visit_code
        )
        appointment.appt_status = IN_PROGRESS_APPT
        appointment.save()
        return SubjectVisit.objects.create(appointment=appointment, reason=SCHEDULED)
