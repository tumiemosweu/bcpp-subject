from datetime import date
from dateutil.relativedelta import relativedelta

from django.apps import apps as django_apps
from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_consent.field_mixins.bw import IdentityFieldsMixin
from edc_consent.field_mixins import (
    ReviewFieldsMixin, PersonalFieldsMixin, VulnerabilityFieldsMixin,
    SampleCollectionFieldsMixin, CitizenFieldsMixin)
from edc_consent.managers import ObjectConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import YES, NO
from edc_offstudy.model_mixins import OffstudyMixin

from member.models import EnrollmentChecklist
from member.models.household_member import HouseholdMember

from bcpp_subject.models.model_mixins import SurveyModelMixin
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_base.model.models.url_mixin import UrlMixin
from edc_identifier.subject_identifier import SubjectIdentifier
from bcpp_subject.exceptions import ConsentValidationError


def is_minor(dob, reference_datetime):
    # TODO: fix this
    age_at_consent = relativedelta(
        date(reference_datetime.year,
             reference_datetime.month,
             reference_datetime.day),
        dob).years
    return age_at_consent >= 16 and age_at_consent <= 17


class SubjectIdentifierMixin(models.Model):

    def save(self, *args, **kwargs):
        if not self.id:
            try:
                RegisteredSubject = django_apps.get_app_config('edc_registration').model
                registered_subject = RegisteredSubject.objects.get(identity=self.identity)
                self.subject_identifier = registered_subject.subject_identifier
            except RegisteredSubject.DoesNotExist:
                maternal_identifier = SubjectIdentifier(
                    subject_type_name='subject',
                    model=self._meta.label_lower,
                    study_site=self.study_site,
                    create_registration=False)
                self.subject_identifier = maternal_identifier.identifier
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class SubjectConsent(
        ConsentModelMixin, SubjectIdentifierMixin, UpdatesOrCreatesRegistrationModelMixin, SurveyModelMixin,
        OffstudyMixin, IdentityFieldsMixin, ReviewFieldsMixin,
        PersonalFieldsMixin, SampleCollectionFieldsMixin, CitizenFieldsMixin, VulnerabilityFieldsMixin,
        UrlMixin, BaseUuidModel):

    """ A model completed by the user that captures the ICF."""

    household_member = models.ForeignKey(HouseholdMember, on_delete=models.PROTECT)

    is_minor = models.CharField(
        verbose_name=("Is subject a minor?"),
        max_length=10,
        null=True,
        blank=False,
        default='-',
        choices=YES_NO,
        help_text=('Subject is a minor if aged 16-17. A guardian must be present for consent. '
                   'HIV status may NOT be revealed in the household.'),
        editable=False)

    is_signed = models.BooleanField(default=False, editable=False)

    objects = ObjectConsentManager()

    history = HistoricalRecords()

    def __str__(self):
        return '{0} ({1}) V{2}'.format(self.subject_identifier, self.survey, self.version)

    def common_clean(self):
        # confirm member is eligible
        if not self.household_member.eligible_subject:
            raise ConsentValidationError('Member is not eligible for consent')
        # validate dob with HicEnrollment, if it exists
        HicEnrollment = django_apps.get_model('bcpp_subject', 'HicEnrollment')
        try:
            HicEnrollment.objects.get(subject_visit__household_member=self.household_member)
            if self.dob != self.dob:
                raise ConsentValidationError(
                    'Date of birth does not match with that on \'{}\'. Please correct.'.format(
                        HicEnrollment._meta.verbose_name))
        except HicEnrollment.DoesNotExist:
            pass
        # match with enrollment checklist.
        try:
            enrollment_checklist = EnrollmentChecklist.objects.get(
                household_member=self.household_member, is_eligible=True)
        except EnrollmentChecklist.DoesNotExist:
            raise ConsentValidationError(
                'Member has not completed the \'{}\'. Please correct before continuing'.format(
                    EnrollmentChecklist._meta.verbose_name))
        # other form validations
        # match DoB
        if enrollment_checklist.dob != self.dob:
            raise ConsentValidationError(
                'DoB mismatch. DoB does not match with that on \'{}\''.format(
                    EnrollmentChecklist._meta.verbose_name))
        # match gender
        if enrollment_checklist.gender != self.gender:
            raise exception_cls(
                'Gender mismatch. Gender does not match \'{}\''.format(
                    EnrollmentChecklist._meta.verbose_name))
        # minor and guardian name
        if is_minor(self, self.consent_datetime):
            if enrollment_checklist.guardian != YES or not self.guardian_name:
                raise ConsentValidationError(
                    'Enrollment Checklist indicates that subject is a minor with guardian '
                    'available, but the consent does not indicate this.')
        # match initials
        if not self.household_member.personal_details_changed == YES:
            if enrollment_checklist.initials != self.initials:
                raise ConsentValidationError('Initials mismatch. Initials do not match \'{}\''.format(
                    EnrollmentChecklist._meta.verbose_name))
        # match citizenship
        if enrollment_checklist.citizen != self.citizen:
            raise ConsentValidationError(
                'Citizenship mismatch. Citizenship does not match \'{}\''.format(
                    EnrollmentChecklist._meta.verbose_name))
        # match literacy
        if (enrollment_checklist.literacy == YES and
                not (self.is_literate == YES or (self.is_literate == NO) and
                     self.witness_name)):
            raise ConsentValidationError(
                'Literacy mismatch. Answer to whether this subject is literate/not literate but with a '
                'literate witness, does not match \'{}\''.format(
                    EnrollmentChecklist._meta.verbose_name))
        # match marriage if not citizen
        if self.citizen == NO:
            if (enrollment_checklist.legal_marriage != self.legal_marriage) or ( 
                    enrollment_checklist.marriage_certificate != self.marriage_certificate):
                raise ConsentValidationError(
                    'Citizenship by marriage mismatch. Answer indicates that this subject is married '
                    'to a citizen with a valid marriage certificate. This does not match \'{}\''.format(
                        EnrollmentChecklist._meta.verbose_name))
        super().common_clean()

    def save(self, *args, **kwargs):
        self.is_minor = YES if is_minor(self, self.consent_datetime) else NO
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_subject'
        get_latest_by = 'consent_datetime'
        unique_together = (('subject_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
        ordering = ('-created', )
