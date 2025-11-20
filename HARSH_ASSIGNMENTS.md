
Assignment 1 — CloudFront (single distribution) + two S3 origins


I will be using Terraform 
Create main.tf, variables.tf, outputs.tf  & then apply terraform init   terraform plan  &  terraform apply.

main.tf

terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "bucket1" {
  bucket = var.bucket1_name
  acl    = "public-read"
  website {
    index_document = "index.html"
    error_document = "error.html"
  }
}

resource "aws_s3_bucket_object" "bucket1_index" {
  bucket = aws_s3_bucket.bucket1.id
  key    = "index.html"
  content = "Hello, CDN origin is working fine"
  acl    = "public-read"
  content_type = "text/html"
}

resource "aws_s3_bucket" "bucket2" {
  bucket = var.bucket2_name
  acl    = "public-read"
  website {
    index_document = "index.html"
    error_document = "error.html"
  }
}

resource "aws_s3_bucket_object" "bucket2_index" {
  bucket = aws_s3_bucket.bucket2.id
  key    = "devops-folder/index.html"
  content = "Hello, CDN 2 origin is working fine"
  acl    = "public-read"
  content_type = "text/html"
}

data "aws_iam_policy_document" "public_bucket_policy_bucket1" {
  statement {
    sid = "PublicReadGetObject"
    principals {
      type = "AWS"
      identifiers = ["*"]
    }
    actions = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.bucket1.arn}/*"]
  }
}

resource "aws_s3_bucket_policy" "bucket1_policy" {
  bucket = aws_s3_bucket.bucket1.id
  policy = data.aws_iam_policy_document.public_bucket_policy_bucket1.json
}

data "aws_iam_policy_document" "public_bucket_policy_bucket2" {
  statement {
    sid = "PublicReadGetObject"
    principals {
      type = "AWS"
      identifiers = ["*"]
    }
    actions = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.bucket2.arn}/*"]
  }
}

resource "aws_s3_bucket_policy" "bucket2_policy" {
  bucket = aws_s3_bucket.bucket2.id
  policy = data.aws_iam_policy_document.public_bucket_policy_bucket2.json
}

resource "aws_cloudfront_distribution" "cdn" {
  enabled = true
  comment = "Single distribution with two origins for assignment"

  origins {
    domain_name = aws_s3_bucket.bucket1.website_endpoint
    origin_id   = "S3-BUCKET-ROOT"
    custom_origin_config {
      http_port = 80
      https_port = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols = ["TLSv1.2"]
    }
  }

  origins {
    domain_name = aws_s3_bucket.bucket2.website_endpoint
    origin_id   = "S3-BUCKET-DEVOPS-FOLDER"
    custom_origin_config {
      http_port = 80
      https_port = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]
    target_origin_id = "S3-BUCKET-ROOT"
    viewer_protocol_policy = "redirect-to-https"
    forwarded_values {
      query_string = false
      cookies { forward = "none" }
    }
    min_ttl = 172800
    default_ttl = 86400
    max_ttl = 31536000
  }

  ordered_cache_behavior {
    path_pattern = "devops-folder/*"
    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]
    target_origin_id = "S3-BUCKET-DEVOPS-FOLDER"
    viewer_protocol_policy = "redirect-to-https"
    forwarded_values {
      query_string = false
      cookies { forward = "none" }
    }
    min_ttl = 0
    default_ttl = 3600
    max_ttl = 86400
  }

  restrictions {
    geo_restriction { restriction_type = "none" }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  price_class = "PriceClass_All"
  is_ipv6_enabled = true
}




**variables.tf

variable "aws_region" { default = "us-east-1" }
variable "bucket1_name" { default = "devops-assignment-bucket-root-unique-12345" }
variable "bucket2_name" { default = "devops-assignment-bucket-devops-unique-12345" }
```

outputs.tf

output "cloudfront_domain_name" {
  value = aws_cloudfront_distribution.cdn.domain_name
}
```

Notes: As I am using S3 website endpoints, It allows folder URLs to return index.html automatically. For production private buckets use Origin Access Control (OAC) and optionally LambdaEdge or CloudFront Function to rewrite directory requests to index.html.

---

Assignment 2 — Top 8 IP addresses script

# As Iam using logfile which is provided for reference in Assignment-2

#!/bin/bash


LOGFILE="logfile.txt"
if [ ! -f "$LOGFILE" ]; then
  echo "Error: $LOGFILE not found in current directory. Please place logfile.txt here."
  exit 1
fi
awk '{print $1}' "$LOGFILE" | sort | uniq -c | sort -nr | head -8 | awk '{print $2, $1}'


Then I will execute

chmod +x count

Then

./count


Output will be:

92.6.41.236 22
186.248.72.9 19
81.243.137.36 18
213.118.39.51 15
217.118.78.16 15
80.116.15.0 14
93.146.139.64 14
186.213.159.176 11




Assignment 3 — High load troubleshooting

As there will be multiple steps to check which is using more cpu more disk space or depending upon the log files.

1.
# Who's logged in and system uptime
uptime
who -a

# Top processes by CPU and memory (interactive)
top
# or htop (if installed)
htop

# Snapshot top output (non-interactive)
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -n 20

# kill the process if not reqd
kill -9 pid

# Check processes in uninterruptible sleep (D-state) which often cause high load
ps -eo pid,cmd,state,wchan:20 | awk '$3=="D"{print $0}'

# Check I/O wait and disk usage
iostat -x 1 3    
vmstat 1 5
df -h

Then execute
- High %wa in iostat or vmstat

then execute in bash
free -m
cat /proc/swaps

2. Check disk and filesystem

# Check largest files and directories
du -sh /* 2>/dev/null | sort -hr | head -n 20
du -sh /var/* 2>/dev/null | sort -hr | head -n 20

# Inspect system logs for errors
journalctl -p 3 -xb --no-pager    
tail -n 200 /var/log/messages || tail -n 200 /var/log/syslog
```
We will look for filesystem full, IO errors, failing disks, corrs, dmesg errors by executing these commands

3. Networking / high connection counts

ss -s
ss -plant | head -n 40
netstat -tunp | head -n 40





