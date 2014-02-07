# Copyright (C) 2013-2014 Fox Wilson, Peter Foley, Srijay Kasturi, Samuel Damashek, James Forcier and Reed Koser
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from time import localtime, strftime
from helpers.hook import Hook
from helpers.orm import Notes


@Hook(['pubmsg', 'action'], ['nick', 'db'])
def handle(send, msg, args):
    cursor = args['db']
    nick = args['nick']
    notes = cursor.query(Notes).filter(Notes.nick == nick).filter(Notes.pending == 1).order_by(Notes.time.asc()).all()
    for note in notes:
        time = strftime('%Y-%m-%d %H:%M:%S', localtime(note['time']))
        send("%s: Note from %s: <%s> %s" % (nick, note['submitter'], time, note['note']))
        note.pending = 0