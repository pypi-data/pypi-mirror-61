# ##############################################################################
#  Author: echel0n <echel0n@sickrage.ca>
#  URL: https://sickrage.ca/
#  Git: https://git.sickrage.ca/SiCKRAGE/sickrage.git
#  -
#  This file is part of SiCKRAGE.
#  -
#  SiCKRAGE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  -
#  SiCKRAGE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  -
#  You should have received a copy of the GNU General Public License
#  along with SiCKRAGE.  If not, see <http://www.gnu.org/licenses/>.
# ##############################################################################

import sickrage


def find_show(indexer_id, indexer=1):
    from sickrage.core import MainDB
    from sickrage.core.tv.show import TVShow
    session = sickrage.app.main_db.session()
    query = session.query(MainDB.TVShow).with_entities(MainDB.TVShow.indexer_id, MainDB.TVShow.indexer).filter_by(indexer_id=indexer_id,
                                                                                                                  indexer=indexer).one_or_none()
    if query:
        return TVShow(query.indexer_id, query.indexer)


def find_show_by_name(term):
    from sickrage.core import MainDB
    from sickrage.core.tv.show import TVShow
    session = sickrage.app.main_db.session()
    query = session.query(MainDB.TVShow).with_entities(MainDB.TVShow.indexer_id, MainDB.TVShow.indexer). \
        filter(MainDB.TVShow.name.like('%{}%'.format(term))).one_or_none()
    if query:
        return TVShow(query.indexer_id, query.indexer)


def find_show_by_location(location):
    from sickrage.core import MainDB
    from sickrage.core.tv.show import TVShow
    session = sickrage.app.main_db.session()
    query = session.query(MainDB.TVShow).with_entities(MainDB.TVShow.indexer_id, MainDB.TVShow.indexer).filter_by(location=location).one_or_none()
    if query:
        return TVShow(query.indexer_id, query.indexer)


def get_show_list():
    from sickrage.core import MainDB
    from sickrage.core.tv.show import TVShow
    session = sickrage.app.main_db.session()
    return [TVShow(x.indexer_id, x.indexer) for x in session.query(MainDB.TVShow).with_entities(MainDB.TVShow.indexer_id, MainDB.TVShow.indexer)]
