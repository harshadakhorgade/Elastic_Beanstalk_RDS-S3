

---

```markdown
# Django Deployment on AWS with Elastic Beanstalk, RDS, and S3

This project demonstrates deploying a Django application using **AWS Elastic Beanstalk**, **Amazon RDS** for PostgreSQL, and **Amazon S3** for static and media files.

## 🌐 Hosted Services

- **Elastic Beanstalk**: For Django app hosting.
- **RDS (PostgreSQL)**: For production-ready relational database.
- **S3**: For serving static and media files.

---

## 🔧 Environment Setup

### 1. Set Environment Variables

Run the following commands to configure environment variables for AWS and Django:

```bash
eb setenv AWS_ACCESS_KEY_ID=example\
          AWS_SECRET_ACCESS_KEY=example\
          AWS_STORAGE_BUCKET_NAME=myapp-static-demo \
          AWS_REGION=us-west-2

eb setenv DJANGO_SECRET_KEY="django-insecure-m10c@k!u5b!y@=n%!9dxmc4#=q)q$)tdu$6$&w#1p_y107=2c_" \
          DJANGO_DEBUG="1"
```

### 2. RDS Configuration

Edit RDS **Security Group** Inbound Rules:

- Add **your IP** to allow PostgreSQL access (port 5432).
- Add **EC2 Security Group** to allow Beanstalk app access.

```bash
MYIP = 42.104.224.58/32
```

Set environment variables for RDS:

```bash
eb setenv RDS_HOSTNAME=backenddemo.cxks8a2gwtg9.us-west-2.rds.amazonaws.com \
          RDS_DB_NAME=backenddemo \
          RDS_USERNAME=mysuperuser \
          RDS_PASSWORD=mysuperuser \
          RDS_PORT=5432
```

---

## 🛠️ EB SSH + Django Commands

```bash
eb ssh
cd /var/app/current
source /var/app/venv/*/bin/activate
python manage.py migrate
```

To connect directly to the RDS instance:

```bash
psql -h backenddemo.cxks8a2gwtg9.us-west-2.rds.amazonaws.com \
     -U mysuperuser \
     -d backenddemo \
     -p 5432
```

Useful Postgres commands:

```sql
\dt        -- List all tables
SELECT * FROM your_table_name;
\dn        -- Show all schemas
\l         -- List all databases
\du        -- List all roles/users
```

---

## 📦 S3 Setup for Static/Media Files

### 1. Create an S3 Bucket

- Bucket Name: `myapp-static-demo`
- Turn **"Block all public access"** to **Off**.

### 2. Permissions

#### Bucket Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAccountAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::590184012044:root"
      },
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::myapp-static-demo",
        "arn:aws:s3:::myapp-static-demo/*"
      ]
    },
    {
      "Sid": "AllowPublicReadAccessToMedia",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::myapp-static-demo/media/*"
    }
  ]
}
```

#### CORS Configuration

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "POST", "PUT", "HEAD"],
    "AllowedOrigins": ["*"],
    "ExposeHeaders": []
  }
]
```

---

## 📂 `.ebextensions/01_django.config`

```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: "core.settings"
    PYTHONPATH: "/var/app/current:$PYTHONPATH"
  aws:elasticbeanstalk:container:python:
    WSGIPath: "core.wsgi:application"

container_commands:
  01_makemigrations:
    command: "source /var/app/venv/*/bin/activate && python3 manage.py makemigrations --noinput"
    leader_only: true
  02_migrate:
    command: "source /var/app/venv/*/bin/activate && python3 manage.py migrate --noinput"
    leader_only: true
  03_superuser:
    command: "source /var/app/venv/*/bin/activate && python3 manage.py createsu"
    leader_only: true
  04_collectstatic:
    command: "source /var/app/venv/*/bin/activate && python3 manage.py collectstatic --noinput"
    leader_only: true
```

---

## 🧪 Local Debugging

To open the Django shell with DB access:

```bash
source /var/app/venv/*/bin/activate
cd /var/app/current
python manage.py dbshell
```

---

## 📦 PostgreSQL Installation on EC2

```bash
sudo dnf install postgresql15 -y
```

---

## 🔐 IAM and S3 Permissions

- Create a **group** with `AmazonS3FullAccess` policy.
- Create an **IAM user** and add to that group.
- Generate **Access Key ID** and **Secret Access Key**.

---

## 📁 Repo Structure

```
Elastic_Beanstalk_RDS-S3/
│
├── .ebextensions/
│   └── 01_django.config
├── core/
│   ├── settings.py
│   ├── wsgi.py
│   └── ...
├── manage.py
├── requirements.txt
├── README.md
└── ...
```

---

## ✅ Final Checklist Before Deployment

- [x] Set all required `eb setenv` variables.
- [x] Update `ALLOWED_HOSTS` in `settings.py`.
- [x] Configure `DATABASES` and `AWS_STORAGE` in Django settings.
- [x] Push your app with `eb deploy`.
- [x] Verify app and database connections.

---

## 📎 Reference

- [AWS Elastic Beanstalk Docs](https://docs.aws.amazon.com/elasticbeanstalk/)
- [Amazon RDS PostgreSQL Docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)
- [Django S3 Storage Docs](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html)

---

## 🙌 Author

**Harshad A Khorgade**  
🔗 [GitHub Profile](https://github.com/harshadakhorgade)

---

```

