import os
import sys
import subprocess
from git import Repo
import random

def generate_commit_messages(diff_files):
    messages = [
        f"Updated {', '.join(diff_files)}",
        f"Refactored code in {', '.join(diff_files)}",
        f"Fixed issues in {', '.join(diff_files)}",
        f"Implemented new features in {', '.join(diff_files)}"
    ]
    return messages

def get_diff_files(repo):
    diff_files = []

    # Include changes between the index (staged changes) and the working tree
    for item in repo.index.diff(None):
        diff_files.append(item.a_path)

    # Include changes between the index (staged changes) and the HEAD commit
    for item in repo.index.diff(repo.head.commit):
        if item.a_path not in diff_files:
            diff_files.append(item.a_path)

    return diff_files

def print_diff(repo):
    # Print diff for unstaged changes
    for diff in repo.index.diff(None):
        print(f"\nDiff for {diff.a_path} (unstaged):")
        for line in diff.diff.splitlines():
            print(line)

    # Print diff for staged changes
    staged_diff = repo.git.diff('--cached').split('\n')
    if staged_diff:
        print("\nStaged changes:")
        for line in staged_diff:
            print(line)



def main():
    print(f"Current working directory: {os.getcwd()}")

    repo_path = os.getcwd()

    try:
        repo = Repo(repo_path)
        print(f"Git repository path: {repo.working_tree_dir}")
        print(f"Diff status: {repo.git.status()}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    if repo.is_dirty():
        print("The following files have changes:")
        diff_files = get_diff_files(repo)
        for f in diff_files:
            print(f"\t{f}")

        print_diff(repo)

        messages = generate_commit_messages(diff_files)
        print("\nSelect a commit message:")
        for i, msg in enumerate(messages):
            print(f"{i + 1}. {msg}")

        choice = int(input("\nEnter your choice (1-4): "))
        if 1 <= choice <= 4:
            commit_message = messages[choice - 1]
            repo.git.add(update=True)
            repo.index.commit(commit_message)
            print(f"\nSuccessfully committed with message: '{commit_message}'")
        else:
            print("\nInvalid choice. Exiting without committing.")
            sys.exit(1)
    else:
        print("There are no changes to commit.")

if __name__ == "__main__":
    main()
