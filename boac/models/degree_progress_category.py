"""
Copyright ©2021. The Regents of the University of California (Regents). All Rights Reserved.

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

from boac import db, std_commit
from boac.models.base import Base
from boac.models.degree_progress_course_unit_requirement import DegreeProgressCourseUnitRequirement
from dateutil.tz import tzutc
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import asc

degree_progress_category_type = ENUM(
    'Category',
    'Subcategory',
    'Course',
    name='degree_progress_category_types',
    create_type=False,
)


class DegreeProgressCategory(Base):
    __tablename__ = 'degree_progress_categories'

    id = db.Column(db.Integer, nullable=False, primary_key=True)  # noqa: A003
    category_type = db.Column(degree_progress_category_type, nullable=False)
    course_units = db.Column(db.Integer)
    description = db.Column(db.Text)
    name = db.Column(db.String(255), nullable=False)
    parent_category_id = db.Column(db.Integer, db.ForeignKey('degree_progress_categories.id'))
    position = db.Column(db.Integer, nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('degree_progress_templates.id'), nullable=False)
    unit_requirements = db.relationship(
        DegreeProgressCourseUnitRequirement.__name__,
        back_populates='category',
        lazy='joined',
    )

    def __init__(
            self,
            category_type,
            name,
            position,
            template_id,
            course_units=None,
            description=None,
            parent_category_id=None,
    ):
        self.category_type = category_type
        self.course_units = course_units
        self.description = description
        self.name = name
        self.parent_category_id = parent_category_id
        self.position = position
        self.template_id = template_id

    def __repr__(self):
        return f"""<DegreeProgressCategory id={self.id},
                    category_type={self.category_type},
                    course_units={self.course_units},
                    description={self.description},
                    name={self.name},
                    parent_category_id={self.parent_category_id},
                    position={self.position},
                    template_id={self.template_id},
                    created_at={self.created_at},
                    updated_at={self.updated_at}>"""

    @classmethod
    def create(
            cls,
            category_type,
            name,
            position,
            template_id,
            course_units=None,
            description=None,
            parent_category_id=None,
            unit_requirement_ids=None,
    ):
        category = cls(
            category_type=category_type,
            course_units=course_units,
            description=description,
            name=name,
            parent_category_id=parent_category_id,
            position=position,
            template_id=template_id,
        )
        # TODO: Use 'unit_requirement_ids' in mapping this instance to 'unit_requirements' table
        db.session.add(category)
        std_commit()
        for unit_requirement_id in unit_requirement_ids or []:
            DegreeProgressCourseUnitRequirement.create(
                category_id=category.id,
                unit_requirement_id=int(unit_requirement_id),
            )
        return category

    @classmethod
    def delete(cls, category_id):
        category = cls.query.filter_by(id=category_id).first()
        db.session.delete(category)
        std_commit()

    @classmethod
    def find_by_id(cls, category_id):
        return cls.query.filter_by(id=category_id).first()

    @classmethod
    def get_categories(cls, template_id):
        hierarchy = []
        categories = []
        for category in cls.query.filter_by(template_id=template_id).order_by(asc(cls.created_at)).all():
            categories.append({
                **category.to_api_json(),
                'children': [],
            })
        categories_by_id = dict((category['id'], category) for category in categories)
        for category in categories:
            parent_category_id = category['parentCategoryId']
            if parent_category_id:
                parent = categories_by_id[parent_category_id]
                parent['children'].append(category)
            else:
                hierarchy.append(category)

        return hierarchy

    def to_api_json(self):
        unit_requirements_json = [m.unit_requirement.to_api_json() for m in (self.unit_requirements or [])]
        return {
            'id': self.id,
            'categoryType': self.category_type,
            'courseUnits': self.course_units,
            'createdAt': _isoformat(self.created_at),
            'description': self.description,
            'name': self.name,
            'parentCategoryId': self.parent_category_id,
            'position': self.position,
            'templateId': self.template_id,
            'unitRequirements': unit_requirements_json,
            'updatedAt': _isoformat(self.updated_at),
        }


def _isoformat(value):
    return value and value.astimezone(tzutc()).isoformat()
