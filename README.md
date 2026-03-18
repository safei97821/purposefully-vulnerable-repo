# IntraPanel — Purposefully Vulnerable Flask App

> **WARNING: This application contains intentional security vulnerabilities.**
> It is designed exclusively for security tooling development and testing.
> **Do NOT deploy to any internet-accessible or production environment.**

IntraPanel is a fictional internal admin dashboard for a small SaaS company. It provides user lookup, file management, network diagnostics, and API token generation — all implemented with deliberately insecure patterns to generate realistic SAST and SCA findings.

---

## Vulnerability Index

| File | Function / Route | Vulnerability | Bandit Rule | Severity |
|------|-----------------|---------------|-------------|----------|
| `db.py` | `find_user()` | SQL injection (`%` format string) | B608 | HIGH |
| `db.py` | `find_user_by_email()` | SQL injection (f-string) | B608 | HIGH |
| `db.py` | `create_user()` | SQL injection (`.format()`) | B608 | HIGH |
| `db.py` | module level | Hardcoded DB password | B105/B106 | LOW |
| `app.py` | module level | Hardcoded `secret_key`, `INTERNAL_API_KEY`, `ADMIN_PASSWORD` | B105 | LOW |
| `app.py` | `GET /diag/ping` | Command injection (`subprocess` + `shell=True`) | B602 | HIGH |
| `app.py` | `GET /files/download` | Command injection + path traversal (`shell=True`) | B602 | HIGH |
| `utils.py` | `hash_password()` | Weak MD5 password hashing | B324 | MEDIUM |
| `utils.py` | `generate_token()` | Insecure randomness for security token | B311 | LOW |
| `app.py` | `load_config()` | `yaml.load()` without `Loader=` | B506 | MEDIUM |

### Dependency CVEs (detected by `pip-audit` or SCA tooling)

| Package | Version | CVE |
|---------|---------|-----|
| Flask | 0.12.4 | CVE-2018-1000656 (DoS via malformed JSON body) |
| Werkzeug | 0.15.5 | CVE-2019-14806 (predictable debug PIN) |
| Jinja2 | 2.11.3 | CVE-2020-28493 (ReDoS) |
| requests | 2.19.1 | CVE-2018-18074 (credential exposure on redirect) |
| PyYAML | 5.1 | CVE-2020-14343 (arbitrary code execution via `yaml.load`) |
| Pillow | 8.0.0 | CVE-2021-25290 (heap buffer overflow, CVSS 9.8) |
| paramiko | 2.4.1 | CVE-2018-1000805 (auth bypass, CVSS 9.8) |

---

## Local Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

App runs at `http://localhost:5000`. On first start, register a user at `/register`.

---

## Run Bandit (SAST)

```bash
pip install bandit
# Show MEDIUM and HIGH findings (what the pipeline processes)
bandit -r . --severity-level medium -f json | python3 -m json.tool

# All findings including LOW
bandit -r . -f text
```

**Expected findings at `--severity-level medium`:** 7 issues — B608 ×3 (HIGH), B602 ×2 (HIGH), B324 ×1 (MEDIUM), B506 ×1 (MEDIUM).

---

## Run pip-audit (SCA)

```bash
pip install pip-audit
pip-audit -r requirements.txt
```
