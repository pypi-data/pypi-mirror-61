# instant-mailer
```sh
pip install instantmailer
```

A Python module that allows you to send instant mails using Python.
Python Requires <= 3.6

## Features
* Fully secured with **SSL**
* Instant mails
* Send mails with attachment

## Additional Libraries
* email
* ssl

## Getting Started

```py
import instant-mailer

mail = instant-mailer.Mail("example@example.com", "12345678") # Replace with your email and password
```

**Attributes**

```py
await mail.send()
```

Sends the email
		
		Parameters
		----------
		reciever: :class: `str`
			The recievers mail address
		body: :class: `str`
			The body of the mail
		subject: :class: `str`
			The subject of the mail
		bcc: :class: `str`
			The bcc of the mail
		attachment_name: :class: `str`
			The name of the attachment
		attachment_bytes: :class: `str`
			The bytes of the attachment


