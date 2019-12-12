/**
 * Copyright ©2020. The Regents of the University of California (Regents). All Rights Reserved.
 *
 * Permission to use, copy, modify, and distribute this software and its documentation
 * for educational, research, and not-for-profit purposes, without fee and without a
 * signed licensing agreement, is hereby granted, provided that the above copyright
 * notice, this paragraph and the following two paragraphs appear in all copies,
 * modifications, and distributions.
 *
 * Contact The Office of Technology Licensing, UC Berkeley, 2150 Shattuck Avenue,
 * Suite 510, Berkeley, CA 94720-1620, (510) 643-7201, otl@berkeley.edu,
 * http://ipira.berkeley.edu/industry-info for commercial licensing opportunities.
 *
 * IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
 * INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
 * THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE
 * SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED
 * "AS IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
 * ENHANCEMENTS, OR MODIFICATIONS.
 */

BEGIN;

CREATE TABLE alerts (
  id SERIAL NOT NULL,
  sid VARCHAR(80) NOT NULL REFERENCES students (sid) ON DELETE CASCADE,
  alert_type VARCHAR(80) NOT NULL,
  key VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  active BOOLEAN DEFAULT TRUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL,

  PRIMARY KEY (id)
);

CREATE INDEX alerts_key_idx ON alerts (key);
CREATE INDEX alerts_sid_idx ON alerts (sid);

ALTER TABLE alerts ADD CONSTRAINT alerts_sid_alert_type_key_unique_constraint UNIQUE (sid, alert_type, key);

CREATE TABLE alert_views (
  alert_id INTEGER NOT NULL REFERENCES alerts (id) ON DELETE CASCADE,
  viewer_id INTEGER NOT NULL REFERENCES authorized_users (id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL,
  dismissed_at TIMESTAMP WITH TIME ZONE,

  PRIMARY KEY (alert_id, viewer_id)
);

CREATE INDEX alert_views_alert_id_idx ON alert_views (alert_id);
CREATE INDEX alert_views_viewer_id_idx ON alert_views (viewer_id);

COMMIT;
