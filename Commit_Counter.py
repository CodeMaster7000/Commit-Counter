import json
from restkit import request
#Enter username here
USER = 'CodeMaster7000'
def count_user_commits(user):
    r = request('https://api.github.com/users/%s/repos' % user)
    repos = json.loads(r.body_string())
    for repo in repos:
        if repo['fork'] is True:
            continue
        n = count_repo_commits(repo['url'] + '/commits')
        yield (repo['name'], n)
def count_repo_commits(commits_url, _acc=0):
    r = request(commits_url)
    commits = json.loads(r.body_string())
    n = len(commits)
    if n == 0:
        return _acc
    link = r.headers.get('link')
    if link is None:
        return _acc + n
    next_url = find_next(r.headers['link'])
    if next_url is None:
        return _acc + n
    return count_repo_commits(next_url, _acc + n)
def find_next(link):
    for l in link.split(','):
        a, b = l.split(';')
        if b.strip() == 'rel="next"':
            return a.strip()[1:-1]
if __name__ == '__main__':
    total = 0
    for repo, n in count_user_commits(USER):
        print "The repository `%s` has %d commits." % (repo, n)
        total += n
    print "Total commits: %d" % total
