# Contributing to EchoShell

Thank you for your interest in contributing to EchoShell! This project is security-focused and requires careful review of all changes.

## Repository Lock Status

**⚠️ This repository implements strict protection policies:**

- All pull requests require review from repository owners
- Main branch is protected from direct pushes
- Force pushes and deletions are disabled
- Code must pass all validation checks before merge

## Before Contributing

1. Read the [Security Policy](../SECURITY.md)
2. Review the [Code of Conduct](CODE_OF_CONDUCT.md)
3. Understand the [Architecture](../architecture.md)

## Development Guidelines

### Shell Script Standards

All shell scripts must:
- Include shebang: `#!/bin/bash`
- Pass shellcheck validation with no errors
- Use proper error handling
- Include comments for complex logic
- Follow existing code style
- Use meaningful variable names

### Testing Your Changes

Before submitting a PR:

```bash
# Validate all shell scripts
shellcheck *.sh *.Sh "Demon reflect" "Demon monitor" "Sigil. Sh"

# Test boot sequence
bash Boot.Sh

# Verify no syntax errors
bash -n *.sh
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes following the guidelines
4. Test thoroughly
5. Commit with clear messages: `git commit -m "feat: add feature description"`
6. Push to your fork: `git push origin feature/your-feature`
7. Open a Pull Request with:
   - Clear description of changes
   - Rationale for the change
   - Testing performed
   - Any security considerations

## Pull Request Review Process

1. Automated checks run (shellcheck, security scans)
2. Repository owner reviews code
3. Feedback is provided
4. Changes are requested if needed
5. Once approved, PR is merged

## Code Review Checklist

- [ ] Code follows existing style
- [ ] Shellcheck passes with no errors
- [ ] No security vulnerabilities introduced
- [ ] Documentation updated if needed
- [ ] Changes are minimal and focused
- [ ] Commit messages are clear

## Commit Message Format

Use conventional commit format:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test additions or changes
- `chore:` - Build/maintenance tasks

## Questions?

Open an issue with the `question` label for clarification.

## License

By contributing, you agree that your contributions will be licensed under the MIT License + Sovereign Attribution.
