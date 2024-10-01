"""
Copyright ©2024. The Regents of the University of California (Regents). All Rights Reserved.

Permission to use, copy, modify, and distribute this software and its documentation
for educational, research, and not-for-profit purposes, without fee and without a
signed licensing agreement, is hereby granted, provided that the above copyright
notice, this paragraph and the following two paragraphs appear in all copies,
modifications, and distributions.

Contact The Office of Technology Licensing, UC Berkeley, 2150 Shattuck Avenue,
Suite 510, Berkeley, CA 94720-1620, (510) 643-7201, otl@berkeley.edu,
http://ipira.berkeley.edu/industry-info for commercial licensing opportunities.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE
SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED
"AS IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
ENHANCEMENTS, OR MODIFICATIONS.
"""

from datetime import datetime
import time

from bea.models.department import Department
from bea.pages.page import Page
from bea.test_utils import boa_utils
from bea.test_utils import utils
from flask import current_app as app
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class CreateNoteModal(Page):

    CONFIRM_DELETE_OR_DISCARD = (By.ID, 'are-you-sure-confirm')
    CANCEL_DELETE_OR_DISCARD = (By.ID, 'are-you-sure-cancel')

    def confirm_delete_or_discard(self):
        self.wait_for_element_and_click(self.CONFIRM_DELETE_OR_DISCARD)

    def cancel_delete_or_discard(self):
        self.wait_for_element_and_click(self.CANCEL_DELETE_OR_DISCARD)

    # DRAFT NOTE

    SAVE_AS_DRAFT_BUTTON = By.ID, 'save-as-draft-button'
    UPDATE_DRAFT_BUTTON = By.XPATH, '//button[text()=" Update Draft "]'
    EDIT_DRAFT_HEADING = By.XPATH, '//h3[text()=" Edit Draft Note "]'

    def click_save_as_draft(self):
        app.logger.info('Clicking the save-as-draft button')
        self.wait_for_element_and_click(self.SAVE_AS_DRAFT_BUTTON)
        self.when_not_present(self.SAVE_AS_DRAFT_BUTTON, utils.get_medium_timeout())

    def click_update_note_draft(self):
        app.logger.info('Clicking the update draft button')
        self.wait_for_element_and_click(self.UPDATE_DRAFT_BUTTON)

    # CREATE NOTE, SHARED ELEMENTS

    # Subject

    NEW_NOTE_SUBJECT_INPUT = By.ID, 'create-note-subject'

    def enter_new_note_subject(self, note):
        app.logger.info(f'Entering new note subject {note.subject}')
        self.wait_for_textbox_and_type(self.NEW_NOTE_SUBJECT_INPUT, note.subject)

    EDIT_NOTE_SUBJECT_INPUT = By.ID, 'edit-note-subject'
    SUBJ_REQUIRED_MSG = By.XPATH, '//span[text()="Subject is required"]'

    def enter_edit_note_subject(self, note):
        app.logger.info(f'Entering edited note subject {note.subject}')
        self.wait_for_textbox_and_type(self.EDIT_NOTE_SUBJECT_INPUT, note.subject)

    # Body

    NOTE_BODY_TEXT_AREA = By.XPATH, '(//div[@role="textbox"])[2]'

    def wait_for_note_body_editor(self):
        self.when_present(self.NOTE_BODY_TEXT_AREA, utils.get_short_timeout())

    def enter_note_body(self, note):
        app.logger.info(f'Entering note body {note.body}')
        self.wait_for_note_body_editor()
        self.wait_for_textbox_and_type(self.NOTE_BODY_TEXT_AREA, note.body)

    # Topics

    TOPIC_INPUT = By.ID, 'add-note-topic'
    ADD_TOPIC_SELECT = By.ID, 'add-topic-select-list'
    TOPIC_OPTION = By.XPATH, '//select[@id="add-topic-select-list"]/option'
    TOPIC_REMOVE_BUTTON = By.XPATH, '//li[contains(@id, "remove-note-")]'

    def topic_options(self):
        sel = Select(self.element(self.ADD_TOPIC_SELECT))
        return [el.get_attribute('value') for el in sel.options if el.get_attribute('value')]

    @staticmethod
    def topic_pill(topic):
        return By.XPATH, f'//li[contains(@id, \"-topic\")][contains(., \"{topic.name}\")]'

    @staticmethod
    def new_note_unsaved_topic_remove_btn(topic):
        return By.XPATH, f'//li[contains(@id, \"-topic\")][contains(., \"{topic.name}\")]//button'

    @staticmethod
    def topic_remove_button(note, topic):
        return By.XPATH, f'//span[text()=\"{topic.name}\"]/../following-sibling::div/button'

    def add_topics(self, note, topics):
        for topic in topics:
            app.logger.info(f'Adding topic {topic.name}')
            self.wait_for_select_and_click_option(self.ADD_TOPIC_SELECT, topic.name)
            self.when_present(self.topic_pill(topic), utils.get_short_timeout())
        note.topics += topics

    def remove_topics(self, note, topics):
        current_topics = list(map(lambda t: t.name, note.topics))
        for topic in topics:
            app.logger.info(f'Removing topic {topic.name}')
            if note.record_id:
                self.wait_for_element_and_click(self.topic_remove_button(note, topic))
                self.when_not_visible(self.topic_pill(topic), utils.get_short_timeout())
            else:
                self.wait_for_element_and_click(self.new_note_unsaved_topic_remove_btn(topic))
                self.when_not_visible(self.topic_pill(topic), utils.get_short_timeout())
            if topic.name in current_topics:
                matching_topic = next(filter(lambda t: t.name == topic.name, note.topics))
                note.topics.remove(matching_topic)

    # Attachments

    NEW_NOTE_ATTACH_INPUT = By.XPATH, '//div[@id="new-note-modal-container"]//input[@type="file"]'
    NOTE_ATTACHMENT_SIZE_MSG = By.XPATH, '//div[contains(text(),"Attachments are limited to 20 MB in size.")]'
    NOTE_DUPE_ATTACHMENT_MSG = By.XPATH, '//div[contains(text(),"Another attachment has the name")]'

    @staticmethod
    def new_note_attachment_delete_button(attachment):
        return By.XPATH, f'//button[@aria-label="Remove attachment {attachment.file_name}"]'

    def enter_new_note_attachments(self, file_string):
        self.when_present(self.NEW_NOTE_ATTACH_INPUT, utils.get_short_timeout())
        self.element(self.NEW_NOTE_ATTACH_INPUT).send_keys(file_string)

    def add_attachments_to_new_note(self, note, attachments):
        files = list(map(lambda a: f'{utils.attachments_dir()}/{a.file_name}', attachments))
        files = '\n'.join(files)
        app.logger.info(f'Adding attachments to an unsaved note: {files}')
        self.enter_new_note_attachments(files)
        self.when_visible(self.new_note_attachment_delete_button(attachments[-1]), utils.get_medium_timeout())
        time.sleep(utils.get_click_sleep())
        note.attachments += attachments

    def remove_attachments_from_new_note(self, note, attachments):
        for a in attachments:
            app.logger.info(f'Removing attachment {a.file_name} from an unsaved note')
            self.wait_for_element_and_click(self.new_note_attachment_delete_button(a))
            self.when_not_visible(self.new_note_attachment_delete_button(a), utils.get_short_timeout())
            note.attachments.remove(a)
            note.updated_date = datetime.now()

    SORRY_NO_ATTACHMENT_MSG = By.XPATH, '//body[text()="Sorry, attachment not available."]'

    @staticmethod
    def existing_note_attachment_input(note):
        return By.ID, f'note-{note.record_id}-choose-file-for-note-attachment'

    @staticmethod
    def existing_note_attachment_delete_button(note, attachment):
        return By.XPATH, f'//div[@id=\"note-{note.record_id}-outer\"]//li[contains(., \"{attachment.file_name}\")]//button'

    def add_attachments_to_existing_note(self, note, attachments):
        for a in attachments:
            app.logger.info(f'Adding attachment {a.file_name} to note ID {note.record_id}')
            self.when_present(self.existing_note_attachment_input(note), utils.get_short_timeout())
            self.element(self.existing_note_attachment_input(note)).send_keys(
                f'{utils.attachments_dir()}/{a.file_name}')
            self.when_visible(self.existing_note_attachment_delete_button(note, a), utils.get_medium_timeout())
            time.sleep(utils.get_click_sleep())
            note.updated_date = datetime.now()
            note.attachments.append(a)

    def remove_attachments_from_existing_note(self, note, attachments):
        for a in attachments:
            app.logger.info(f'Removing attachment {a.file_name} from note ID {note.record_id}')
            self.wait_for_element_and_click(self.existing_note_attachment_delete_button(note, a))
            self.confirm_delete_or_discard()
            self.when_not_present(self.existing_note_attachment_delete_button(note, a), utils.get_short_timeout())
            note.attachments.remove(a)
            a.deleted_at = datetime.now()
            note.updated_date = datetime.now()

    # CE3 restricted

    UNIVERSAL_RADIO = By.XPATH, '//input[@id="note-is-not-private-radio-button"]/ancestor::div[contains(@class, "custom-radio")]'
    PRIVATE_RADIO = By.XPATH, '//input[@id="note-is-private-radio-button"]/ancestor::div[contains(@class, "custom-radio")]'

    def set_note_privacy(self, note):
        if note.advisor.depts and Department.ZCEEE.value['name'] in note.advisor.depts:
            if note.is_private:
                app.logger.info('Setting note to private')
                self.wait_for_element_and_click(self.PRIVATE_RADIO)
            else:
                app.logger.info('Setting note to non-private')
                self.wait_for_element_and_click(self.UNIVERSAL_RADIO)
        else:
            app.logger.info(f'Advisor not with CE3, so privacy defaults to {note.is_private}')

    # Contact type

    @staticmethod
    def contact_type(note):
        if note.contact_type:
            return By.XPATH, f'//input[@type="radio"][@value="{note.contact_type}"]'
        else:
            return By.XPATH, '//input[@id="contact-option-none-radio-button"]'

    def select_contact_type(self, note):
        app.logger.info(f'Selecting contact type {note.contact_type}')
        self.wait_for_page_and_click_js(self.contact_type(note))

    # Set date

    SET_DATE_INPUT = By.ID, 'manually-set-date-input'

    def enter_set_date(self, note):
        app.logger.info(f'Entering note set date {note.set_date}')
        date = note.set_date and note.set_date.strftime('%m/%d/%Y')
        if date:
            self.wait_for_textbox_and_type(self.SET_DATE_INPUT, date)
            time.sleep(1)

    # Save

    NEW_NOTE_SAVE_BUTTON = By.ID, 'create-note-button'

    def click_save_new_note(self):
        app.logger.info('Clicking the new note Save button')
        self.wait_for_element_and_click(self.NEW_NOTE_SAVE_BUTTON)

    def set_new_note_id(self, note, student=None):
        start_time = datetime.now()
        tries = 0
        max_tries = 15
        while tries <= max_tries:
            tries += 1
            try:
                results = boa_utils.get_note_ids_by_subject(note, student)
                assert len(results) > 0
                note.record_id = f'{results[0]}'
                break
            except AssertionError:
                if tries == max_tries:
                    raise
                else:
                    time.sleep(1)
        app.logger.info(f'Note ID is {note.record_id}')
        end_time = datetime.now()
        app.logger.info(f'Note was created in {(end_time - start_time).seconds} seconds')
        self.when_not_present(self.NEW_NOTE_SUBJECT_INPUT, utils.get_short_timeout())
        note.created_date = datetime.now()
        note.updated_date = datetime.now()
        return note.record_id

    # Cancel

    NEW_NOTE_CANCEL_BUTTON = By.ID, 'create-note-cancel'

    def click_cancel_new_note(self):
        self.wait_for_element_and_click(self.NEW_NOTE_CANCEL_BUTTON)

    # SID LIST ENTRY

    def enter_sid_list(self, loc, sids):
        app.logger.info(f'Entering SIDs {sids}')
        self.wait_for_textbox_and_type(loc, sids)

    def enter_comma_sep_sids(self, loc, students):
        sids = list(map(lambda s: s.sid, students))
        string = ', '.join(sids)
        self.enter_sid_list(loc, string)

    def enter_line_sep_sids(self, loc, students):
        sids = list(map(lambda s: s.sid, students))
        string = '\n'.join(sids)
        self.enter_sid_list(loc, string)

    def enter_space_sep_sids(self, loc, students):
        sids = list(map(lambda s: s.sid, students))
        string = ' '.join(sids)
        self.enter_sid_list(loc, string)

    # BATCH NOTES

    BATCH_NOTE_BUTTON = By.ID, 'batch-note-button'
    BATCH_NO_STUDENTS_PER_COHORTS = By.ID, 'no-students-per-cohorts-alert'
    BATCH_NO_STUDENTS_PER_GROUPS = By.ID, 'no-students-per-curated-groups-alert'
    BATCH_NO_STUDENTS = By.ID, 'no-students-alert'
    BATCH_STUDENT_COUNT = By.ID, 'target-student-count-alert'
    BATCH_DRAFT_STUDENT_WARNING = By.XPATH, '//span[contains(text(), "but not the associated students")]'

    def click_create_note_batch(self):
        app.logger.info('Clicking the new note batch button')
        self.wait_for_element_and_click(self.BATCH_NOTE_BUTTON)

    # Students

    BATCH_ADD_STUDENT_INPUT = By.ID, 'create-note-add-student-input'
    BATCH_ADD_STUDENTS_BUTTON = By.ID, 'create-note-add-student-add-button'

    def wait_for_student_input(self):
        self.when_present(self.BATCH_ADD_STUDENT_INPUT, utils.get_short_timeout())

    @staticmethod
    def added_student_loc(student):
        return By.XPATH, f'//span[text()="{student.full_name} ({student.sid})"]'

    @staticmethod
    def student_remove_button_loc(student):
        return By.XPATH, f'//button[@aria-label="Remove  {student.full_name} ({student.sid})"]'

    def wait_for_batch_students(self, students):
        for student in students:
            self.when_present(self.added_student_loc(student), 2)

    def add_comma_sep_sids_to_batch(self, students):
        self.enter_comma_sep_sids(self.BATCH_ADD_STUDENT_INPUT, students)
        self.wait_for_element_and_click(self.BATCH_ADD_STUDENTS_BUTTON)
        self.wait_for_batch_students(students)

    def add_line_sep_sids_to_batch(self, students):
        self.enter_line_sep_sids(self.BATCH_ADD_STUDENT_INPUT, students)
        self.wait_for_element_and_click(self.BATCH_ADD_STUDENTS_BUTTON)
        self.wait_for_batch_students(students)

    def add_space_sep_sids_to_batch(self, students):
        self.enter_space_sep_sids(self.BATCH_ADD_STUDENT_INPUT, students)
        self.wait_for_element_and_click(self.BATCH_ADD_STUDENTS_BUTTON)
        self.wait_for_batch_students(students)

    @staticmethod
    def student_auto_suggest_loc(student):
        path = f'//*[contains(., "{student.full_name} ({student.sid})")]'
        return By.XPATH, path

    def add_students_to_batch(self, note_batch, students):
        self.scroll_to_top()
        self.wait_for_element_and_click(self.BATCH_ADD_STUDENT_INPUT)
        for student in students:
            app.logger.info(f'Adding SID {student.sid} to batch note {note_batch.subject}')
            self.enter_chars(self.BATCH_ADD_STUDENT_INPUT, f'{student.sid}')
            self.wait_for_element_and_click(self.student_auto_suggest_loc(student))
            self.append_student_to_batch(note_batch, student)

    def append_student_to_batch(self, note_batch, student):
        self.when_present(self.added_student_loc(student), 3)
        note_batch.students.append(student)

    def remove_students_from_batch(self, note_batch, students):
        for student in students:
            app.logger.info(f'Removing SID {student.sid} from batch note')
            self.scroll_to_top()
            self.wait_for_element_and_click(self.student_remove_button_loc(student))
            self.when_not_present(self.added_student_loc(student), 2)
            if student in note_batch.students:
                note_batch.students.remove(student)

    # Cohorts

    BATCH_COHORT_SELECT = By.ID, 'batch-note-cohort'

    @staticmethod
    def added_cohort_loc(cohort):
        return By.XPATH, f'//span[contains(@id, "batch-note-cohort")][contains(., "{cohort.name}")]'

    @staticmethod
    def cohort_remove_button(cohort):
        return By.ID, f'remove-batch-note-cohort-{cohort.cohort_id}-btn'

    def add_cohorts_to_batch(self, note_batch, cohorts):
        for cohort in cohorts:
            app.logger.info(f'Adding cohort {cohort.name} to batch note {note_batch.subject}')
            self.wait_for_select_and_click_option(self.BATCH_COHORT_SELECT, cohort.name)
            self.when_present(self.added_cohort_loc(cohort), utils.get_short_timeout())
            note_batch.cohorts.append(cohort)

    def remove_cohorts_from_batch(self, note_batch, cohorts):
        for cohort in cohorts:
            app.logger.info(f'Removing cohort {cohort.name} from batch note')
            self.wait_for_element_and_click(self.cohort_remove_button(cohort))
            self.when_not_present(self.added_cohort_loc(cohort), 2)
            if cohort in note_batch.cohorts:
                note_batch.cohorts.remove(cohort)

    # Groups

    BATCH_GROUP_SELECT = By.ID, 'batch-note-curated'

    @staticmethod
    def added_group_loc(group):
        return By.XPATH, f'//span[contains(@id, "batch-note-curated")][contains(., "{group.name}")]'

    @staticmethod
    def group_remove_button(group):
        return By.ID, f'remove-batch-note-curated-{group.cohort_id}-btn'

    def add_groups_to_batch(self, note_batch, groups):
        for group in groups:
            app.logger.info(f'Adding group {group.name} to batch note {note_batch.subject}')
            self.wait_for_select_and_click_option(self.BATCH_GROUP_SELECT, group.name)
            self.when_present(self.added_group_loc(group), utils.get_short_timeout())
            note_batch.groups.append(group)

    def remove_groups_from_batch(self, note_batch, groups):
        for group in groups:
            app.logger.info(f'Removing group {group.name} from batch note')
            self.wait_for_element_and_click(self.group_remove_button(group))
            self.when_not_present(self.added_group_loc(group), 2)
            if group in note_batch.groups:
                note_batch.groups.remove(group)

    # Create

    def verify_batch_note_alert(self, students, cohorts, groups):
        count = len(self.unique_students_in_batch(students, cohorts, groups))
        visible_alert = self.el_text_if_exists(self.BATCH_STUDENT_COUNT)
        utils.assert_actual_includes_expected(visible_alert, f'{count} student record')
        if count >= 500:
            utils.assert_actual_includes_expected(visible_alert, 'Are you sure')

    def create_note_batch(self, note_batch, students, cohorts, groups, topics, attachments):
        app.logger.info(f'Creating note batch with {len(students)} students, {len(cohorts)} cohorts, {len(groups)} groups')
        self.click_create_note_batch()
        # TODO - remove the following once the auto-suggest behaves itself
        self.add_space_sep_sids_to_batch(students)
        for student in students:
            self.append_student_to_batch(note_batch, student)
        # TODO - use the following once the auto-suggest behaves itself
        # self.add_students_to_batch(note_batch, students)
        self.add_cohorts_to_batch(note_batch, cohorts)
        self.add_groups_to_batch(note_batch, groups)
        self.enter_new_note_subject(note_batch)
        self.enter_note_body(note_batch)
        if attachments:
            self.add_attachments_to_new_note(note_batch, attachments)
        if topics:
            self.add_topics(note_batch, topics)
        self.set_note_privacy(note_batch)
        self.click_save_new_note()
        time.sleep(utils.get_click_sleep())
        return self.unique_students_in_batch(students, cohorts, groups)

    @staticmethod
    def unique_students_in_batch(students, cohorts, groups):
        uniques = []
        uniques.extend(students)
        for cohort in cohorts:
            for member in cohort.members:
                if member not in uniques:
                    uniques.append(member)
        for group in groups:
            for member in group.members:
                if member not in uniques:
                    uniques.append(member)
        return uniques