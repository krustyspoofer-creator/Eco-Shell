# Branch Protection Settings

This document describes the recommended branch protection rules for the EchoShell repository to "lock" the codebase and ensure quality control.

## Recommended Settings for Main/Master Branch

### Protection Rules

Enable the following settings in GitHub repository settings under **Settings → Branches → Branch protection rules**:

#### 1. Require Pull Request Reviews Before Merging
- ✅ **Required approvals**: 1
- ✅ **Dismiss stale pull request approvals when new commits are pushed**
- ✅ **Require review from Code Owners** (enforces CODEOWNERS file)

#### 2. Require Status Checks to Pass Before Merging
- ✅ **Require branches to be up to date before merging**
- ✅ **Status checks required**:
  - `Shellcheck Validation` - Validates all shell scripts
  - `Security Scan` - Scans for security issues

#### 3. Require Conversation Resolution Before Merging
- ✅ **Require all conversations to be resolved** before merging

#### 4. Require Signed Commits
- ✅ **Require signed commits** (optional but recommended for security)

#### 5. Require Linear History
- ✅ **Require linear history** - Prevents merge commits

#### 6. Include Administrators
- ✅ **Include administrators** - Apply rules to admins too

#### 7. Restrict Push Access
- ✅ **Restrict who can push to matching branches**
- Only repository owners can push directly

#### 8. Prevent Force Pushes
- ✅ **Do not allow force pushes**

#### 9. Prevent Branch Deletion
- ✅ **Do not allow deletions**

## How to Enable

1. Go to repository Settings
2. Navigate to Branches
3. Click "Add rule" or edit existing rule
4. Enter branch name pattern: `main` or `master`
5. Enable the checkboxes listed above
6. Click "Create" or "Save changes"

## Additional Repository Settings

### General Settings

Navigate to **Settings → General**:

- **Disable**: Allow merge commits (to enforce linear history)
- **Enable**: Automatically delete head branches (cleanup after merge)
- **Enable**: Allow squash merging (recommended)
- **Enable**: Allow rebase merging (recommended)

### Security Settings

Navigate to **Settings → Code security and analysis**:

- ✅ **Dependabot alerts**: Enable
- ✅ **Dependabot security updates**: Enable  
- ✅ **Code scanning**: Enable
- ✅ **Secret scanning**: Enable

### Collaborators & Teams

Navigate to **Settings → Collaborators and teams**:

- Limit write access to trusted maintainers only
- Use CODEOWNERS file to enforce review requirements

## Testing Protection

After enabling these settings, test by:

1. Try to push directly to main: Should be blocked ❌
2. Try to force push: Should be blocked ❌
3. Open a PR without review: Should require approval ✅
4. Merge without passing checks: Should be blocked ❌

## Lock Status

Once these settings are enabled:
- ✅ Repository is "locked" from unauthorized changes
- ✅ All changes require review
- ✅ Code quality is enforced
- ✅ Security is validated automatically

## Maintenance

Review and update these settings:
- Quarterly security review
- After any security incidents
- When team structure changes
- Before major releases

---

**Note**: These settings ensure the repository maintains high security and code quality standards while preventing unauthorized modifications.
