# Phone Store Project

A e-store project for Electric and Electronic Devices

## Getting Started

Migrate Database
```sh
python manage.py migrate
```
Load Data Samples

```sh
python manage.py samples
```
Test Card
```
Card Number: 5213720304238582
CVV: 642
Exp: 01-2032 
```

## Translation
To make messages
```
python manage.py makemessages --all --ignore env
```
Compile messages
```
python manage.py compilemessages --ignore env
```
