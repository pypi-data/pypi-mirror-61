# zec2

[![PyPI version](https://badge.fury.io/py/zec2.svg)](https://badge.fury.io/py/zec2)
[![Build Status](https://travis-ci.com/arrrlo/zec2.svg?branch=master)](https://travis-ci.com/arrrlo/zec2)

![GitHub issues](https://img.shields.io/github/issues/arrrlo/zec2.svg)
![GitHub closed issues](https://img.shields.io/github/issues-closed/arrrlo/zec2.svg)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/arrrlo/zec2.svg)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zec2.svg)
![GitHub](https://img.shields.io/github/license/arrrlo/zec2.svg?color=blue)
![GitHub last commit](https://img.shields.io/github/last-commit/arrrlo/zec2.svg?color=blue)

Easily manage your AWS EC2 instances

## INSTALL

```bash
pip install zec2
```

## CONFIGURE AWS CREDENTIALS

You should have this two files on your computer:

`~/.aws/config`:

```ini
[default]
region=your_aws_region
output=json
```

`~/.aws/credentials`:

```ini
[default]
aws_access_key_id=your_access_key_id
aws_secret_access_key=your_secret_access_key
```

To learn more about AWS credentials and how to install them on your computer, please read this:
[https://docs.aws.amazon.com/rekognition/latest/dg/setting-up.html](https://docs.aws.amazon.com/rekognition/latest/dg/setting-up.html)

## DIFFERENT AWS PROFILES

You can put as many profiles in your aws credentials file and call them with zec2:

```bash
# use default aws profile
> zec2 ls

# use different aws profile
> zec2 -p my_profile ls
```

Use this option with every command.

## CLI COMMANDS

```bash
# list all EC2 instances
> zec2 ls

# list all EC2 instances using custom aws profile (applies to all commands)
> zec2 -p work ls

# live list all EC2 instances
> zec2 ls -f

# ssh to 1st instance from the list
> $(zec2 ssh 1)

# ssh using different user (the default is ec2-user)
> $(zec2 ssh 1 -u ubuntu)

# ssh using different pem key path (the default is ~/.ssh/__instance_key_pair__.pem)
> $(zec2 ssh 1 -i ~/path/to/key.pem)

# stop 1st EC2 instance from the list
> zec2 stop 1

# start 1st EC2 instance from the list
> zec2 start 1

# restart 1st EC2 instance from the list
> zec2 restart 1

# terminate 1st EC2 instance from the list
> zec2 terminate 1
```

