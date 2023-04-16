import os
import sys
import subprocess
from git import Repo
import random
from openAIGenerator import OpenAIGen
import concurrent.futures

def generate_commit_messages(diff, num_messages=5):
    gen = OpenAIGen()

    # Define your prompt
    prompt = "Suggest a commit message for the changes made, this is a git diff:\n\n"
    prompt += "\n".join(diff)

    # Define a function to generate a single commit message
    def generate_message():
        return gen.gpt(prompt)

    # Use a thread pool to generate multiple commit messages in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_message) for _ in range(num_messages)]

    # Collect the generated commit messages from the completed futures
    generated_messages = [future.result() for future in futures]

    return generated_messages



def get_diff_files(repo):
    diff_files = []

    # Include changes between the index (staged changes) and the HEAD commit
    for item in repo.index.diff(repo.head.commit):
        if item.a_path not in diff_files:
            diff_files.append(item.a_path)

    return diff_files

def print_diff(repo):
    
    # Print diff for staged changes
    staged_diff = repo.git.diff('--cached').split('\n')
    if staged_diff:
        print("\nStaged changes:")
        for line in staged_diff:
            print(line)


def get_diff(repo):
    diff_lines = []

    # Get diff for staged changes
    staged_diff = repo.git.diff('--cached').split('\n')
    if staged_diff:
        diff_lines.append("\nStaged changes:")
        diff_lines.extend(staged_diff)

    return diff_lines


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

    staged_diff = repo.index.diff("HEAD")
    if staged_diff:
        print("The following files have changes:")
        diff_files = get_diff_files(repo)
        for f in diff_files:
            print(f"\t{f}")

        print_diff(repo)

        messages = generate_commit_messages(get_diff(repo))
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
        print("There are no changes staged for commit.")


if __name__ == "__main__":
    main()
