import requests
from datetime import datetime, timedelta

# 配置GitHub API
GITHUB_API = "https://api.github.com"
REPO = "pallets/flask"  # 更新为Flask的仓库路径
TOKEN = ""  # 替换为你的GitHub Personal Access Token

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def get_issues(state="open"):
    """
    获取仓库的Issues。
    :param state: Issues的状态，'open'或'closed'
    :return: Issues列表
    """
    url = f"{GITHUB_API}/repos/{REPO}/issues?state={state}&per_page=100"
    response = requests.get(url, headers=headers)
    issues = response.json()
    return issues

def calculate_average_close_time(issues):
    """
    计算Issues平均关闭时间。
    :param issues: 闭合Issues的列表
    :return: 平均关闭时间（天）
    """
    total_time = timedelta()
    for issue in issues:
        created_at = datetime.strptime(issue['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        closed_at = datetime.strptime(issue['closed_at'], "%Y-%m-%dT%H:%M:%SZ")
        total_time += (closed_at - created_at)
    average_time = total_time / len(issues) if issues else timedelta()
    return average_time.days

def get_commit_count(since_days=30):
    """
    获取特定时间段内的提交次数。
    :param since_days: 天数
    :return: 提交次数
    """
    since_date = (datetime.now() - timedelta(days=since_days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"{GITHUB_API}/repos/{REPO}/commits?since={since_date}"
    response = requests.get(url, headers=headers)
    commits = response.json()
    return len(commits)

def get_contributors_count():
    """
    获取项目的贡献者数量。
    :return: 贡献者数量
    """
    url = f"{GITHUB_API}/repos/{REPO}/contributors?per_page=1&anon=true"
    response = requests.get(url, headers=headers)
    contributors_count = int(response.headers['Link'].split(",")[1].split(">")[0].split("&page=")[1])
    return contributors_count

def get_pull_requests(state="all"):
    """
    获取仓库的Pull Requests。
    :param state: PR的状态，'open'、'closed'或'all'
    :return: PR列表
    """
    url = f"{GITHUB_API}/repos/{REPO}/pulls?state={state}&per_page=100"
    response = requests.get(url, headers=headers)
    prs = response.json()
    return prs

def calculate_average_pr_merge_time(prs):
    """
    计算PR平均合并时间。
    :param prs: PR列表
    :return: 平均合并时间（天）
    """
    merged_prs = [pr for pr in prs if pr.get('merged_at')]
    total_time = timedelta()
    for pr in merged_prs:
        created_at = datetime.strptime(pr['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        merged_at = datetime.strptime(pr['merged_at'], "%Y-%m-%dT%H:%M:%SZ")
        total_time += (merged_at - created_at)
    average_time = total_time / len(merged_prs) if merged_prs else timedelta()
    return average_time.days

def get_community_engagement():
    """
    获取社区参与度指标：Star、Forks、Watchers。
    :return: 社区参与度字典
    """
    url = f"{GITHUB_API}/repos/{REPO}"
    response = requests.get(url, headers=headers)
    repo_data = response.json()
    engagement = {
        'stars': repo_data['stargazers_count'],
        'forks': repo_data['forks_count'],
        'watchers': repo_data['watchers_count']
    }
    return engagement

def get_issues_with_comments(state="all"):
    """
    获取包含评论的Issues。
    :param state: Issues的状态
    :return: Issues列表
    """
    issues = get_issues(state)
    issues_with_comments = [issue for issue in issues if issue['comments'] > 0]
    return issues_with_comments

def calculate_average_issue_response_time(issues):
    """
    计算Issue的平均响应时间。
    :param issues: 包含评论的Issues列表
    :return: 平均响应时间（小时）
    """
    total_response_time = timedelta()
    for issue in issues:
        issue_created_at = datetime.strptime(issue['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        comments_url = issue['comments_url']
        response = requests.get(comments_url, headers=headers)
        comments = response.json()
        if comments:
            first_comment_created_at = datetime.strptime(comments[0]['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            total_response_time += (first_comment_created_at - issue_created_at)
    average_response_time = (total_response_time / len(issues)).total_seconds() / 3600 if issues else timedelta()
    return average_response_time

def calculate_crv(average_close_time, average_pr_merge_time, average_issue_response_time):
    """
    计算综合响应速度指标（Comprehensive Response Velocity, CRV）。
    :param average_close_time: Issues平均关闭时间（天）
    :param average_pr_merge_time: PRs平均合并时间（天）
    :param average_issue_response_time: Issues平均响应时间（小时）
    :return: CRV值（天）
    """
    # 将Issues平均响应时间从小时转换为天
    average_issue_response_time_days = average_issue_response_time / 24
    crv = (average_close_time + average_pr_merge_time + average_issue_response_time_days) / 3
    return crv

def calculate_cae(contributors, stars, forks):
    """
    计算社区活跃和参与度指标（Community Activity and Engagement, CAE）。
    :param contributors: 贡献者数量
    :param stars: Stars数量
    :param forks: Forks数量
    :return: CAE值，基于简化计算的指标
    """
    # 为了简化，这里我们仅将这三个指标简单相加得到一个指标值
    # 实际应用中，可以根据项目具体情况调整权重
    cae = contributors + stars + forks
    return cae


if __name__ == "__main__":
    # 示例用法
    closed_issues = get_issues('closed')
    print(f"Closed issues: {len(closed_issues)}")
    print(f"Average close time: {calculate_average_close_time(closed_issues)} days")

    commit_count = get_commit_count()
    print(f"Commits in the last 30 days: {commit_count}")

    contributors_count = get_contributors_count()
    print(f"Contributors: {contributors_count}")

    # 示例用法
    prs = get_pull_requests('all')
    print(f"Total PRs: {len(prs)}")
    print(f"Average PR merge time: {calculate_average_pr_merge_time(prs)} days")

    engagement = get_community_engagement()
    print(
        f"Stars: {engagement['stars']}, Forks: {engagement['forks']}, Watchers: {engagement['watchers']}")

    # 示例用法
    issues_with_comments = get_issues_with_comments('closed')
    print(
        f"Average Issue response time: {calculate_average_issue_response_time(issues_with_comments)} hours")

    # 确保之前的函数和数据已经定义和计算
    average_close_time = calculate_average_close_time(closed_issues)
    average_pr_merge_time = calculate_average_pr_merge_time(prs)
    average_issue_response_time = calculate_average_issue_response_time(
        issues_with_comments)
    crv = calculate_crv(average_close_time, average_pr_merge_time,
                        average_issue_response_time)
    print(f"Comprehensive Response Velocity (CRV): {crv} days")

    cae = calculate_cae(contributors_count, engagement['stars'], engagement['forks'])
    print(f"Community Activity and Engagement (CAE): {cae}")
