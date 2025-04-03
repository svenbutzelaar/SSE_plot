# This script can be used to calculate multiple statistics regarding issues
# and pull requests in a GitHub repository.

from github import Github

# Replace with your GitHub personal access token
TOKEN = "your GitHub personal access token"

# List of repositories (format: "owner/repo_name")
REPOSITORIES = [
    "has2k1/plotnine",
    "Kozea/pygal",
    "matplotlib/matplotlib",
    "mwaskom/seaborn",
    "plotly/plotly.py",
    "vega/altair",
    "holoviz/holoviews",
]

# Authenticate with GitHub
g = Github(TOKEN)


def get_issue_metrics(repo_name):
    repo = g.get_repo(repo_name)
    issues = repo.get_issues(state="closed")  # Fetch only closed items

    issue_closure_durations = [1] # How long does it take for an issue to be closed
    pr_closure_durations = [1] # How long does it take for a pr to be closed
    response_durations = [1] # How long until the first response on closed issues
    open_response_durations = [1] # How long until the first response on open issues
    no_responses_closed = 0 # How many closed issues have no responses
    no_responses_open = 0 # How many open issues have no responses
    for issue in issues:
        if issue.closed_at and issue.created_at:
            closure_time = (issue.closed_at - issue.created_at).total_seconds()

            if issue.pull_request is not None:  # It's a PR
                pr_closure_durations.append(closure_time)
            else:  # It's a regular issue
                issue_closure_durations.append(closure_time)

                # Compute first response time for issues only
                comments = issue.get_comments()
                if comments.totalCount > 0:
                    first_response_time = (comments[0].created_at - issue.created_at).total_seconds()
                    response_durations.append(first_response_time)
                else:
                    no_responses_closed += 1
    open_issues = repo.get_issues(state="open")

    for issue in open_issues:
        if issue.pull_request is not None:
            continue
        if issue.created_at:
            comments = issue.get_comments()
            if comments.totalCount > 0:
                first_response_time = (comments[0].created_at - issue.created_at).total_seconds()
                open_response_durations.append(first_response_time)
            else:
                no_responses_open += 1


    # Compute averages
    avg_issue_closure = (sum(issue_closure_durations) / len(issue_closure_durations) / 3600) if issue_closure_durations else None
    avg_pr_closure = (sum(pr_closure_durations) / len(pr_closure_durations) / 3600) if pr_closure_durations else None
    avg_response_time = (sum(response_durations) / len(response_durations) / 3600) if response_durations else None
    avg_open_response_time = (sum(open_response_durations) / len(open_response_durations) / 3600) if open_response_durations else None
    avg_response_closed_open = (sum(response_durations) + sum(open_response_durations)) / len(response_durations + open_response_durations) / 3600 if response_durations and open_response_durations else None
    avg_all_issues_responeses = (sum(response_durations) + sum(open_response_durations) + no_responses_open * 7 * 24 + no_responses_closed * 7 * 24) / (len(response_durations) + len(open_response_durations) + no_responses_open + no_responses_closed) / 3600 if response_durations and open_response_durations else None
    # Compute total average (issues + PRs combined)
    total_closure_durations = issue_closure_durations + pr_closure_durations
    avg_total_closure = (
                sum(total_closure_durations) / len(total_closure_durations) / 3600) if total_closure_durations else None

    return avg_issue_closure, avg_pr_closure, avg_total_closure, avg_response_time, avg_open_response_time, avg_response_closed_open, no_responses_closed, no_responses_open, avg_all_issues_responeses


# Loop through each repo and print results
for repo in REPOSITORIES:
    avg_issue_closure, avg_pr_closure, avg_total_closure, avg_response, avg_open_response, avg_response_closed_open, no_responses_closed, no_responses_open, avg_all_issues_responeses = get_issue_metrics(repo)

    issue_closure_str = f"{avg_issue_closure:.2f} hours" if avg_issue_closure is not None else "No data"
    pr_closure_str = f"{avg_pr_closure:.2f} hours" if avg_pr_closure is not None else "No data"
    total_closure_str = f"{avg_total_closure:.2f} hours" if avg_total_closure is not None else "No data"
    response_str = f"{avg_response:.2f} hours" if avg_response is not None else "No responses"
    open_response_str = f"{avg_open_response:.2f} hours" if avg_open_response is not None else "No responses"
    response_closed_open_str = f"{avg_response_closed_open:.2f} hours" if avg_response_closed_open is not None else "No open and closed responses"
    no_responses_closed_str = f"{no_responses_closed * 7 * 24}" if no_responses_closed is not None else "No closed responses"
    no_responses_open_str = f"{no_responses_open * 7 * 24}" if no_responses_open is not None else "No responses"
    all_issues_responses_str = f"{avg_all_issues_responeses}" if avg_all_issues_responeses is not None else "No responses"

    print(f"Repo: {repo}")
    print(f"  - Avg. Time to Close Issues: {issue_closure_str}")
    print(f"  - Avg. Time to Close Pull Requests: {pr_closure_str}")
    print(f"  - Avg. Total Closure Time (Issues + PRs): {total_closure_str}")
    print(f"  - Avg. First Response Time (Closed issues only): {response_str}")
    print(f"  - Avg. First Response Time (Open issues only): {open_response_str}")
    print(f"  - Avg. First Response Time (Open and closed issues): {response_closed_open_str}")
    print(f"  - No responses closed: {no_responses_closed_str}")
    print(f"  - No responses open: {no_responses_open_str}")
    print(f"  - Avg. First Response Time (Open, closed and not responded issues): {all_issues_responses_str}")

    print("-" * 60)