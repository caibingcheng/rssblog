from utils.date import date
from utils.generator import generator


def fds(ps):
    rss_all = ps['rssall']
    rss_member = ps['member']
    rss_fd = {}
    rss_fd_member = {}
    rss_fd_date = {}

    for rss in rss_all:
        if rss['id'] not in rss_fd.keys():
            rss_fd[rss['id']] = []
        rss_fd[rss['id']].append(rss)
    for member in rss_member:
        if member['id'] not in rss_fd_member.keys():
            rss_fd_member[member['id']] = []
        rss_fd_member[member['id']].append(member)

    ps['friends'] = rss_fd
    ps['friends-member'] = rss_fd_member
    ps['friends-date'] = {}
    ps['friends-rss'] = {}
    for (id, rss) in rss_fd.items():
        ps['friends-date'][id] = date(rss_fd, inkey=id, locale=False)
        ps['friends-rss'][id] = generator(rss_fd, inkey=id, locale=False)

    return ps
