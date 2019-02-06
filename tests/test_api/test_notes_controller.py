"""
Copyright ©2019. The Regents of the University of California (Regents). All Rights Reserved.

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

coe_advisor = '1133399'


class TestGetNotes:

    def test_not_authenticated(self, client):
        """Returns 401 if not authenticated."""
        assert client.get('/api/notes/student/11667051').status_code == 401

    def test_notes_for_sid(self, fake_auth, client):
        """Returns advising notes per SID."""
        fake_auth.login(coe_advisor)
        response = client.get('/api/notes/student/11667051')
        assert response.status_code == 200

    def test_get_note_by_id(self, fake_auth, client):
        """Returns advising notes per SID."""
        fake_auth.login(coe_advisor)
        response = client.get('/api/notes/123')
        assert response.status_code == 200


class TestUpdateNotes:

    def test_not_authenticated(self, client):
        """Returns 401 if not authenticated."""
        assert client.post('/api/notes/was_read/123').status_code == 401

    def test_note_was_read(self, fake_auth, client):
        """Returns advising notes per SID."""
        fake_auth.login(coe_advisor)
        response = client.post('/api/notes/was_read/123')
        assert response.status_code == 200
        assert int(response.json['noteId']) == 123
