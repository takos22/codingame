# Contributing to the `codingame` module

Thank you for your interest in contributing to this codingame API wrapper! We welcome contributions from the community to improve and expand this project. Please follow these guidelines to make the process smooth for everyone.

---

## 🚀 How to Contribute

1. **Fork the repository** on GitHub.
2. **Clone your fork** to your local machine:

   ```sh
   git clone https://github.com/your-username/codingame.git
   ```

3. **Create a new branch** for your feature or bugfix:

   ```sh
   git checkout -b feature-branch
   ```

4. **Make your changes** and commit:

   ```sh
   git commit -m "feat: add new feature description"
   ```

5. **Push your changes** to your fork:

   ```sh
   git push origin feature-branch
   ```

6. **Create a Pull Request (PR)** from your fork to the main repository.

---

## 🛠 Setting Up the Development Environment

1. Install dependencies:

   ```sh
   pip install -r requirements.txt
   pip install -r async-requirements.txt
   pip install -r dev-requirements.txt
   ```

2. (Optional) Create a virtual environment:
  
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

---

## 📜 Coding Guidelines

- Follow **[PEP 8](https://peps.python.org/pep-0008/)** for code style.
- Format code using the **formatting script**:

  ```sh
  ./scripts/format.sh
  ```

- Use **type hints** where applicable:
  
  ```python
  def add_numbers(a: int, b: int) -> int:
      return a + b
  ```
  
- Write **clear docstrings** using [PEP 257](https://peps.python.org/pep-0257/).
- Update docs if you can.

---

## ✅ Testing

- Ensure that tests pass before submitting a PR.
- Setup a **`.env` file** with the necessary variables:
  
  ```env
  TEST_LOGIN_REMEMBER_ME_COOKIE=... # your remember me cookie (see docs)
  TEST_LOGIN_REMEMBER_ME_COOKIE_312=... # a 2nd remember me cookie (not necessary, some clash of code tests will fail though)

  TEST_CODINGAMER_ID=... # a codingamer id (see docs)
  TEST_CODINGAMER_PSEUDO=... # a codingamer pseudo (see docs)
  TEST_CODINGAMER_PUBLIC_HANDLE=... # a codingamer public handle (see docs)

  TEST_CLASHOFCODE_PUBLIC_HANDLE=... # a clash of code public handle (see docs)
  ```
  
- Run tests with the **testing script**:
  
  ```sh
  ./scripts/test.sh --full
  ```
  
- If adding new functionality, include appropriate unit tests in the `tests/` directory.

---

## 📌 Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

- `feat: Add a new feature`
- `fix: Fix a bug`
- `docs: Update documentation`
- `refactor: Code refactoring without feature changes`
- `test: Add or update tests`

Example:

```sh
git commit -m "feat: add support for clash of codes"
```

---

## 🔍 Reporting Issues

If you find a bug or have a feature request:

- Check [open issues](https://github.com/takos22/codingame/issues) to see if it's already reported.
- Create a [new issue](https://github.com/takos22/codingame/issues/new) with:
  - A clear title and description.
  - Steps to reproduce (if a bug).
  - Expected vs. actual behavior.

---

## 🤝 Code of Conduct

By contributing, you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 💡 Need Help?

If you have any questions, feel free to open an issue or contact the maintainers.

Happy coding! 🚀
