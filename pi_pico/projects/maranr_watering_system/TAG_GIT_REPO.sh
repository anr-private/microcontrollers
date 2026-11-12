#!/usr/bin/env bash
# TAG_THE_GIT_REPO.sh
#
# Ask for a tag name, then tag the last commit (HEAD) of this repo and push
# the tag to the remote. Works from any directory inside the repo.
#
# WHAT IT CHECKS (each failure prints "ERROR: ..." and exits with status 1,
# before anything is tagged):
#   - the current directory is inside a git repository
#   - the tag name is not empty (leading and trailing spaces are removed first)
#   - the tag name is valid for git (git check-ref-format): no spaces inside,
#     no ~ ^ : ? * [ or backslash, no "..", must not end with "/" or ".lock"
#   - a tag with that name does not already exist in this repo
#   - the remote named in REMOTE_NAME exists
#
# WHAT IT WARNS ABOUT:
#   - Uncommitted changes in tracked files. A tag marks the last COMMIT (HEAD),
#     not the files as they are on disk right now, so the tag would not contain
#     those changes. You are asked "Tag anyway? [y/N]"; anything but y or Y
#     cancels and nothing is tagged. Untracked files are not reported.
#
# WHAT CAN GO WRONG AFTER TAGGING:
#   - If the push fails (no network, no permission, or a tag of that name
#     already exists on the remote), the tag stays in the local repo. The
#     script says so and prints the push command to retry. To undo the local
#     tag instead:  git tag -d TAGNAME
#   - Status 0 only if the tag was created AND pushed.
#
# WHAT IT DOES NOT CHECK:
#   - Whether HEAD is the commit you mean (for example a detached HEAD).
#   - Whether your branch has been pushed. Pushing the tag sends the tagged
#     commit to the remote even if the branch itself has not been pushed.
#
# HOW IT WAS TESTED: in a throwaway repo with a local bare repo as the remote,
# run from a subdirectory. Cases: empty name; invalid name; good name with
# surrounding spaces; duplicate name; uncommitted changes answered n (nothing
# tagged) and y (tagged and pushed); no remote; run outside a repo. A real
# network remote with authentication was not tested. With an empty remote git
# prints a harmless "push negotiation failed ... proceeding anyway" line.

REMOTE_NAME="origin"


fail() {
    echo "ERROR: $1" >&2
    exit 1
}


if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    fail "not inside a git repository"
fi

read -r -p "Tag name: " tag_name
tag_name="$(printf '%s' "$tag_name" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

if [ -z "$tag_name" ]; then
    fail "the tag name is empty"
fi
if ! git check-ref-format "refs/tags/$tag_name"; then
    fail "'$tag_name' is not a valid tag name"
fi
if git rev-parse -q --verify "refs/tags/$tag_name" >/dev/null; then
    fail "tag '$tag_name' already exists"
fi
if ! git remote get-url "$REMOTE_NAME" >/dev/null 2>&1; then
    fail "there is no remote named '$REMOTE_NAME'"
fi

if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    echo "WARNING: there are uncommitted changes. The tag marks the last commit, not those changes."
    read -r -p "Tag anyway? [y/N] " answer
    case "$answer" in
        y|Y) ;;
        *) echo "Cancelled. Nothing was tagged."; exit 1 ;;
    esac
fi

git tag "$tag_name" || fail "could not create the tag"
echo "Tagged commit $(git rev-parse --short HEAD) as '$tag_name'."

if git push "$REMOTE_NAME" "$tag_name"; then
    echo "Pushed '$tag_name' to $REMOTE_NAME."
else
    fail "the push failed. The tag exists locally. To retry: git push $REMOTE_NAME $tag_name"
fi

###