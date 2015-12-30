# MailNext

Web mail client that separates mails from people and services (automated mails). Connects to mailserver via IMAP, syncs with local MySQL and front-end pulls from local mysql displays to user.

## To Do

### Back-end

- search new mails and fetch header and 
	flags (FLAGS BODY.PEEK[HEADER]) from IMAP server
- if new mailbox then get mails from max last 7 days
- fetch flags of last 20 mails on the list
- mechanism to refresh flags of existing mails (sync in background?)
- parse headers and subject and update `Mail Message` - if in services, set as 'service_mail'

### Front-end

- `mailbox` page
- listing (list from Mail Message) - on demand, pull more mails from IMAP
- sidebar build "services" (send in boot global + local)
- filter based on service

### User Management

- `signup` - create profile and mail account

