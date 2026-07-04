# 🛡️ Secure DevSecOps Pipeline for a Python Web Application

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Azure](https://img.shields.io/badge/Azure-Cloud-0078D4)
![Terraform](https://img.shields.io/badge/Terraform-IaC-623CE4)
![Ansible](https://img.shields.io/badge/Ansible-Automation-EE0000)
![OWASP](https://img.shields.io/badge/OWASP-DevSecOps-green)
![Status](https://img.shields.io/badge/Project-In%20Progress-orange)

---

# 📖 Project Story

Modern software delivery is no longer just about writing code and deploying applications.

Every stage of the Software Development Life Cycle (SDLC) introduces potential security risks—from accidentally committing secrets to a repository, to vulnerable third-party libraries, insecure infrastructure, misconfigured servers, and exploitable web applications.

This project demonstrates how security can be integrated into every stage of the CI/CD pipeline by following DevSecOps principles.

Instead of treating security as a final checkpoint before production, this pipeline continuously validates the application's security posture throughout development, build, deployment, and runtime.

The goal is not simply to use security tools.

The goal is to demonstrate how each tool contributes to building a secure software delivery lifecycle.

---

# 🎯 Project Objectives

This project aims to demonstrate:

- Secure CI/CD Pipeline Design
- Shift-Left Security
- Infrastructure as Code (IaC)
- Automated Security Testing
- Continuous Compliance Validation
- Secure Cloud Deployment
- Centralized Vulnerability Management

---

# 🏗 Project Architecture

```
                Developer
                    │
                    ▼
              Source Control
                    │
                    ▼
          Continuous Integration
                    │
      ┌─────────────┴─────────────┐
      │                           │
      ▼                           ▼
 Secret Scanning            Static Analysis
      │                           │
      ▼                           ▼
 Dependency Scan          Security Code Scan
      └─────────────┬─────────────┘
                    ▼
              Build Docker Image
                    │
                    ▼
          Infrastructure Provisioning
             (Terraform on Azure)
                    │
                    ▼
            Server Configuration
                 (Ansible)
                    │
                    ▼
          Deploy Python Application
                    │
      ┌─────────────┴─────────────┐
      │                           │
      ▼                           ▼
 Compliance Scan          Dynamic Security Test
(OpenSCAP / InSpec)        (OWASP ZAP)
      └─────────────┬─────────────┘
                    ▼
             DefectDojo Dashboard
                    │
                    ▼
          Security Reports & Metrics
```

---

# 🔒 Security Pipeline

The pipeline follows a defense-in-depth approach where every stage validates a different aspect of the application.

| Stage | Purpose | Tool |
|--------|----------|------|
| Secret Detection | Detect leaked credentials | TruffleHog |
| Repository Analysis | Identify exposed sensitive files | Gitrob |
| Static Application Security Testing | Analyze Python source code | Bandit |
| Dependency Scanning | Detect vulnerable Python packages | Safety |
| Containerization | Package application | Docker |
| Infrastructure Provisioning | Build Azure infrastructure | Terraform |
| Configuration Management | Configure servers | Ansible |
| Compliance Assessment | Validate OS security baseline | OpenSCAP |
| Compliance Testing | Verify infrastructure configuration | InSpec |
| Dynamic Application Security Testing | Test running application | OWASP ZAP |
| Vulnerability Management | Aggregate findings | DefectDojo |

---

# ☁ Cloud Infrastructure

The application is deployed to Microsoft Azure using Infrastructure as Code.

Provisioned resources include:

- Resource Group
- Virtual Network
- Network Security Group
- Public IP
- Ubuntu Virtual Machine
- Docker Runtime
- Python Web Application

Infrastructure is provisioned automatically using Terraform and configured using Ansible.

---

# 🐍 Application

The demo application is intentionally designed to include common security weaknesses for educational purposes.

Examples include:

- Hardcoded credentials
- Vulnerable dependencies
- SQL Injection
- Command Injection
- Weak password storage
- Insecure configuration
- Missing security headers
- Debug mode enabled

These vulnerabilities allow each security tool to produce meaningful findings during pipeline execution.

> **Note:** The vulnerabilities are intentional and should never be used in production environments.

---

# 📂 Project Structure

```
python-devsecops-pipeline/

├── app/
├── ansible/
├── terraform/
├── docker/
├── bandit/
├── zap/
├── openscap/
├── inspec/
├── reports/
├── screenshots/
├── Jenkinsfile
└── README.md
```

---

# 📊 Expected Workflow

1. Developer commits code.
2. CI pipeline starts automatically.
3. Secrets are scanned.
4. Source code is analyzed.
5. Dependencies are checked.
6. Docker image is built.
7. Azure infrastructure is provisioned.
8. Server configuration is applied.
9. Application is deployed.
10. Infrastructure compliance is validated.
11. Running application is tested dynamically.
12. All findings are imported into DefectDojo.
13. Security reports are generated.

---

# 📈 Reports

The project generates reports from multiple security tools.

Examples include:

- Bandit Report
- Safety Report
- TruffleHog Report
- OWASP ZAP Report
- OpenSCAP Report
- InSpec Report

These reports are centralized in DefectDojo for easier vulnerability management.

---

# 🎓 Learning Outcomes

This project demonstrates practical experience with:

- DevSecOps
- Secure CI/CD
- Secure SDLC
- Infrastructure as Code
- Cloud Security
- Static Analysis
- Dynamic Analysis
- Compliance Validation
- Vulnerability Management
- Container Security
- Azure Administration
- Automation

---

# 🚧 Project Status

This repository is being built incrementally.

Each stage of the pipeline will be implemented, tested, documented, and integrated before moving to the next phase.

Follow the commit history to see the project evolve from a simple Python application into a complete end-to-end DevSecOps platform.

---

# ⚠ Disclaimer

This project intentionally contains vulnerable code and insecure configurations for educational and testing purposes only.

Do not deploy this project to production environments.

---

# 📜 License

This project is released under the MIT License.